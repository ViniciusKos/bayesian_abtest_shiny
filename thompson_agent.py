import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

class ThompsonAgent( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list
    
    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine ]:
            reward = 1
        else:
            reward = 0
            
        return reward


def reward_plot( success_array, failure_array ):
    linestyle = [ "-", "--" ]

    x = np.linspace( 0 ,1, 1002 )[1:-1]

    plt.clf()
    plt.xlim( 0, 1 )
    plt.ylim( 0, 30)

    for a, b, ls in zip( success_array, failure_array, linestyle ):
        dist = beta( a, b )

        plt.plot( x, dist.pdf( x ), ls=ls ,c='black', label=f"Alpha:{a} Beta:{b}")
        plt.draw()
        plt.pause( 0.01 )
        plt.legend( loc=0 )

# positive result proba    
prob_list = [ 0.25 , 0.28 ]

# experiment params
trials = 1000
episodes = 200

bandit = ThompsonAgent( prob_list )

prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = []
avg_accumulated_reward_array = []

for episode in range( episodes ):

    #arrays creations
    success_array = np.ones( len( prob_list ) )
    failure_array = np.full( len( prob_list ), 1.0e-5 )

    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5)
    accumulated_reward = 0

    for trial in range( trials ):
        # agent choose
        prob_reward = np.random.beta( success_array, failure_array )
        bandit_machine = np.argmax( prob_reward )

        # agent reward
        reward = bandit.pull( bandit_machine )

        if reward == 1:
            success_array[ bandit_machine ] += 1
        else:
            failure_array[ bandit_machine ] += 1


        # plot reward
        reward_plot( success_array, failure_array )


        reward_array[ bandit_machine ] += reward
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    prob_reward_array += reward_array / bandit_array
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

prob01 = 100*np.round( prob_reward_array[0] / episodes, 2)
prob02 = 100*np.round( prob_reward_array[1] / episodes, 2)

print( "Prob page 1 better:", prob01,"% ", "Prob page 2 better:", prob02,"% ")
print( "Avg acccumulated reward:", np.mean( avg_accumulated_reward_array ) )