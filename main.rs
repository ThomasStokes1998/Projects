
use std::collections::HashMap;
use std::cmp::min;
use std::env;
use std::io::stdin;
use std::time::Instant;

use crate::utils::retrieve_bitsu64;
use crate::table::Tables;
use crate::gamestate::GameState;

mod utils;
mod gamestate;
mod table;
fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let azul = AzulEnvironment::new();
    azul.play_computer(vec![4],4,15,0,
        true, false, false);
    /*let mut gamestate = GameState::new(&azul.table);
    let pruning:Vec<f32> = vec![-101.0;4];
    for x in 1..=4 {
        let starttime = Instant::now();
        _ = azul.minimax(&mut gamestate, 0, &pruning, x, 15);
        let dt = starttime.elapsed().as_millis();
        println!("Depth = {} Time = {}ms",x,dt);
        if dt >= 20_000 {
            return;
        }
    }*/
}

const COLOURS:usize = 5;
const MAXPENALTY:u8 = 7;
const PENALTYROW:[u64;8] = [0,1,2,4,6,8,11,14];
const ROWPOINTS:f32 = 2.0;
const COLUMNPOINTS:f32 = 7.0;
const COLOURPOINTS:f32 = 10.0;
const MAXTURNS:u8 = 1 + 9*4;
const ROWPROB:[f32;5] = [0.9, 0.8, 0.6, 0.5, 0.4];
// Player board sections
//const SCORESTART:u64 = 0;
const SCOREEND:u64 = 8;
const PENALTIESSTART:u64 = 9;
const PENALTIESEND:u64 = 11;
const ISTURNSTART:u64 = 12;
//const ISTURNEND:u64 = 12;
const YELLOWSQUARESTART:u64 = 13;
//const YELLOWSQUAREEND:u64 = 13;
const FILLEDTILESSTART:u64 = 14;
const FILLEDTILESEND:u64 = 23;
const TILECOLOURSSTART:u64 = 24;
const TILECOLOURSEND:u64 = 38;
const RIGHTBOARDSTART:u64 = 39;
const RIGHTBOARDEND:u64 = 63;



fn print_help() {
    println!("Moves need to be inputted in this format: group,colour,row.");
    println!("The group is where you take the tile(s) from. It is a number from 0 to 70.");
    println!("Type 0 if you would like to take from the middle.");
    println!("Type 1-70 if you would like to take from the respective outer tile group.");
    println!("Colour is a number from 1-5.");
    println!("Colour 1 is the tile colour in the top left of the 5x5 board. Colour 2 is the colour to the right etc.");
    println!("Row is a number from 1-6.");
    println!("Numbers 1-5 represent placing it on the row with the corresponding number of tiles needed to fill the row.");
    println!("Type 6 for penalties.");
    println!("Example: 43,3,2 would mean take the colour 3 tiles from group 43 and place them on row 2.");
}

fn normalise_vec(v:Vec<f32>) -> Vec<f32> {
    let mut norm_vec: Vec<f32> = Vec::with_capacity(v.len());
    let mut first: f32 = 0.0;
    let mut second: f32 = 0.0;
    for &x in v.iter() {
        if x <= second {
            continue;
        }
        if x > first {
            second = first;
            first = x;
        } else {
            second = x;
        }
    }
    for &x in v.iter() {
        if x == first {
            norm_vec.push(x - second);
        } else {
            norm_vec.push(x - first);
        }
    }
    return norm_vec
}
fn binom(n:u8, k:u8) -> f32 {
    if n < k {
        return 0.0
    }
    if k == 0 || n == k {
        return 1.0
    }
    if k == 1 || n == k-1 {
        return n as f32
    }
    return (n as f32) * (n as f32 - 1.0) / 2.0
}
fn weighted_mean(vals:Vec<u64>, weights:Vec<u64>) -> f32 {
    if vals.len() != weights.len() {
        println!("Vals ({}) and  Weights ({}) different lengths.",
        vals.len(),weights.len());
        return 0.0
    }
    let denom:u64 = weights.iter().sum();
    if denom == 0 {
        return 0.0
    }
    let mut numerator:u64 = 0;
    for (i, &xi) in vals.iter().enumerate() {
        let wi = weights[i];
        numerator += wi*xi
    } 
    return (numerator as f32) / (denom as f32)
}

fn prob_aorb(a:f32, b:f32) -> f32 {
    // Assumes events A and B are independent.
    return a + b - a*b
}



fn prob_or(u:Vec<f32>) -> f32 {
    if u.len() == 0 {
        return 0.0
    }
    if u.len() == 1 {
        return u[0]
    }
    if u.len() == 2 {
        return prob_aorb(u[0], u[1])
    }
    let mut p: f32 = u[0];
    for (i, &b) in u.iter().enumerate() {
        if i < 2 {
            continue;
        }
        p = prob_aorb(p, b);
    }
    return p
}

