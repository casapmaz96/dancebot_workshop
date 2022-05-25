import random, math
import numpy as np

DANCES =[0, 1, 2, 3] #do nothing, wiggle, left moonwalk, right moonwalk
#LOCATIONS = [0, 1] #in frame, out of frame

class QLearningAgent():
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, epsilon=0.3, alpha=0.3, gamma=0):
        "You can initialize Q-values here..."
        num_states = len(DANCES)**2
        num_actions = len(DANCES)
        ##Create state to index mapping
        self.actionIndices = {'doNothing': 0, 'wiggle': 1, 'shuffle':2, 'donut':3}
        self.index2action = {0: 'doNothing', 1: 'wiggle', 2:'shuffle', 3: 'donut'}

        self.stateIndices = {}
        i = 0
        for p in DANCES:
            for pp in DANCES:
                self.stateIndices[(p, self.index2action[pp])] = i
                i += 1

        #self.previousDanceMove = 'doNothing'
        ##Create action to index mapping
        self.qvalues = np.zeros((num_states, num_actions)) ##q values start with all zero
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = gamma

        self.calm = np.zeros((num_states, num_actions))
        for s in range(self.calm.shape[0]):
            self.calm[s, int(s/num_actions)] = 500

        self.restless = self.calm.copy()
        for s in range(num_actions):
            self.restless[s, 0] = -500
            for ss in range(1, num_actions):
                if s != ss:
                    self.restless[s, ss] = 500

        self.variations = {'My Dancebot': self.qvalues, 'Calm Dancebot': self.calm, 'Restless Dancebot': self.restless}
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        state_index = self.stateIndices[state]
        action_index = self.actionIndices[action]
        return self.qvalues[state_index, action_index]


    def computeValueFromQValues(self, state, legal_actions):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        state_index = self.stateIndices[state]
        #legal_actions = self.getLegalActions(state)
        if len(legal_actions) > 0:
            action_values = self.qvalues[state_index, legal_actions]
            return np.max(action_values)
        else: return 0

    def computeActionFromQValues(self, state, legal_actions):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        state_index = self.stateIndices[state]
        #legal_actions = self.getLegalActions(state)
        if len(legal_actions) > 0:
            action_values = self.qvalues[state_index, legal_actions]
            optimum_action =  np.argmax(action_values)
            return self.index2action[legal_actions[optimum_action]]
        else: return None


    def getAction(self, state, legal_actions):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        state_index = self.stateIndices[state]
        #legal_actions = self.getLegalActions(state)
        "*** YOUR CODE HERE ***"
        if legal_actions == []: return None
        if random.choices([True, False], cum_weights=[self.epsilon, 1-self.epsilon], k=1)[0]:
            action = self.index2action[random.choice(legal_actions)]

        else:
            action = self.computeActionFromQValues(state, legal_actions)
        return action


    def update(self, state, action, nextState, reward, legal_actions):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #bestAction = self.computeActionFromQValues(nextState)
        nextValue = self.computeValueFromQValues(nextState, legal_actions)
        state_index = self.stateIndices[state]
        action_index = self.actionIndices[action]

        qval = self.getQValue(state, action)
        self.qvalues[state_index, action_index] = qval + self.alpha * (reward + self.discount * nextValue - qval)


    def getPolicy(self, state, legal_actions):
        return self.computeActionFromQValues(state, legal_actions)

    def getValue(self, state, legal_actions):
        return self.computeValueFromQValues(state, legal_actions)

    def createState(self, detectedPose, prevDanceMove):
        state = (detectedPose, prevDanceMove)
        return state

#    def getLegalActions(self, state):
#        if state[1] == 'doNothing':
#            return DANCES
#        else:
#            return MOVES
