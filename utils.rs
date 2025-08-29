

pub fn retrieve_bitsu64(x:&u64, firstbit:u64, lastbit:u64) -> u64 {
    let bits: u64 = x >> firstbit;
    return bits % (1 << (lastbit + 1 - firstbit)) 
}