fn prob_agivenr(a:f32, n:u8, r:u8) -> f32 {
    if n == 0 {
        return 1.0
    }
    if n == r {
        return a.powi(r as i32)
    }
    let mut p:f32 = 0.0;
    let b = 1.0 - a;
    for k in n..=r {
        p += binom(r, k) * (a.powi(k as i32)) * (b.powi((r-k) as i32))
    }
    return p
}

fn prob_tiles(tilenums:Vec<u8>,r:u8) -> f32 {
    let mut p:f32 = 1.0;
    for (row, &tiles) in tilenums.iter().enumerate() {
        if tiles > r {
            return 0.0
        }
        if tiles == 0 {
            continue;
        }
        p *= prob_agivenr(ROWPROB[row], tiles, r);
    }
    return p
}



fn estimate_rounds_remaining(player:&u64) -> u8 {
    let rightboard = retrieve_bitsu64(&player, RIGHTBOARDSTART, RIGHTBOARDEND);
    let mut rounds_remaining: u8 = 5;
    let mut emptytilecount: u8 = 0;
    for k in 0..25 {
        if rightboard & 1 << k == 0 {
            emptytilecount += 1
        }
        if k % 5 == 4 {
            if rounds_remaining > emptytilecount {
                rounds_remaining = emptytilecount;
            }
            emptytilecount = 0;
        }
    }
    return rounds_remaining
}

fn score_row(rightboard:&u64, row:u64, colour:u64) -> u64 {
    let mut horizontalscore: u64 = 1;
    let x = (row + colour - 1) % 5;
    let square = 5*row + x;
    let mut posx: bool = true;
    let mut negx: bool = true;
    for d in 1..5 {
        if !(posx || negx) {
            break;
        }
        if x + d >= 5 {
            posx = false;
        }
        if posx {
            if rightboard & 1 << (square + d) == 0 {
                posx = false;
            } else {
                horizontalscore += 1
            }
        }
        if x < d {
            negx = false;
        }
        if negx {
            if rightboard & 1 << (square - d) == 0 {
                negx = false;
            } else {
                horizontalscore += 1
            }
        }
    }
    let mut verticalscore: u64 = 1;
    let mut posy: bool = true;
    let mut negy: bool = true;
    for d in 1..5 {
        if !(posy || negy) {
            break;
        }
        if row + d >= 5 {
            posy = false;
        }
        if posy {
            if rightboard & 1 << (square + 5*d) == 0 {
                posy = false;
            } else {
                verticalscore += 1
            }
        }
        if row < d {
            negy = false;
        }
        if negy {
            if rightboard & 1 << (square - 5*d) == 0 {
                negy = false;
            } else {
                verticalscore += 1
            }
        }
    }
    if horizontalscore == 1 {
        return verticalscore
    }
    if verticalscore == 1 {
        return horizontalscore
    }
    return horizontalscore + verticalscore
}

fn lastround_bonuses(rightboard:&u64, explain:bool) -> u64 {
    let mut bonus:u64 = 0;
    let mut rows:[bool;5] = [true;5];
    let mut cols:[bool;5] = [true;5];
    let mut clrs:[bool;5] = [true;5];
    for square in 0..25 {
        let row = square / 5;
        let col = square % 5;
        let clr =(col + 4*row) % 5; 
        if !rows[row] && !cols[col] && !clrs[clr] {
            continue;
        }
        if rightboard & 1 << square == 0 {
            rows[row] = false;
            cols[col] = false;
            clrs[clr] = false;
        }
    }
    for k in 0..5 {
        if rows[k] {
            if explain {
                println!("+{:.0} for completing row {}",ROWPOINTS,k+1);
            }
            bonus += ROWPOINTS as u64;
        }
        if cols[k] {
            if explain {
                println!("+{:.0} for completing column {}",COLUMNPOINTS,k+1);
            }
            bonus += COLUMNPOINTS as u64;
        }
        if clrs[k] {
            if explain {
                println!("+{:.0} for completing colour {}",COLOURPOINTS,k+1);
            }
            bonus += COLOURPOINTS as u64;
        }
    }
    return bonus
}

