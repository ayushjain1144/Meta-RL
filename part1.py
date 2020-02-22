import random
import numpy as np
from dataclasses import dataclass
import time

# 7 dollars per hour or 0.002 dollars / sec
OPPORTUNITY_COST  =  0.002
EPSILON = 0.1
MIN_BOUND = 0.5

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
    
    # 4 Reads + 2 Additions + 1 comparisions + 1 Result
    if heurestic == 'ewh':
        return 8 * OPPORTUNITY_COST

    # 2 Reads + 1 comparision + 1 Result
    else:
        return 4 * OPPORTUNITY_COST

def extract_features(g1):

    highest_outcome_probability = g1.p
    differnce = max(g1.x1, g1.y1) - min (g1.x1, g1.y1)
    return (highest_outcome_probability, differnce)


def get_relative_reward(g1, g2, heurestic):

    
    # outcome can be either o1 (with prob p) and o2 (with prob 1-p)


    #if outcome is o1

    actual_reward_o1 = get_reward(g1, g2, heurestic, 0)
    max_reward_o1 = max(g1.x, g2.x)
    predicted_relative_reward_o1 =  (actual_reward_o1 / max_reward_o1)

    # if outcome is o2
    actual_reward_o2 = get_reward(g1, g2, heurestic, 1)
    max_reward_o2 = max(g1.y, g2.y)
    predicted_relative_reward_o2 =  (actual_reward_o2 / max_reward_o2)

    # expected reward = o1*p + o2*(1-p)

    expected_reward = predicted_relative_reward_o1 * p + predicted_relative_reward_o2 * (1 - p)

    min_possible_reward = min(g1.x, g1.y, g2.x, g2.y)
    max_possible_strategy = max(g1.x, g1.y, g2.x, g2.y)
    predicted_absolute_reward = min(min_possible_reward + (max_possible_strategy - min_possible_reward) * expected_reward, max_possible_strategy)

    if heurestic == 'ewh':
        return predicted_absolute_reward / 8
    else:
        return predicted_absolute_reward / 4



# VOC = (utility of strategy s) - gamma * cost
def get_voc(g1, g2, heurestic):
    utility = get_relative_reward(g1, g2, heurestic)
    cost = get_time_cost(heurestic)
    voc = utility - cost
    #print(gamma, voc, heurestic)
    return voc
    

def get_strategy_epsilon_greedy(voc_ewh, voc_lh):

    # exploit
    if random.random() < 1 - EPSILON:
        if np.argmax((voc_ewh, voc_lh)) == 0:
            return "ewh"
        else:
            return "lh"
    
    #explore
    else:
        if random.random() < 0.5:
            return "ewh"
        else:
            return "lh"

    


#################### main function #################

reward = 0

t = 0
count_ewh = 0
count_lh = 0

voc_lh_total = 0
voc_ewh_total = 0
while t < 1000:

    print(f"\nPresent time:  {t}\n")
    p = random.uniform(MIN_BOUND , 1.0)
    x1 = random.uniform(-10, 10)
    y1 = random.uniform(-10, 10)
    x2 = random.uniform(-10, 10)
    y2 = random.uniform(-10, 10)
    
    g1 = Gamble(p, x1, y1)
    g2 = Gamble(p, x2, y2)

    # for selecting the actual outcome, similar to what is done in genetic algorithms
    roulette_wheel = random.random()

    voc_ewh = get_voc(g1, g2, 'ewh')
    voc_lh = get_voc(g1, g2, 'lh')

    heurestic = get_strategy_epsilon_greedy(voc_ewh, voc_lh)
    print(f"usinh heurestic: {heurestic}")
    reward = reward + get_reward(g1, g2, heurestic, roulette_wheel)
    print(f"got reward: {reward}")
    #print(voc_ewh, voc_lh, g1, g2)

    
    if heurestic == "ewh":
        t = t + 8
        count_ewh = count_ewh + 1
    else:
        t = t + 4
        count_lh = count_lh + 1

print("\nFinal statistics\n\n")

print(f"\n\ntotal reward: {reward}")
print(f"number of times equal weight heurestic is used: {count_ewh}")
print(f"number of lexigographic heurestic is used: {count_lh}")


