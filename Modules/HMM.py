import numpy as np
import json

class HMM:

    def __init__(self,states,initProb,transProb,observe,emissionProb,inputSequence):

        self.states = states # Words 

        self.pi = initProb  # Initial probability 

        self.A = transProb # Transition probability 

        self.observations = observe # Observations

        self.B = emissionProb # Emission probability

        self.seq = inputSequence # Input Sequence
        print(self.seq)

        alpha = self.forward(self.seq, self.pi, self.A, self.B)
        self.likelihood(alpha)
        beta = self.backward(self.seq, self.A, self.B)
        beta.T
        self.gamma(alpha,beta)
        self.Answer = self.viterbi(self.seq, self.pi, self.A, self.B)

        # print("Observed Sequence is:", ", ",list(map(lambda y: self.observations[y], self.seq)))
        # print("Possible Outcome is:", ", ", list(map(lambda s: self.states[s], self.Answer)))

# BAUM WELCH Algorithm or Forward-Backward Algorithm
    # Forward Path
    def forward(self,obs_seq, pi, A, B):
        T = len(obs_seq)
        N = A.shape[0]
        alpha = np.zeros((T, N))
        alpha[0] = pi*B[:,obs_seq[0]]
        for t in range(1, T):
            alpha[t] = np.inner(alpha[t-1],A) * B[:, obs_seq[t]]
        return alpha

    def likelihood(self,alpha):
        # returns log P(Y  \mid  model)
        # using the forward part of the forward-backward algorithm
        return  alpha[-1].sum()

    # Backward Path
    def backward(self,obs_seq, A, B):
        N = A.shape[0]
        T = len(obs_seq)

        beta = np.zeros((N,T))
        beta[:,-1:] = 1

        for t in reversed(range(T-1)):
            for n in range(N):
                beta[n,t] = np.sum(beta[:,t+1] * A[n,:] * B[:, obs_seq[t+1]])

        return beta
# Baum-welch End

    def gamma(self,alpha, beta):
        obs_prob = self.likelihood(alpha)
        return (np.multiply(alpha,beta.T) / obs_prob)


    def viterbi(self,obs_seq,pi, A, B):
        # returns the most likely state sequence given observed sequence x
        # using the Viterbi algorithm
        T = len(obs_seq)
        N = A.shape[0]
        delta = np.zeros((T, N))
        psi = np.zeros((T, N))
        delta[0] = pi*B[:,obs_seq[0]]
        for t in range(1, T):
            for j in range(N):
                delta[t,j] = np.max(delta[t-1]*A[:,j]) * B[j, obs_seq[t]]
                psi[t,j] = np.argmax(delta[t-1]*A[:,j])

        # backtrack
        states = np.zeros(T, dtype=np.int32)
        states[T-1] = np.argmax(delta[T-1])
        for t in range(T-2, -1, -1):
            states[t] = psi[t+1, states[t+1]]
        return states

    def getSequence(self):
        return list(map(lambda s: self.states[s], self.Answer))

# states = ()
# A = np.array([])
# B = np.array([])
# sequence = np.array([])

# with open('Dataset/learningCache.json') as json_file:
#     file = json.load(json_file)
#     # print(file.keys())



#     forInitProb = []
#     forTransition = []

#     states = tuple(file['states'])

#     for i in states:
#         forInitProb.append(file['initialProbabilities'][i]/sum(file['initialProbabilities'].values()))
#         tempInner = []
#         for j in states:
#             tempInner.append(file['transitionProbabilities'][i][j])
#         forTransition.append(tempInner)

#     pi = np.array(forInitProb)
#     A = np.array([forTransition])



#     # print(file['emissions'].keys())
#     # print(file['emissions']['rightWristX'].keys())
#     # print(file['emissions']['rightWristX']['observations'][0])
#     # print(file['emissions']['rightWristX']['emissionProbabilities'])
#     # print(file['transitionProbabilities'].keys())

#     for key, value in file['emissions'].items():
#         # print(key)
#         observations = tuple(value['observations'][0])

#         forEmission = []
#         for i in states:
#             tempInner = []
#             for j in observations:
#                 # print(value['emissionProbabilities'].keys())
#                 tempInner.append(value['emissionProbabilities'][str(j)][str(i)])
#             forEmission.append(tempInner)
#             # print(tempInner)
#         # print(len(forEmission), len(states))
#         B = np.array(forEmission)
#         sequence = np.array([])

#         # alpha = forward(sequence, pi, A, B)
#         # likelihood(alpha)
#         # beta = backward(sequence, A, B)
#         # beta.T
#         # gamma(alpha,beta)
#         # Answer = viterbi(sequence, pi, A, B)
#         # print("Observed Sequence is:", ", ",list(map(lambda y: observations[y], sequence)))
#         # print("Possible Outcome is:", ", ", list(map(lambda s: states[s], Answer)))


# states = ('Good', 'Morning') # Words 

# pi = np.array([0.6, 0.4])  #initial probability 

# A = np.array([[0.7, 0.3],[0.4, 0.6]]) #Transition probability 

# observations = ('RightWrist', 'shop', 'clean') # Keypoints

# B = np.array([ [0.1, 0.4, 0.5], [0.6, 0.3, 0.1] ]) #Emission probability

# bob_says = np.array([0, 2, 1, 1, 2, 0, 1,2,1,0,0,2,1]) # input Sequence



# alpha = forward(bob_says, pi, A, B)
# # print(alpha)
# likelihood(alpha)

# beta=backward(bob_says, A, B)
# beta.T

# gamma(alpha, beta)

# alice_hears=viterbi(bob_says, pi, A, B)
# print("Observed Sequence is:", ", ",list(map(lambda y: observations[y], bob_says)))
# print("Possible Outcome is:", ", ", list(map(lambda s: states[s], alice_hears)))