fn score_board(player:u64, lastround:bool, table:&Tables, explain:bool) -> u64 {
    let mut score:u64 = 0;
    let mut newplayer = player;
    let leftboardtiles = retrieve_bitsu64(&player, FILLEDTILESSTART, FILLEDTILESEND);
    let mut rightboard = retrieve_bitsu64(&player, RIGHTBOARDSTART, RIGHTBOARDEND);
    for row in 0..5 {
        let tiles = table.leftboardtiles_encoder[5*leftboardtiles as usize + row];
        if tiles < 1 + row as u8 {
            continue;
        }
        let colour = retrieve_bitsu64(&player, TILECOLOURSSTART + 3*row as u64, TILECOLOURSSTART + 2  + 3*row as u64);
        if explain {
            println!("+{} for row {}",score_row(&rightboard, row as u64, colour),row+1)
        }
        score += score_row(&rightboard, row as u64, colour);
        let square = 5*row as u64 + (row as u64 + colour - 1) % 5;
        rightboard += 1 << square;
        newplayer += 1 << (square + RIGHTBOARDSTART);
        newplayer -= (tiles as u64) * (table.factorials[row + 1] as u64) << FILLEDTILESSTART;
        newplayer -= colour << (TILECOLOURSSTART + 3*row as u64);
    }
    if lastround {
        score += lastround_bonuses(&rightboard, explain);
    }
    let penalties = retrieve_bitsu64(&player, PENALTIESSTART, PENALTIESEND);
    let point_deduction = PENALTYROW[penalties as usize];
    newplayer += score;
    if newplayer % (1 << SCOREEND) <= point_deduction {
        if explain && point_deduction > 0 {
            println!("-{} from penalties",newplayer % (1 << SCOREEND));
        }
        return newplayer - (newplayer % (1 << SCOREEND))
    }
    if explain && point_deduction > 0 {
        println!("-{} from penalties",point_deduction);
    }
    return newplayer - point_deduction
}

fn generate_boards(rounds_remaining:u8, tolerance:f32, lefttiles:[u8;5]) -> HashMap<u16,f32> {
    let mut boards: HashMap<u16,f32> = HashMap::new();
    boards.insert(0, 1.0);
    for row in 0..5 {
        let a = ROWPROB[row];
        let b = 1.0 - a;
        let c = ROWPROB[row-lefttiles[row] as usize];
        let d = 1.0 - c;
        let mut newboards: HashMap<u16,f32> = HashMap::new();
        for &rp in boards.keys() {
            let p = boards[&rp];
            for t in 0..=rounds_remaining {
                let mut q = p * binom(rounds_remaining, t);
                if lefttiles[row] > 0 {
                    if t == 0 {
                        q *= d * b.powi((rounds_remaining-t-1) as i32);
                    } else {
                        q *= c * a.powi(t as i32 - 1) * b.powi((rounds_remaining-t) as i32);
                    }
                    
                } else {
                    q *= a.powi(t as i32) * b.powi((rounds_remaining-t) as i32);
                }
                if q <= tolerance {
                    continue;
                }
                newboards.insert(rp + ((t as u16) << 3*row),q);
            }
        }
        boards = newboards;
    }
    return boards
}

fn expected_bonuses(rightboard:&u64, leftcolours:[u8;5], rounds_remaining:u8,
    boards:HashMap<u16,f32>) -> f32 {
    let mut exp_bonus:f32 = 0.0;
    let mut boardskeys:Vec<u16> = Vec::with_capacity(boards.keys().len());
    for &rp in boards.keys() {
        let idx = boardskeys.partition_point(|&x| x <= rp);
        boardskeys.insert(idx, rp);
    }
    for row in 0..5 {
        for t in 0..=rounds_remaining {

        }
    }
    /*
        Recursively update hashmap. 
        Check if rp in boards.
        Evaluate boards along the way, and then remove from boardskeys.
     */
    return exp_bonus
}



struct AzulEnvironment {
    table:Tables
}

impl Default for AzulEnvironment {
    fn default() -> Self {
        AzulEnvironment { 
            table:Tables::new() 
        }
    }
}

impl AzulEnvironment {
    fn new() -> AzulEnvironment {
        return Default::default();
    }

