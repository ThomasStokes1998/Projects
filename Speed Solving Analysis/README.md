# What is Speed Solving?
The goal of speed solving is to solve the Rubik's Cube (and similiar puzzles) as fast as possible. Most speed solvers are able to do this in under 20 seconds. There is an
organisation called the World Cube Association (WCA) which organises competitions in which speed solvers can compete and get official times that are posted on leaderboards.
I am a speed solver myself, and I have also been to a couple of competitions organised by the WCA. 

The WCA has a website where they show competitions (both upcoming and past ones) as well as leaderboards for the various events that are speed solved at competitions. The data for
the leaderboards is also freely able to be downloaded from their website: https://www.worldcubeassociation.org/results/misc/export.html. 
# Summary
Obviously, since I am a speed solver myself (and on the database) I am personally interested this dataset. The information in the WCA database is based on competition results 
owned and maintained by the World Cube Assocation, published at https://worldcubeassociation.org/results. 

I am interested in answering the following questions:
* How fast are competitors improving? 
* Is the rate of improvement speeding up, slowing down, remaining constant? 

As well as adding the following features:
* A relay leaderboard
* A scoring system

# Relay Leaderboard

There are 6 NxNxN puzzles that are speed solved in WCA competitions, from 2x2x2 up to 7x7x7. Solving all these puzzles in succession is called a 'Relay'. Relay's are not an
official event in the WCA but theoretical times can be calculated from the leaderboards for 2x2x2 up to 7x7x7. The Relay leaderboard I produced takes all the competitors that
have both an official single and average time in all the NxNxN events from 2x2x2 up to 7x7x7 and then sums them up to calculate their Relay times.

The score is calculated by normalising the relay times and then putting the results through a sigmoid function (takes the normalised times as inputs and outputs a number 
between 0 and 100). The full list of relay times can viewed by clicking on the WCA_Relay.csv file. \
Here is a histogram of the relay times:
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/wca_relay_single.png) 

Here are the current top 10 times:
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/wca_relay_top10.PNG)
