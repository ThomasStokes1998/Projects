use rand::{thread_rng, Rng};
use std::cmp::min;

use crate::utils::retrieve_bitsu64;
use crate::table::Tables;

const COLOURS:usize = 5;
const MAXPENALTY:u8 = 7;
const TILEGROUPS:usize = 9;
// Player board sections
//const SCORESTART:u64 = 0;
//const SCOREEND:u64 = 8;
const PENALTIESSTART:u64 = 9;
const PENALTIESEND:u64 = 11;
//const ISTURNSTART:u64 = 12;
//const ISTURNEND:u64 = 12;
//const YELLOWSQUARESTART:u64 = 13;
//const YELLOWSQUAREEND:u64 = 13;
const FILLEDTILESSTART:u64 = 14;
const FILLEDTILESEND:u64 = 23;
const TILECOLOURSSTART:u64 = 24;
const TILECOLOURSEND:u64 = 38;
const RIGHTBOARDSTART:u64 = 39;
const RIGHTBOARDEND:u64 = 63;


#[derive(Debug, Clone, Copy, Default)]
pub struct TilePool {
    pub innertilepool:u32,
    pub outertilepool:u64
}

impl TilePool {
    pub fn new() -> TilePool {
        return Default::default()
    }

    pub fn generate_outer_tile_pool(&mut self, mut tilebag:Vec<u8>, table:&Tables) {
        let mut rng = thread_rng();
        let mut tilepool: u64 = 0;
        let mut tiles_vec: Vec<u64> = Vec::with_capacity(TILEGROUPS);
        let mut tilebagcounters = tilebag.iter().sum();
        for _ in 0..TILEGROUPS {
            let mut tilegroup: u16 = 0;
            for _ in 0..4 {
                let r = rng.gen_range(0..tilebagcounters) as u8;
                let mut cumulative: u8  = 0;
                let mut colour = 0;
                for c in 0..5 {
                    cumulative += tilebag[c];
                    if cumulative <= r {
                        continue;
                    }
                    colour = c;
                    break;
                }
                
                tilegroup += 8_u16.pow(colour as u32);
                tilebag[colour] -= 1;
                tilebagcounters -= 1;
            }
            match table.tilegroup_encoder.binary_search(&tilegroup) {
                Ok(t) => tiles_vec.push(1 + t as u64),
                Err(_) => panic!("Tilegroup {} not in tilegroup encoder",tilegroup)
            }
        }
        tiles_vec.sort();
        for &tile in tiles_vec.iter() {
            tilepool <<= 7;
            tilepool += tile;
        }
        self.outertilepool = tilepool;
    }

    pub fn decompose_innertilepool(&self) -> Vec<u8> {
        let mut innertiles: Vec<u8> = Vec::with_capacity(COLOURS);
        let mut innertilepool_copy = self.innertilepool;
        for _ in 0..COLOURS {
            let tiles = innertilepool_copy % 32;
            innertiles.push(tiles as u8);
            innertilepool_copy >>= 5;
        }
        return innertiles
    }

    pub fn decompose_outertilepool(&self) -> Vec<usize> {
        if self.outertilepool == 0 {
            return vec![]
        }
        let mut outertiles: Vec<usize> = Vec::with_capacity(TILEGROUPS);
        for t in 0..TILEGROUPS {
            let tilegroup = self.outertilepool & (0x7f_u64 << (7 * t as u64));
            if tilegroup == 0 {
                break
            }
            outertiles.push(tilegroup as usize >> (7 * t))
        }
        outertiles.sort();
        return outertiles
    }

    pub fn get_legal_tiles(&self, table:&Tables) -> Vec<u16> {
        let mut legaltiles: Vec<u16> = Vec::new();
        if self.innertilepool > 0 {
            let innertiles = self.decompose_innertilepool();
            for (i, &tile) in innertiles.iter().enumerate() {
                if tile == 0 {continue;}
                legaltiles.push(i as u16 + 1);
            }
        }
        if self.outertilepool == 0 {
            return legaltiles
        }
        let outertiles = self.decompose_outertilepool();
        let mut previous_tilegroup = 0;
        for &tilegroup in outertiles.iter() {
            if tilegroup == previous_tilegroup {
                continue;
            } 
            for &groupcolour in table.tilemove_encoder.iter().filter(|x| **x / 8  == tilegroup as u16) {
                legaltiles.push(groupcolour);
            }
            previous_tilegroup = tilegroup
        }
        return legaltiles
    }