    fn score_player(&self, group_colour_row:u16, gamestate:&GameState, playernum:usize, rounds_remaining:u8) -> f32 {
        let colour = (group_colour_row % 64) / 8;
        let group = group_colour_row / 64;
        let mut tilenum: u8 = 1;
        let player = gamestate.players[playernum];
        if group == 0 {
            tilenum = ((gamestate.tilepool.innertilepool / 32_u32.pow(colour as u32 - 1)) % 32) as u8;
        } else {
            tilenum = self.table.tilenum_encoder[(5*group + colour - 6) as usize];
        }       
        
        let row = group_colour_row % 8;
        let current_penalties = retrieve_bitsu64(&player, PENALTIESSTART, PENALTIESEND);
        if row == COLOURS as u16 {
            let new_penalties = min(MAXPENALTY as u64, current_penalties + tilenum as u64);
            let point_deduction = PENALTYROW[new_penalties as usize] - PENALTYROW[current_penalties as usize];
            return - (point_deduction as f32)
        }
        
        let mut score: f32 = 0.0;
        let leftboardtiles = retrieve_bitsu64(&player, FILLEDTILESSTART, FILLEDTILESEND) as usize;
        let rightboard = retrieve_bitsu64(&player, RIGHTBOARDSTART, RIGHTBOARDEND);
        let rowtiles = self.table.leftboardtiles_encoder[5*leftboardtiles + row as usize];
        let appliedtiles = min(1 + row as u8 - rowtiles, tilenum);
        // Row points
        let mut rowtiles_remaining: u8 = 0;
        for k in 0..5 {
            if rightboard & 1 << (5*row + k) == 0 {
                rowtiles_remaining += 1;
            }
        }
        if rowtiles_remaining <= rounds_remaining {
            score += ROWPOINTS / (rowtiles_remaining as f32);
        }
        // Column Points
        let col = (row + colour - 1) % 5;
        let leftboardcolours = retrieve_bitsu64(&player, TILECOLOURSSTART, TILECOLOURSEND);
        let mut coltilesremaining:f32 = 15.0;
        for k in 0..5 {
            if k == row {
                coltilesremaining -= rowtiles as f32;
                continue;
            }
            if rightboard & 1 << col + 5*k != 0 {
                coltilesremaining -= k as f32;
                continue;
            }
            let rowcolour = retrieve_bitsu64(&leftboardcolours, 3*k as u64, 3*k as u64 + 2);
            if rowcolour != 0 && (k + 4*(rowcolour as u16) - 1) % 5 == col {
                coltilesremaining -= self.table.leftboardtiles_encoder[5*leftboardtiles + k as usize] as f32;
            }
        }
        score += COLUMNPOINTS * (appliedtiles as f32) / coltilesremaining;
        // Colour points
        let mut colourtilesremaining:f32 = 15.0;
        for k in 0..5 {
            if k == row {
                colourtilesremaining -= rowtiles as f32;
                continue;
            }
            if rightboard & 1 << col + 5*k != 0 {
                colourtilesremaining -= k as f32;
                continue;
            }
            let rowcolour = retrieve_bitsu64(&leftboardcolours, 3*k as u64, 3*k as u64 + 2);
            if rowcolour as u16 == colour {
                colourtilesremaining -= self.table.leftboardtiles_encoder[5*leftboardtiles + k as usize] as f32;
            }
        }

        score += COLOURPOINTS * (appliedtiles as f32) / colourtilesremaining;
        score += score_row(&rightboard, row as u64, colour as u64) as f32;
        
        if appliedtiles + rowtiles == (1 + row as u8) {
            score += (rounds_remaining as f32 - 1.0)*(rounds_remaining as f32)/2.0;
        }
        if tilenum + rowtiles <= (1 + row as u8) {
            return score
        }
        let excesstiles = tilenum - appliedtiles;
        let new_penalties = min(MAXPENALTY as u64, excesstiles as u64 + current_penalties);
        let point_deduction = PENALTYROW[new_penalties as usize] - PENALTYROW[current_penalties as usize];
        return score - (point_deduction as f32)
    }

    fn expected_bonus_score(&self, player:&u64, rounds_remaining:u8) -> f32 {
        // Function assumes it is the end of a round
        let mut expected_points:f32 = 0.0;
        let leftboardtiles = retrieve_bitsu64(player, FILLEDTILESSTART, FILLEDTILESEND) as usize;
        let leftboardcolours = retrieve_bitsu64(player, TILECOLOURSSTART, TILECOLOURSEND);
        let rightboard = retrieve_bitsu64(player, RIGHTBOARDSTART, RIGHTBOARDEND);
        let mut lefttiles:[u8;5] = [0;5];
        let mut leftcolours:[u8;5] = [0;5];
        for row in 0..5 {
            let tiles = self.table.leftboardtiles_encoder[5*leftboardtiles + row];
            lefttiles[row] = tiles;
            let colour = retrieve_bitsu64(&leftboardcolours, 3*row as u64, 2 + 3*row as u64);
            leftcolours[row] = colour as u8;
        }
        
        return expected_points
    }

    fn evaluate_gamestate_scoreonly(&self, gamestate:&GameState) -> Vec<f32> {
        let mut evals: Vec<f32> = vec![0.0, 0.0, 0., 0.0];
        let lastround = gamestate.is_lastround(&self.table, false);
        let mut r = 4;
        for player in gamestate.players.iter() {
            r = min(r, estimate_rounds_remaining(player));
        }
        for (i, player) in gamestate.players.iter().enumerate() {
            evals[i] += (player % (1 << SCOREEND)) as f32;
            let rightboard = retrieve_bitsu64(player, RIGHTBOARDSTART, RIGHTBOARDEND);
            evals[i] += lastround_bonuses(&rightboard, false) as f32;
            for k in 0..25 {
                if rightboard & 1 << k == 0 {
                    continue;
                }
                evals[i] += 5.0
            }
            if r == 1 || lastround {
                continue;
            }
            if player & (1 << YELLOWSQUARESTART) != 0 {
                evals[i] += 2.0;
            }
        }
        return evals
    }

