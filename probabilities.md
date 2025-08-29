Probabilities calculated assume an infinite tile pool. It also assumes a worse case
for what the other players pick.

## Probability of getting 1-5 of the same colour in a single round
Assumes a random starting position unless stated otherwise.

One colour \
1 - 1/4 SUM_{n=0->3} (4-n)nCr(9,n)p^{9-n}(1-p)^n \
Where p is the probability of a group of 4 tiles having none of the desired colour (0.8^4).

The sum is 0.96397 to 5 decimal places.