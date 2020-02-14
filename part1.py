import random

#heurestic functions

def lexigographic_heurestic(p1, x1, y1, p2, x2, y2):
    """returns gamble number (1 or 2) based on payoff of most probable outcome"""

    #since p lies between 0.5 and 1, most probable outcome is x1 or x2
    #need to handle p = 0.5 case

    #clearly the cost is 1 here.
    if x1 > x2:
        return 1
    else:
        return 2


def equal_weight_heurestic(p1, x1, y1, p2, x2, y2):
    """returns gamble number (1 or 2) based on highest average payoff"""

    #clearly the cost is 3 time steps
    avg1 = ( x1 + y1 ) / 2
    avg2 = ( x2 + y2 ) / 2

    if (avg1 > avg2):
        return 1
    else:
        return 2
 

#################### main function #################

for i in range(1000):
    p1 = random.uniform(0.5, 1)
    p2 = random.uniform(0.5, 1)
    x1 = random.uniform(-10, 10)
    y1 = random.uniform(-10, 10)
    x2 = random.uniform(-10, 10)
    y2 = random.uniform(-10, 10)

    gamble = equal_weight_heurestic(p1, x1, y1, p2, x2, y2)

    