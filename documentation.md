# Azul Documentation

## Encodings

### Player Board (u64)
bits | description
--|--
00-08 | score
9-11 | penalties
12    | Is turn
13    | yellow square
14-23 | filled in tiles (left board)
24-38 | tile colours (left board)
39-63 | right board (5x5 square)


**Left Board: Filled In Tiles** Add k! for the kth row. \
**Left Board: Tile Colours** Add colour * 8^k for the kth row. \
**Right Board** *(column + 4xrow) mod 5* gives the square colour
and *(colour+row) mod 5* gives the column number for a given colour and row.

### Outer Tile Pool (u64)
There are 70 unique tiles. \
So 7 bits required for each of the 9 tile groups. \
Tiles are ordered by their encoding (ascending).

### Inner Tile Pool (u32)
Max for each colour = 9*3 = 27^. \
So 5 bits for each of the 5 colours.

^ In the physical version there are 20 tiles of each colour provided,
but this would still need 5 bits.

### Move (u32)
**Current**
bits | description
--|--
00-02 | 6 places on the player board (0-4 rows, 5 penalty)
03-05 | colour (1-5)
06-13 | tilegroup (0-70) (inner tile group=0)

**Retired**
bits | description
--|--
00-02 | 6 places on the player board (0-4 rows, 5 penalty)
03-05 | 5 colours
06-09 | 10 tile groups

## Functions

### PlayerBoard

**available_squares:** 0 - cannot place colour, 1 - can place colour. \
Row r occupies bits 5r..=5r+4. \
Colour c occupies bit c in the row.

### AzulEnvironment

**score:** The score is a simple way of ranking moves. \ 
It priortise tiles that complete rows, add new tiles on
columns with tiles, or have a lot of that colour.


## Game Changes

Here are any ways my emulation of Azul is different from the physical game.

* Passing if no legal moves: The rule book does not mention what to do if a player has
no legal moves. 
In my implementation the player simply passes their turn to the next player.
If no players have any legal moves then the round ends, 
even if there are tiles left.
* No-one takes from the middle: It is theoretically possible for a round to
be completed without anyone taking from the middle. This case is not covered
in the rules. If this happens then the start turn passes clockwise from the player
who started on the previous round.  