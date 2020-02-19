import random
import numpy
from dataclasses import dataclass
import time

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
 
def get_reward(g1, g2, heurestic, roulette_wheel):
    
    if heurestic == 'ewh':
        g = equal_weight_heurestic(g1, g2)
    else:
        g = lexigographic_heurestic(g1, g2) 
    

    if (roulette_wheel < g1.p):
        return g.x
    else:
        return g.y
        

def get_time_cost(heurestic):
    
    
    if heurestic == 'ewh':
        return 3
    else:
        return 1

def get_relative_reward(g1, g2, heurestic, roulette_wheel):

    actual_reward = get_reward(g1, g2, heurestic, roulette_wheel)

    if roulette_wheel < g1.p:
        max_reward_strategy = max(g1.x, g2.x)
    else:
        max_reward_strategy = max(g1.y, g2.y)
    
    predicted_relative_reward =  (actual_reward / max_reward_strategy)

    min_possible_reward = min(g1.x, g1.y, g2.x, g2.y)
    max_possible_strategy = max(g1.x, g1.y, g2.x, g2.y)
    predicted_absolute_reward = min(min_possible_reward + (max_possible_strategy - min_possible_reward) * predicted_relative_reward, max_possible_strategy)

    return predicted_absolute_reward 


# VOC = (utility of strategy s) - gamma * cost
def get_voc(g1, g2, heurestic, roulette_wheel, reward, t):
    utility = get_reward(g1, g2, heurestic, roulette_wheel)
    gamma = get_relative_reward(g1, g2, heurestic, roulette_wheel)
    cost = get_time_cost(heurestic)
    voc = utility - (gamma * cost)
    #print(gamma, voc, heurestic)
    return voc
    




#################### main function #################

reward = 0

t = 0
count_ewh = 0
count_lh = 0

voc_lh_total = 0
voc_ewh_total = 0
while t < 1000:
    p = random.uniform(0.9, 1.0)
    x1 = random.uniform(-10, 10)
    y1 = random.uniform(-10, 10)
    x2 = random.uniform(-10, 10)
    y2 = random.uniform(-10, 10)
    
    g1 = Gamble(p, x1, y1)
    g2 = Gamble(p, x2, y2)

    roulette_wheel = random.random()

    voc_ewh = get_voc(g1, g2, 'ewh', roulette_wheel, reward, t)
    voc_lh = get_voc(g1, g2, 'lh', roulette_wheel, reward, t)
    print(voc_ewh, voc_lh)
    voc_lh_total = voc_lh + voc_lh_total
    voc_ewh_total = voc_ewh + voc_ewh_total

    if voc_ewh > voc_lh:
        t = t + 3
        reward = reward + get_reward(g1, g2, 'ewh', roulette_wheel)
        count_ewh = count_ewh + 1
        #print('ewh')
    else:
        t = t + 1
        reward = reward + get_reward(g1, g2, 'lh', roulette_wheel)
        count_lh = count_lh + 1
        #print('lh')
    #print(t, g1.x, g1.y, g2.x, g2.y, reward)
    


def run():
    reward = 0

    t = 0
    count_ewh = 0
    count_lh = 0

    voc_lh_total = 0
    voc_ewh_total = 0
    while t < 1000:
        p = random.uniform(0.9, 1.0)
        x1 = random.uniform(-10, 10)
        y1 = random.uniform(-10, 10)
        x2 = random.uniform(-10, 10)
        y2 = random.uniform(-10, 10)
        
        g1 = Gamble(p, x1, y1)
        g2 = Gamble(p, x2, y2)

        roulette_wheel = random.random()

        voc_ewh = get_voc(g1, g2, 'ewh', roulette_wheel, reward, t)
        voc_lh = get_voc(g1, g2, 'lh', roulette_wheel, reward, t)
        print(voc_ewh, voc_lh)
        voc_lh_total = voc_lh + voc_lh_total
        voc_ewh_total = voc_ewh + voc_ewh_total

        if voc_ewh > voc_lh:
            t = t + 3
            reward = reward + get_reward(g1, g2, 'ewh', roulette_wheel)
            count_ewh = count_ewh + 1
            #print('ewh')
        else:
            t = t + 1
            reward = reward + get_reward(g1, g2, 'lh', roulette_wheel)
            count_lh = count_lh + 1

    print(voc_ewh_total, voc_lh_total)
#print(reward)
#print(count_ewh, count_lh)

    