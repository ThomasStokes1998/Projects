# Summary
This project uses the results of every women's international football match -that was not a friendly- from November 1967 to June 2020, to look at how playing at home and a teams 
experience affects their performance (i.e. how often they win and how many goals they score per game). The data set I used was from https://www.kaggle.com/datasets. I decided
to analyse this dataset specifically because women's football is a sport I do not know alot about. So I thought it would be interesting to see what an outsider could learn about
the sport only using data analysis tools. \
Findings:
* Playing at home means a team is 14% more likely to win and 16% less likely to lose on average
* Playing at home does not have a statistically significant effect on how often a team draws
* Playing at home equates to about 0.2 extra goals per game
* Experience is directly correlated with more wins and fewer losses

# Home Advantage
In most sports it is considered to be an advantage for a team if they are playing at home. This makes a lot of sense: the team will be more familiar with the venue, likely more
effort will have been put in to performing well in the match since it's home losses are generally seen as worse than away losses. There are some reasons to think that this might
not be the case however. Playing at home puts extra pressure on the home team to win particularly if there is a prior expectation for them to perform well, also training more for
a match can increase performance anxiety. \
Here is a table summarising my findings:
Home? | Win% | Draw% | Loss% 
---|---|---|---
Home | 49.4 | 14.2 | 36.5
Neutral | 43.3 | 13.3 | 43.3
P-value | 7.6x10^-9 | 0.25 | 8.9x10^-12 

![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-1.png)

# Match Experience
The more you do the something, the better you get at doing said thing. This a perfectly fine qualitative assessment, however it would be nice to put some numbers to this 
principle. To do this, first I need to be able to measure how good a team is based on their results. I decided to do this by assigning every team a score based on their 
proportion of wins, draws and losses. \
The formula I used was: (3xwins + 1xdraws) / games played, the only drawback to this formula is that teams that have played only a few games, or have played most of their games 
against lower ranked teams, tend to have inaccurate scores. \
Here is a world map (I produced in Tableau) with each countries score: (the more blue a country is, the better its score)
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-6.PNG) \
Here is how the number of games affects a teams score: \
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-2.png) \
Here is how the number of games affects a teams win proportion: \
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-5.png) \
Here is how the number of games affects a teams draw proportion: \
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-4.png) \
Here is how the number of games affects a teams loss proportion: \
![](https://github.com/ThomasStokes1998/hello-world/blob/master/images/project-1-7.PNG)
