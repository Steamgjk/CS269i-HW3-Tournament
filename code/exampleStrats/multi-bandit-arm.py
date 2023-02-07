import random
import numpy as np
from mabwiser.mab import MAB, LearningPolicy, NeighborhoodPolicy

# value is your initial value in this round, you should not bid a higher price than value
# because in that way you will get a negative utility (score) in this round

# We also provide the history for you and the competitor
# The length of myHistory and competitorHistory are equal
# During round n, you receive the history for the past (n-1) rounds, i.e.,
# The length of myHistory is n-1
# myHistory[i] is a 4-element list, including 
# (1) your initial value in round i
# (2) your bid price in round i
# (3) your allocation result (whether or not you get the item) in round i
# (4) your payment in round i

# We are using the Multi-Arm-Bandit algorithm to choose bid price
# We are using MABWiser lib, you should install it by running pip install mabwiser
# Please check the doc https://fidelity.github.io/mabwiser/examples.html and you can 
# implement many fancy algorithms by yourself


# Define your arm, here we define 10 arms, each arm is a factor between [0.1,1.0]
# After you make a decision of the arm to use,  the bid price will be value * arm[i] 

# Surely you can have your own definition of arms and design more complicated algorithms
Arms = [ 0.1 * i for i in range(1,11) ]

Rewards = []

Decisions = []



def strategy(value, myHistory):
    global Arms
    global Rewards
    global Decisions
    bidPrice = 0
    if len(myHistory)>0:
        # Since there can be multiple times of running, trim the Decision list so that
        # the decision history belongs to one single run 
        Decisions = Decisions[-len(myHistory):]
        Rewards = []
        for i in range(len(myHistory)):
            # I use the allocation Result as the reward, you can also try using payment as the reward
            Rewards.append(myHistory[i][2])
        # print(len(Decisions), "  ", len(Rewards))
    else:
        Decisions = []
        Rewards = []
    if(len(myHistory)<100):
        # For the first 100 rounds, just randomly make decisions to explore
        decision = int(random.randrange(0,10,1))
        Decisions.append(decision)
        bidPrice =  Arms[decision] * value
    else:
        # Model 
        mab = MAB(Arms, LearningPolicy.UCB1(alpha=1.25))
        # Train
        mab.fit(Decisions, Rewards)
        decision = int(mab.predict())
        Decisions.append(decision)
        bidPrice =  Arms[decision] * value

    return bidPrice
    




