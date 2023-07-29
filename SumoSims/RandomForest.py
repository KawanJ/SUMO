#%%
import numpy as np
from itertools import permutations
import random
import matplotlib.pyplot as plt
#%% Creating Distance between distance
Num_city = 4
City_dist = np.array([[0,230,275,210],
                      [230,0,220,290],
                      [275,220,0,195],
                      [210,290,195,0]])

def Calculate_Dist(Sol,City_dist):
    Dist = 0
    for i in range(len(Sol)-1):
        Dist+=City_dist[Sol[i]][Sol[i+1]]
    return Dist

Solutions = list(permutations(np.array(range(Num_city))))
#%% For Graph
Y = []
X = np.array(range(len(Solutions)))
for Sol in Solutions:
    Y.append(Calculate_Dist(Sol, City_dist))
plt.plot(X,Y)
plt.show()
#%% For Hill Climbing
Best_Dist = max(Y)
Best_Sol = Solutions[0]
Episodes = 10
for e in range(Episodes):
    Initial_Sol = random.choice(Solutions)
    Initial_Ind = Solutions.index(Initial_Sol)
    Initial_Dist = Calculate_Dist(Initial_Sol, City_dist)
    while(1):
        if Initial_Ind == len(Solutions)-1: 
            break
        print(Initial_Sol, Initial_Dist)
        if Calculate_Dist(Solutions[Initial_Ind-1], City_dist) < Initial_Dist and Calculate_Dist(Solutions[Initial_Ind-1], City_dist) < Calculate_Dist(Solutions[Initial_Ind+1], City_dist):
            Initial_Sol = Solutions[Initial_Ind-1]
            Initial_Ind -= 1
            Initial_Dist = Calculate_Dist(Solutions[Initial_Ind], City_dist)
        elif Calculate_Dist(Solutions[Initial_Ind+1], City_dist) < Initial_Dist and Calculate_Dist(Solutions[Initial_Ind+1], City_dist) < Calculate_Dist(Solutions[Initial_Ind-1], City_dist):
            Initial_Sol = Solutions[Initial_Ind+1]
            Initial_Ind += 1
            Initial_Dist = Calculate_Dist(Solutions[Initial_Ind], City_dist)
        else:
            break
    if Initial_Dist<Best_Dist:
        Best_Dist = Initial_Dist
        Best_Sol = Initial_Sol
    print(Initial_Sol,Initial_Dist)
    print(Best_Dist)

print("Best Solution = ", Best_Sol, " with Distance: ", Best_Dist)