    fn highest_scoring_move(&self, legalmoves:Vec<u16>, gamestate:&GameState, playernum:usize) -> u16 {
        let mut bestmove:u16 = 0;
        let mut besteval:f32 = -101.0;
        let rounds_remaining = estimate_rounds_remaining(&gamestate.players[playernum]);
        for &group_colour_row in legalmoves.iter() {
            if group_colour_row % 8 == COLOURS as u16 && besteval >= 0.0 {
                continue;
            }
            let moveeval = self.score_player(group_colour_row, gamestate, 
                playernum, rounds_remaining);
            if moveeval > besteval {
                besteval = moveeval;
                bestmove = group_colour_row;
            }
        }
        return bestmove
    }
    
    fn rank_moves(&self, legalmoves:Vec<u16>, gamestate:&GameState, playernum:usize) -> Vec<u16> {
        let mut ranked_moves: Vec<u16> = Vec::with_capacity(legalmoves.len());
        let mut move_evals: Vec<f32> = Vec::with_capacity(legalmoves.len());
        let rounds_remaining = estimate_rounds_remaining(&gamestate.players[playernum]);
        for &gcr in legalmoves.iter() {
            let eval = self.score_player(gcr, gamestate, playernum, rounds_remaining);
            if ranked_moves.len() == 0 {
                ranked_moves.push(gcr);
                move_evals.push(eval);
                continue;
            }
            let idx = move_evals.partition_point(|&x| x > eval);
            ranked_moves.insert(idx, gcr);
            move_evals.insert(idx, eval);
        }
        //ranked_moves.reverse();
        return ranked_moves
    }

    fn simulate_round(&self, gamestate:&GameState, playernum:usize) -> (GameState, bool) {
        let mut sim_gamestate = gamestate.clone();
        let mut currentplayernum: usize = playernum;
        let mut turncounter: u8 = 0;
        let mut turns_skipped: u8 = 0;
        //self.print_outertilepool(&sim_gamestate);
        //println!("Tile Bag : {:?}",sim_gamestate.tilebag(&self.table));
        //sim_gamestate.print_players();
        while turns_skipped < 4 && turncounter < MAXTURNS && !sim_gamestate.is_endstate() {
            //println!("Turn = {} Outertile Group = {:x}",turncounter,sim_gamestate.tilepool.outertilepool);
            let legalmoves = sim_gamestate.get_legal_moves(currentplayernum, &self.table);
            if legalmoves.len() == 0 {
                // println!("innerpool = {:x}, outertilepool = {:x}", sim_gamestate.tilepool.innertilepool, sim_gamestate.tilepool.outertilepool);
                turncounter += 1;
                currentplayernum += 1;
                currentplayernum %= 4;
                turns_skipped += 1;
                continue;
            }
            if turns_skipped > 0 {
                turns_skipped = 0;
            }
            let bestmove = self.highest_scoring_move(legalmoves, &sim_gamestate, currentplayernum);
            //self.print_move(bestmove, &sim_gamestate, currentplayernum);
            sim_gamestate.update_player(bestmove, currentplayernum, &self.table);
            turncounter += 1;
            currentplayernum += 1;
            currentplayernum %= 4;
        }
        if turncounter >= MAXTURNS {
            panic!("Turn counter hit limit of {} turns. innerpool = {:x}, outertilepool = {:x}", 
            MAXTURNS, sim_gamestate.tilepool.innertilepool, sim_gamestate.tilepool.outertilepool);
        }

        let lastround = sim_gamestate.is_lastround(&self.table, false);
        for player in sim_gamestate.players.iter_mut() {
            *player = score_board(*player, lastround, &self.table, false);
        }
        //let mut scores:Vec<u8> = Vec::with_capacity(4);
        //for &player in sim_gamestate.players.iter() {
        //    scores.push((player % 0x200) as u8);
        //}
        //sim_gamestate.print_players();
        //println!("End of Round scores = {:?}", scores);
        // sim_gamestate.print_players();
        return (sim_gamestate, lastround)
    }

