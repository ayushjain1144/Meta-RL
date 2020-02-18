import random
from dataclasses import dataclass

@dataclass
class Gamble:
    p: float
    x: int
    y: int


#heurestic functions


def lexigographic_heurestic(g1, g2):
    """returns gamble number (1 or 2) based on payoff of most probable outcome"""

    #since p lies between 0.5 and 1, most probable outcome is x1 or x2
    #need to handle p = 0.5 case

    #clearly the cost is 1 here.
    if g1.x > g2.x:
        return g1
    else:
        return g2


def equal_weight_heurestic(g1, g2):
    """returns gamble number (1 or 2) based on highest average payoff"""

    #clearly the cost is 3 time steps
    avg1 = ( g1.x + g1.y ) / 2
    avg2 = ( g2.x + g2.y ) / 2

    if (avg1 > avg2):
        return g1
    else:
        return g2
 
def get_reward(g1, g2, heurestic):
    
    if heurestic == 'ewh':
        g = equal_weight_heurestic(g1, g2)
    else:
        g = lexigographic_heurestic(g1, g2)    

    roulette_wheel = random.random()
    

    if (roulette_wheel < g1.p):
        return g.x
    else:
        return g.y
        




#################### main function #################

reward = 0

for i in range(1000):
    p = random.uniform(0.5, 1)
    x1 = random.uniform(-10, 10)
    y1 = random.uniform(-10, 10)
    x2 = random.uniform(-10, 10)
    y2 = random.uniform(-10, 10)
    
    g1 = Gamble(p, x1, y1)
    g2 = Gamble(p, x2, y2)
   
    temp_reward = get_reward(g1, g2, 'ewh')
    print(g1.x, g1.y, g2.x, g2.y, temp_reward)
    reward = reward + temp_reward

print(reward)



    