    pub fn update_tilepool(&mut self, group_colour_row:u16, table:&Tables) {
        
        let group_colour = group_colour_row / 8;
        let removed_group = group_colour / 8;
        let removed_colour = group_colour % 8;
        
        if removed_group == 0 {
            self.innertilepool &= u32::MAX - 0x1f * 32_u32.pow(removed_colour as u32-1);
            return
        }
        for colour in 1..=COLOURS {
            if colour == removed_colour as usize {
                continue;
            }
            let colours = table.tilenum_encoder[5 * removed_group as usize + colour - 6] as u32;
            self.innertilepool += colours * 32_u32.pow(colour as u32 - 1);
        }

        let mut outertilegroups = self.decompose_outertilepool();
        let mut removed_index:usize=0;
         match outertilegroups.binary_search(&(removed_group as usize)) {
            Ok(index) => removed_index = index,
            Err(index) => panic!("Group not in outertile groups. Group = {}, index= {}",removed_group+1,index)
        }
        outertilegroups.remove(removed_index);
        //println!("{:?}",outertilegroups);
        self.outertilepool = 0;
        for &group in outertilegroups.iter() {
            self.outertilepool <<= 7;
            self.outertilepool += group as u64;
        }
        return

    }

}


#[derive(Debug, Clone)]
pub struct GameState {
    pub tilepool:TilePool,
    pub takenfrommiddle:bool,
    pub players:Vec<u64>
}

impl Default for GameState {
    fn default() -> Self {
        GameState {
            tilepool:TilePool::new(),
            takenfrommiddle:false,
            players:vec![0x1000u64, 0u64, 0u64, 0u64]
        }
    }
}

impl GameState {
    pub fn new(table:&Tables) -> GameState {
        let mut newgamestate: GameState = Default::default();
        let tilebag = newgamestate.tilebag(table);
        newgamestate.tilepool.generate_outer_tile_pool(tilebag, table);
        return newgamestate
    }

    pub fn available_squares(&self, playernum:usize, table:&Tables) -> u32 {
        let player = self.players[playernum];
        let rightboard = retrieve_bitsu64(&player, RIGHTBOARDSTART, RIGHTBOARDEND) as u32;
        let mut filledcolours: u32 = 0;
        for row in 0..5 {
            let tilecount = table.leftboardtiles_encoder[5*retrieve_bitsu64(&player, FILLEDTILESSTART, FILLEDTILESEND) as usize + row];
            if tilecount == 1 + row as u8 {
                continue;
            }
            if tilecount > 0 {
                let leftcolour = retrieve_bitsu64(&player, TILECOLOURSSTART + 3*row as u64, TILECOLOURSSTART + 2 + 3*row as u64) as u32;
                filledcolours += 1 << (5*row as u32 + leftcolour - 1);
                continue;
            }
            for col in 0..5 {
                if rightboard & 1 << (5 * row  + col) as u32 != 0 {
                    continue;
                }
                let right_colour = (4 * row + col) % 5;
                filledcolours += 1 << (5*row + right_colour) as u32;
            } 
        }
        return filledcolours
    }

    pub fn get_legal_moves(&self, playernum:usize, table:&Tables) -> Vec<u16> {
        let player = self.players[playernum];
        let penalties = retrieve_bitsu64(&player,PENALTIESSTART, PENALTIESEND) as u8;
        let mut legalmoves:Vec<u16> = Vec::new();
        let legaltiles = self.tilepool.get_legal_tiles(table);
        let filled_colours: u32 = self.available_squares(playernum, table);
        for &tile in legaltiles.iter() {
            let colour = tile % 8;
            if colour == 0 {
                panic!("Colour 0 detected! Tile: {}, outerpool: 0x{:x}, innerpool: 0x{:x}",tile,
            self.tilepool.outertilepool, self.tilepool.innertilepool)
            }
            for row in 0..5 {
                if filled_colours & 1 << (5*row + colour - 1) == 0 {
                    continue;
                }
                legalmoves.push(tile * 8 + row);
            }
            if penalties < MAXPENALTY {
                legalmoves.push(tile*8 + 5)
            }
        }
        
        return legalmoves
    }

    pub fn update_board(&mut self, playernum:usize, group_colour_row:u16, tilenum:u8, table:&Tables) {
        let colour_row = group_colour_row % 64;
        let colour = colour_row / 8;
        let row = (group_colour_row % 8) as usize;
        let penalties = retrieve_bitsu64(&self.players[playernum], PENALTIESSTART, PENALTIESEND);
        if row == COLOURS {
            let addedpenalties = min(tilenum as u64, MAXPENALTY as u64 - penalties);
            self.players[playernum] += addedpenalties << PENALTIESSTART;
            return
        }
        let leftboardtiles = retrieve_bitsu64(&self.players[playernum], FILLEDTILESSTART, FILLEDTILESEND);
        let current_tiles = table.leftboardtiles_encoder[5*leftboardtiles as usize + row];
        if current_tiles == 0 {
            self.players[playernum] += (colour as u64) << (TILECOLOURSSTART + 3*row as u64);
        }
        
        if current_tiles + tilenum <= row as u8 + 1 {
            self.players[playernum] += (tilenum as u64) * (table.factorials[row as usize+1] as u64) << FILLEDTILESSTART;
            return
        }
        self.players[playernum] += (1 + row as u64 - current_tiles as u64) * (table.factorials[row as usize+1] as u64) << FILLEDTILESSTART;
        let addedpenalties = min(tilenum as u64 + current_tiles as u64 - row as u64 - 1, MAXPENALTY as u64 - penalties);
        self.players[playernum] += addedpenalties << PENALTIESSTART;
        return
    }