    fn minimax_chasefirst(&self, gamestate:&GameState, rankedmoves:Vec<u16>, playernum:usize, pruning:&Vec<f32>, 
        depth:u8, maxnodes:usize) -> Vec<f32> {
        let mut eval:Vec<f32> = vec![-101.0;4];
        if depth == 0 || gamestate.is_endstate() {
            let roundinfo = self.simulate_round(gamestate, playernum);
            eval = self.evaluate_gamestate_scoreonly(&roundinfo.0);
            return normalise_vec(eval)
        }
        let mut newpruning: Vec<f32> = pruning.clone();
        for (i, &gcr) in rankedmoves.iter().enumerate() {
            if i >= maxnodes {
                break
            }
            let mut newgamestate = gamestate.clone();
            newgamestate.update_player(gcr, playernum, &self.table);
            let legalmoves = newgamestate.get_legal_moves(playernum, &self.table);
            let rankedmoves = self.rank_moves(legalmoves, gamestate, playernum);
            let neweval = self.minimax_chasefirst(&newgamestate, rankedmoves, (playernum+1)%4, 
            &newpruning,depth-1, maxnodes);
            if neweval[playernum] <= eval[playernum] {
                continue;
            }
            eval = neweval;
            newpruning[playernum] = eval[playernum];
            for p in 0..4 {
                if p == playernum {
                    continue;
                }
                if (eval[playernum] >= 0.0 || pruning[p] >= 0.0) && eval[playernum] + pruning[p] >= 0.0 {
                    break
                } 
            }
            
        }
        return eval
    }

    fn minimax_bestscore(&self, gamestate:&GameState, rankedmoves:Vec<u16>, playernum:usize, 
        depth:u8, maxnodes:usize) -> Vec<f32> {
        let mut eval:Vec<f32> = vec![-101.0;4];
        if depth == 0 || gamestate.is_endstate() {
            let roundinfo = self.simulate_round(gamestate, playernum);
            eval = self.evaluate_gamestate_scoreonly(&roundinfo.0);
            return eval
        }
        for (i, &gcr) in rankedmoves.iter().enumerate() {
            if i >= maxnodes {
                break
            }
            let mut newgamestate = gamestate.clone();
            newgamestate.update_player(gcr, playernum, &self.table);
            let legalmoves = newgamestate.get_legal_moves(playernum, &self.table);
            let rankedmoves = self.rank_moves(legalmoves, gamestate, playernum);
            let neweval = self.minimax_bestscore(&newgamestate, rankedmoves, (playernum+1)%4, 
            depth-1, maxnodes);
            if neweval[playernum] <= eval[playernum] {
                continue;
            }
            eval = neweval;
        }
        return eval
    }
    fn minimax_worsecase(&self, gamestate:&GameState, rankedmoves:Vec<u16>, playernum:usize, 
        minplayer:usize, pruning:&Vec<f32>, depth:u8, maxnodes:usize) -> Vec<f32> {
        let mut eval:Vec<f32> = vec![-101.0;4];
        if depth == 0 || gamestate.is_endstate() {
            let roundinfo = self.simulate_round(gamestate, playernum);
            eval = self.evaluate_gamestate_scoreonly(&roundinfo.0);
            return normalise_vec(eval)
        }
        let mut newpruning: Vec<f32> = pruning.clone();
        for (i, &gcr) in rankedmoves.iter().enumerate() {
            if i >= maxnodes {
                break
            }
            let mut newgamestate = gamestate.clone();
            newgamestate.update_player(gcr, playernum, &self.table);
            let legalmoves = newgamestate.get_legal_moves(playernum, &self.table);
            let rankedmoves = self.rank_moves(legalmoves, gamestate, playernum);
            let neweval = self.minimax_worsecase(&newgamestate, rankedmoves, (playernum+1)%4, 
            minplayer,&newpruning,depth-1, maxnodes);
            if playernum == minplayer && neweval[playernum] <= eval[playernum] {
                continue;
            }
            if playernum != minplayer && -neweval[minplayer] <= eval[playernum] {
                continue;
            }
            eval = neweval;
            if playernum == minplayer {
                newpruning[playernum] = eval[minplayer];
            } else {
                newpruning[playernum] = -eval[minplayer];
            }
            for p in 0..4 {
                if p == playernum {
                    continue;
                }
                if (eval[playernum] >= 0.0 || pruning[p] >= 0.0) && eval[playernum] + pruning[p] >= 0.0 {
                    break
                } 
            }
            
        }
        return eval
    }

