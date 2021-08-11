# ELO Rankings for WCA competitors
The goal of this sub-project is to create an ELO style rating system for WCA competitors. The main ELO rankings file keeps track of every competitors ELO score. It is too large to
display on Github but it can be downloaded from the repository. You can view the competitors with the top 1000 ELO points for every WCA event.

## How are the ELO ratings calculated?
In summary: ELO points are calculated based on a competitors position in a round and the ELO rationgs of the other competitors in that round. The higher you placed 
in the round the more ELO points you gain and the higher the ELO points of the competitors you beat the more ELO points you gain. You can also lose ELO points if you perform worse 
than expected. The special thing about ELO points is that the amount of points you gain or lose is based on the relative skill level of the competitors. So losing to Felix in a 
round of 3x3x3 probably means you won't lose many ELO points unless you're Max Park.

In full: The object the algortihm modifies is a dictionary that contains all the ELO scores for all the competitors. The keys for the dictionary are the WCAID's for the 
competitors and the entry is a list that contains the competitors ELO scores. Algorithm steps:
1. For a given competition the algorithm starts by getting all the results for the competition and all the events held at that competition.  
2. Find the index numbers for each event in the competition.
3. For each event find all the rounds for this event at the competition and calculate the ELO weight based on the type of event (see below for weightings).
4. For each round, order the round based on position then loop through all the competitors in the round from best to worst.
5. For a given competitor (from now on referred to as "home") check if they are in the dictionary, if not then create a new entry into the dictionary with a list filled with "-1" 
 (default entry for home's with no official results in an event).
6. Next check if the ELO score for home in this event is -1. If so then change the ELO score to 1000 (default for first time competitors).
7. Loop through all competitors (from now on referred to as "away") below our current competitor in the list and repeat steps 5 and 6.
8. Calcualte the points needed to added and subtracted from home and away respectively (see below for formulae).
9. Add the appropiate points to home and subtract the appropiate points from away. If away's score is negative set it to zero.
10. Check if home set any national, continental or world records if so add 10, 20 or 50 points respectively.
11. Repeat steps 5-10 for every competitor in the round then repeat steps 4-10 for every round and 3-10 for every event in the competition.
12. Repeat the above steps for every competition (usually only the ones from the past week).

Weight Type | Weighting
---|---
Round 1 | 10
Round 2 | 20
Round 3 | 25
Final | 50
Other | 20
Tournament | x1.5
Worlds | x2

Home ELO = Weighting * ( 1 - 1 / (1 + e^{λ(away - home)}) ) \
Away ELO = -Weighting * 1 / (1 + e^{λ(home - away)}) ) \
Where Home ELO and Away ELO are the amounts to be added respectively, home and away are the current ELOs of the two competitors and λ is a parameter that enusres a sensible
amout of ELO is added / subtracted.
