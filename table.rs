use std::fs::File;
use std::io::{Read,Result};

const UNIQUETILEGROUPS:usize = 70;
const COLOURS:usize = 5;

fn read_table(filename: &str) -> Result<Vec<u32>> {
    let mut tilegroup_encoder: Vec<u32> = Vec::with_capacity(UNIQUETILEGROUPS);
    let mut file = File::open(filename)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    for (i, &b) in buffer.iter().enumerate() {
        // First 79 bytes used for a single group of 4 tiles (index 0-69)
        // Remaining bytes for the middle tiles (values offset by 632 (79*8))
        if tilegroup_encoder.len() == UNIQUETILEGROUPS {
            /*
                Middle tile encoding do not work because computed under the
                assumption there were 8 outer tile groups instead of 9.
             */
            break
        }
        if b == 0 {
            continue;
        }
        for k in 0..8 {
            if b & 1 << k == 0 {
                continue;
            }
            tilegroup_encoder.push(8*i as u32 + k);
        }
    }
    Ok(tilegroup_encoder)
}

pub struct Tables {
    pub factorials:Vec<u16>,
    pub tilegroup_encoder:Vec<u16>,
    pub tilenum_encoder:Vec<u8>,
    pub tilemove_encoder:Vec<u16>,
    pub leftboardtiles_encoder:Vec<u8>
}

impl Default for Tables {
    fn default() -> Self {
        let tilegroup_encoderbase5 = read_table("group_table.txt").unwrap();
        let mut tilegroup_encoder:Vec<u16> = Vec::with_capacity(70);
        for &tilegroupb5 in tilegroup_encoderbase5.iter() {
            let mut newtilegroup:u32 = 0;
            let mut decodedtileb5 = 4 * tilegroupb5;
            for colour in 0..COLOURS {
                newtilegroup += (decodedtileb5 % 5) << (3*colour);
                decodedtileb5 /= 5;
            }
            tilegroup_encoder.push(newtilegroup as u16);
        }
        Tables { 
            factorials:vec![1,1,2,6,24,120,720],
            tilegroup_encoder:tilegroup_encoder, 
            tilenum_encoder:vec![],
            tilemove_encoder:vec![],
            leftboardtiles_encoder:vec![] 
        }
    }
}

impl Tables {
    pub fn new() -> Tables {
        let mut newtable: Tables = Default::default();
        newtable.generate_tables();
        return newtable
    }

    fn generate_tables(&mut self) {
        self.generate_tileencoders();
        self.leftboardtiles_encoder = self.generate_leftboardtiles();
    }

    fn generate_tileencoders(&mut self) {
        for (i, &tilegroup) in self.tilegroup_encoder.iter().enumerate() {
            for colour in 1..=COLOURS {
                let colours = (tilegroup & 7 << 3*(colour as u16-1)) / 8_u16.pow(colour as u32 - 1);
                self.tilenum_encoder.push(colours as u8);
                if colours == 0 {
                    continue;
                }
                self.tilemove_encoder.push((8*i+colour+8) as u16);
            }
        }
    }

    fn generate_leftboardtiles(&self) -> Vec<u8> {
        let mut leftboardtiles: Vec<u8> = Vec::with_capacity(720*5);
        for k in 0..720_u16 {
            let mut enc = k;
            for j in 1..=5_usize {
                let tiles = (enc % self.factorials[j+1]) / self.factorials[j];
                enc -= tiles*self.factorials[j];
                leftboardtiles.push(tiles as u8)
            }
        }
        return leftboardtiles
    }
}