    fn ida(&self, gamestate:&GameState, maxdepth:u8, playernum:usize, maxnodes:usize,
    minimaxsetting:u8) -> (u16, Vec<f32>) {
        let legalmoves= gamestate.get_legal_moves(playernum, &self.table);
        let mut rankedmoves: Vec<u16> = self.rank_moves(legalmoves, gamestate, playernum);
        let mut vals: Vec<f32> = Vec::with_capacity(rankedmoves.len());
        let mut newrankedmoves:Vec<u16> = Vec::with_capacity(rankedmoves.len());
        let mut bestmove = rankedmoves[0];
        let mut besteval: Vec<f32> = Vec::with_capacity(4);
        for d in 0..maxdepth {
            let mut pruning = vec![-101.0_f32;4];
            for (i, &m) in rankedmoves.iter().enumerate() {
                if i == maxnodes {
                    break;
                }
                let mut newgamestate = gamestate.clone();
                newgamestate.update_player(m, playernum, &self.table);
                let legalmoves = newgamestate.get_legal_moves((playernum+1)%4, &self.table);
                let rankedmovesm = self.rank_moves(legalmoves, &newgamestate, (playernum+1)%4);
                if minimaxsetting == 0 {
                    let eval = self.minimax_chasefirst(&newgamestate, rankedmovesm, 
                    (playernum+1)%4, &pruning, d, maxnodes);
                    let idx = vals.partition_point(|&x| x > eval[playernum]);
                    vals.insert(idx, eval[playernum]);
                    newrankedmoves.insert(idx, m);
                    if eval[playernum] > pruning[playernum] {
                        pruning = eval
                    }
                } else if minimaxsetting == 1 {
                    let eval = self.minimax_bestscore(&newgamestate, rankedmovesm, 
                    (playernum+1)%4, maxdepth-1, maxnodes);
                    let idx = vals.partition_point(|&x| x > eval[playernum]);
                    vals.insert(idx, eval[playernum]);
                    newrankedmoves.insert(idx, m);
                    if eval[playernum] > pruning[playernum] {
                        pruning = eval
                    
                    }
                } else if minimaxsetting == 2 {
                    let eval = self.minimax_worsecase(&newgamestate, rankedmovesm, 
                    (playernum+1)%4, playernum, &pruning, d, maxnodes);
                    let idx = vals.partition_point(|&x| x > eval[playernum]);
                    vals.insert(idx, eval[playernum]);
                    newrankedmoves.insert(idx, m);
                    if eval[playernum] > pruning[playernum] {
                        pruning = eval
                    
                    }
                } else {
                    println!("minimax setting must be 0,1,2.");
                    break
                }
            }
            besteval = pruning;
            rankedmoves = newrankedmoves;
            bestmove = rankedmoves[0];
            if minimaxsetting == 1 { 
                break;
            }
            vals = Vec::with_capacity(rankedmoves.len());
            newrankedmoves = Vec::with_capacity(rankedmoves.len());
        }
        return (bestmove, besteval)
    }

    fn play_computer(&self, humanplayers:Vec<usize>, depth:u8, 
        maxnodes:usize,minimaxsetting:u8,
    explain_score:bool, explain_lastround:bool, showeval:bool) {
        let pruning = vec![-101.0_f32;4];
        let mut gamestate = GameState::new(&self.table);
        let mut lastround = gamestate.is_lastround(&self.table,false);
        let mut turns_skipped: u8 = 0;
        let mut currentplayer = 0;
        while !lastround {
            self.print_outertilepool(&gamestate);
            gamestate.print_players();
            // Round
            while !gamestate.is_endstate() && turns_skipped < 4 {
                let legalmoves = gamestate.get_legal_moves(currentplayer, &self.table);
                if legalmoves.len() == 0 {
                    turns_skipped += 1;
                    currentplayer += 1;
                    currentplayer %= 4;
                    continue;
                } else {
                    turns_skipped = 0;
                }
                // Human Player
                if humanplayers.contains(&currentplayer) {
                    let gcr = self.human_input(currentplayer, &gamestate, &legalmoves);
                    if gcr == 0 {
                        return
                    }
                    gamestate.update_player(gcr, currentplayer, &self.table);
                }
                // Computer Player 
                else {
                    let starttime = Instant::now();
                    let gcrinfo = self.ida(&gamestate, depth, 
                        currentplayer, maxnodes, minimaxsetting);
                    self.print_move(gcrinfo.0, &gamestate, currentplayer,
                    starttime.elapsed().as_millis());
                    if showeval {
                        println!("Player {} Eval: {:?}",currentplayer+1,gcrinfo.1);
                    }
                    gamestate.update_player(gcrinfo.0, currentplayer, &self.table);
                }
                currentplayer += 1;
                currentplayer %= 4
            }
            // Reset 
            turns_skipped = 0;
            lastround = gamestate.is_lastround(&self.table,explain_lastround);
            for (i,player) in gamestate.players.iter_mut().enumerate() {
                if explain_score {
                    println!("Player {}",i+1)
                }
                *player = score_board(*player, lastround, &self.table,explain_score);
            }
            for (i, &player) in gamestate.players.iter().enumerate() {
                println!("Player {} | {} points.",i+1,player % (1 << SCOREEND));
            }
            if lastround {
                
                return
            }
            let tilebag = gamestate.tilebag(&self.table);
            if tilebag.iter().sum::<u8>() < 36 {
                println!("Game ended because less than 36 tiles left in the bag: {:?}",tilebag);
                return
            }
            gamestate.reset(&self.table);
            currentplayer += 1;
            currentplayer %= 4;
            for (i, &player) in gamestate.players.iter().enumerate() {
                if player & 1 << ISTURNSTART != 0 {
                    currentplayer = i;
                }
            }
        }
            
    }

