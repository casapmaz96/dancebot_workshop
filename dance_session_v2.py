#TERMINAL = [4] #stop and finish game
DANCES =[0, 1, 2, 3] #do nothing, wiggle, left moonwalk, right moonwalk

class DanceSession:

    def __init__(self, agent,  dance_punishment,
                laziness_punishment, dance_reward, repeat_punishment, pose2dance):
        self.agent = agent
        self.prevState = None
        self.prevAction = 'doNothing'
        self.cumReward = 0

        self.pose2dance = dict(pose2dance)
        self.repeatPunishment = repeat_punishment
        self.lazinessPunishment = laziness_punishment
        self.dancePunishment = dance_punishment
        self.danceReward = dance_reward

        self.repeated = False
    def run(self, counts, keypoints, robot):
        """
        Main control loop for game play.
        """
        # inform learning agents of the game start
        # aka. Reset the agent state to initial state, reset rewards, etc.


        # Observe current state
        # aka. get the image, convert to state, etc
        # also do qlearning updates here
        #location = self.getLocation(counts, keypoints)
        pose = self.getPose(counts, keypoints)        
        newstate = self.agent.createState(pose, self.prevAction)
        #print('prevaction2:', self.prevAction)
        legalActions = self.getLegalActions(newstate)
        reward = 0
        if self.prevState:
            reward = self.calculateReward()
            self.cumReward += reward
         #   print('prevaction:', self.prevAction)
            self.agent.update(self.prevState, self.prevAction, newstate, reward, legalActions)
        #print('1:', predance)
        # Solicit an action
        # aka. agent.getAction()
        action = self.agent.getAction(newstate, legalActions)
#        print(action)
        if action == self.prevAction:
            self.repeated = True

        # Execute the action
        # aka. robot. perform action
        #self.executeAction(action)

        self.executeAction(action, robot)

        # Allow for game specific conditions (winning, losing, etc.)
        # aka. update predance/postdance, prevstate/action, reset sesh
        self.prevAction = action
        self.prevState = newstate
        return reward


    def calculateReward(self):
        reward = 0
        if self.repeated:
#            print('repeatd')
            reward -= self.repeatPunishment
            self.repeated = False
        if self.prevAction == 'doNothing':
#            print('lazy')
            reward -= self.lazinessPunishment
        if self.pose2dance[self.prevState[0]] == self.prevAction:
#            print('good dance')
            reward += self.danceReward
        else:
#            print('bad dance')
            reward -= self.dancePunishment
        return reward

    def getPose(self, counts, keypoints):
        #define poses
        pose = 0

        if counts.item() > 0:
            if 'neck' in keypoints.keys():
                if 'left_wrist' in keypoints.keys():
                    if keypoints['left_wrist'][1] \
                    < keypoints['neck'][1]:
                        pose += 1
                if 'right_wrist' in keypoints.keys():
                    if keypoints['right_wrist'][1] \
                    < keypoints['neck'][1]:
                        pose += 2
        return pose

    def getLegalActions(self, state):
        return DANCES

    def executeAction(self, action, robot):
        if action != 'doNothing' and action != 'stop':
            move = getattr(robot, action)
            move()