    pub fn update_player(&mut self, group_colour_row:u16, playernum:usize, table:&Tables) {
        let group = group_colour_row / 64;
        if group == 0 && !self.takenfrommiddle {
            self.players[playernum] += 0x2_000;
            let penalties = retrieve_bitsu64(&self.players[playernum], PENALTIESSTART, PENALTIESEND);
            if penalties < MAXPENALTY as u64 {
                self.players[playernum] += 1 << PENALTIESSTART;
            }
            self.takenfrommiddle = true;
        }
        let colour = (group_colour_row % 64) / 8;
        if colour == 0 {
            panic!("Colour 0 detected! GCR: {}, outerpool: 0x{:x}, innerpool: 0x{:x}",
            group_colour_row, self.tilepool.outertilepool, self.tilepool.innertilepool)
        }
        let mut tilenum: u8 = 1;
        if group == 0 {
            tilenum = (self.tilepool.innertilepool / 32_u32.pow(colour as u32 - 1) % 32) as u8;
        } else {
            
            tilenum = table.tilenum_encoder[(5*group + colour - 6) as usize];
        }
        self.tilepool.update_tilepool(group_colour_row, table);
        self.update_board(playernum, group_colour_row, tilenum, table);

    }
    pub fn tilebag(&self, table:&Tables) -> Vec<u8> {
        let mut tilebag: Vec<u8> = vec![20,20,20,20,20];
        for player in self.players.iter() {
            let leftboardtiles = retrieve_bitsu64(player, FILLEDTILESSTART, FILLEDTILESEND);
            let leftboardcolours = retrieve_bitsu64(player, TILECOLOURSSTART, TILECOLOURSEND);
            let rightboard = retrieve_bitsu64(player, RIGHTBOARDSTART, RIGHTBOARDEND);
            for row in 0..5 {
                for col in 0..5 {
                    if rightboard & 1 << (5*row + col) == 0 {
                        continue;
                    }
                    let colour = (col + 4*row) % 5;
                    tilebag[colour] -= 1; 
                }
                let colour = retrieve_bitsu64(&leftboardcolours, 3*row as u64, 2 + 3*row as u64);
                if colour == 0 {
                    continue;
                }
                let tiles = table.leftboardtiles_encoder[5*leftboardtiles as usize + row];
                tilebag[colour as usize - 1] -= tiles; 
            }
            
        }
        return tilebag
    }
    pub fn reset(&mut self, table:&Tables) {
        
        self.takenfrommiddle = false;
        for player in self.players.iter_mut() {
            let leftboardtiles = retrieve_bitsu64(player, FILLEDTILESSTART, FILLEDTILESEND);
            for row in 0..5 {
                let tiles = table.leftboardtiles_encoder[5*leftboardtiles as usize + row];
                if tiles as usize != row + 1 {
                    continue;
                }
                let tilecolour = retrieve_bitsu64(player, TILECOLOURSSTART + 3*row as u64, 
                    TILECOLOURSSTART + 2 + 3*row as u64);
                *player -= (tiles as u64) * (table.factorials[row+1] as u64) << FILLEDTILESSTART;
                *player -= tilecolour << (TILECOLOURSSTART + 3*row as u64);
            }
            // Sets isturn to 1 if player picked up the yellow square
            *player &= u64::MAX - 0x1000;
            *player += (*player & 0x2000) / 2;
            // Resets penalties and the yellow square 
            *player &= u64::MAX - 0x2E00; 
        }
        self.tilepool.generate_outer_tile_pool(self.tilebag(table), table);
    }

    pub fn is_endstate(&self) -> bool {
        /*
            End condition when none of the players have a legal moves is handled
            separetly in the loop for the round.
         */
        return self.tilepool.innertilepool == 0 && self.tilepool.outertilepool == 0
    }

    pub fn is_lastround(&self, table:&Tables, explain:bool) -> bool {
        let end_boards: Vec<u64> = vec![0b01111, 0b10111, 0b11011, 0b11101, 0b11110];
        for (i, player) in self.players.iter().enumerate() {
            let mut rightboard = retrieve_bitsu64(player, RIGHTBOARDSTART, RIGHTBOARDEND);
            for k in 0..5 {
                let row = rightboard % 32;
                if !end_boards.contains(&row) {
                    rightboard /= 32;
                    continue;
                }
                
                let leftboardtiles = retrieve_bitsu64(player, FILLEDTILESSTART, FILLEDTILESEND);
                let tiles = table.leftboardtiles_encoder[5*leftboardtiles as usize + k];
                if explain {
                    println!("Player {} has 4/5 tiles completed on row {}, tiles {} = ",i+1,k+1,tiles);
                }
                if tiles == 1 + k as u8 {
                    return true
                }
                rightboard /= 32;
            }
        }
        return false
    }

    pub fn print_players(&self)  {
        println!("[0x{:x},0x{:x},0x{:x},0x{:x}]",
        self.players[0],self.players[1],self.players[2],self.players[3]);
        return
    }
}