    fn valid_humaninput(&self, stringinput:&String, legalmoves:&Vec<u16>) -> u16 {
        if stringinput.len() == 0 {
            return 0
        }
        let nums: Vec<&str> = stringinput.split(",").collect();
        if nums.len() != 3 {
            println!("Expected 3 numbers found {}.",nums.len());
            return 0
        }
        let mut y: u16 = 0;
        for (i,&num) in nums.iter().enumerate() {
            y *= 8;
            let x:u16 = match num.trim().parse() {
                Ok(n) => n,
                Err(_) => {
                    println!("Could not interpret as u16.");
                    return 0
                }
            };
            if i == 0 && x > 70 {
                println!("Group must be between 0 and 70.");
                return 0
            }
            if i == 1 && (x < 1 || x > 5) {
                println!("Colour must be between 1 and 5.");
                return 0
            }
            if i == 2 && (x < 1 || x > 6) {
                println!("Row must be between 1 and 6.");
                return 0
            }
            if i < 2 {
                y += x
            } else {
                y += x-1
            }
        }
        if !legalmoves.contains(&y) {
            println!("Inputted move is not legal!");
            return 0
        }
        return y
    }
    fn human_input(&self, currentplayer:usize, gamestate:&GameState, legalmoves:&Vec<u16>) -> u16 {
        println!("Type end to stop the program.");
        println!("Type tilepool to print out the the outer and inner tilepool.");
        println!("Type help to see how to input a move.");
        let mut stringinput: String = String::new();
        while self.valid_humaninput(&stringinput, legalmoves) == 0 {
            stringinput = "".to_string();
            println!("Enter Player {}'s move below:",currentplayer+1);
            stdin().read_line(&mut stringinput).expect("Could not read input!");
            if stringinput.trim().to_lowercase() == "end" {
                self.print_outertilepool(gamestate);
                println!("ITP (0x{}) = {:?}",gamestate.tilepool.innertilepool,
                gamestate.tilepool.decompose_innertilepool());
                gamestate.print_players();
                return 0
            }
            if stringinput.trim() == "tilepool" {
                self.print_outertilepool(gamestate);
                println!("ITP (0x{}) = {:?}",gamestate.tilepool.innertilepool,
                gamestate.tilepool.decompose_innertilepool());
                println!("Type help to see how to input a move.");
                stringinput = "".to_string();
                continue;
            }
            if stringinput.trim() == "help" {
                print_help();
                println!("Type tilepool to print out the outer and inner tilepool.");
                stringinput = "".to_string();
                continue;
            }
            if self.valid_humaninput(&stringinput, legalmoves) != 0 {
                let m = self.valid_humaninput(&stringinput, legalmoves);
                self.print_move(m, gamestate, currentplayer, 0);
                println!("Are you sure you want to play this move? (y/n)");
                let mut yesno = String::new();
                stdin().read_line(&mut yesno).expect("Could not read input!");
                if yesno.trim().to_lowercase() == "y" {
                    return self.valid_humaninput(&stringinput, legalmoves)
                }
                stringinput = "".to_string();
            }
        }
        return self.valid_humaninput(&stringinput, legalmoves)
    }
    fn print_move(&self, group_colour_row:u16, gamestate:&GameState, playernum:usize,
    time_elapsed:u128) {
        let group = group_colour_row / 64;
        let colour = (group_colour_row % 64) / 8;
        let row = group_colour_row % 8;
        if group == 0 {
            let innertilepool = gamestate.tilepool.decompose_innertilepool();
            let tiles = innertilepool[colour as usize - 1];
            println!("Player {} took {} tiles (colour={}) from the middle and placed them on row {}. {} ms",
        playernum+1, tiles, colour, row+1,time_elapsed);
        return
        }
        let tiles = self.table.tilenum_encoder[(5*group + colour - 6) as usize];
        println!("Player {} took {} tiles (colour={}) from group {} and placed them on row {}. {} ms",
        playernum+1, tiles, colour, group, row+1, time_elapsed);
        return
    }

    fn print_outertilepool(&self, gamestate:&GameState) {
        let outertilepool = gamestate.tilepool.decompose_outertilepool();
        println!("Starting Tiles: 0x{:x}", gamestate.tilepool.outertilepool);
        for (i, &tilegroup) in outertilepool.iter().enumerate() {
            let mut groupbreakdown: Vec<u8> = Vec::with_capacity(5);
            for c in 0..5 {
                let tiles = self.table.tilenum_encoder[(5*tilegroup + c - 5) as usize];
                groupbreakdown.push(tiles);
            }
            println!("Tilegroup {}: {:?}",tilegroup, groupbreakdown);
        }
        return
    }

}






