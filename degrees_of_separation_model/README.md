# Research Question 
How correlated are the mean degrees of separation in a network when compared to the standard deviation
of the degrees of connection of those same nodes. I.e: in the range of [-1, 1], a strong correlation is
a coefficient whose absolute value is > 0.5. (I.e: <= -0.5 or >= 0.5).

# Test plan
Generate 1,000 random networks with 100 nodes, using a modified version of the Barbarsi-Albert method,
measure each network's mean degrees of separation and connection, then graph that data in 
a scatter chart to find the correlation coefficient of those two variables.

## Inputs
m0, m, w
## Controls
m0, m
## Independent
w --> We believe this will give us graphs with the same number of connections, same mean degree of connection but varying standard deviations of degrees of connection

