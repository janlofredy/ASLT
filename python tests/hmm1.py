import numpy as np
# Words 
states = ('Good', 'Morning')

#Keypoints
observations = ('RightWrist', 'shop', 'clean')

pi = np.array([0.6, 0.4])  #initial probability 

#
A = np.array([[0.7, 0.3],[0.4, 0.6]]) #Transmission probability 

#
B = np.array([[0.1, 0.4, 0.5],[0.6, 0.3, 0.1]]) #Emission probability

bob_says = np.array([0, 2, 1, 1, 2, 0, 1,2,1,0,0,2,1])


# Forward Path
def forward(obs_seq, pi, A, B):
    T = len(obs_seq)
    N = A.shape[0]
    alpha = np.zeros((T, N))
    alpha[0] = pi*B[:,obs_seq[0]]
    for t in range(1, T):
        alpha[t] = np.inner(alpha[t-1],A) * B[:, obs_seq[t]]
    return alpha

def likelihood(alpha):
    # returns log P(Y  \mid  model)
    # using the forward part of the forward-backward algorithm
    return  alpha[-1].sum()

alpha = forward(bob_says, pi, A, B)
# print(alpha)
likelihood(alpha)

def backward(obs_seq, A, B):
    N = A.shape[0]
    T = len(obs_seq)

    beta = np.zeros((N,T))
    beta[:,-1:] = 1

    for t in reversed(range(T-1)):
        for n in range(N):
            beta[n,t] = np.sum(beta[:,t+1] * A[n,:] * B[:, obs_seq[t+1]])

    return beta


def gamma(alpha, beta):
    obs_prob = likelihood(alpha)
    return (np.multiply(alpha,beta.T) / obs_prob)

beta=backward(bob_says, A, B)
beta.T

gamma(alpha, beta)
def viterbi(obs_seq,pi, A, B):
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

alice_hears=viterbi(bob_says, pi, A, B)
print("Bob says:", ", ",list(map(lambda y: observations[y], bob_says)))
print("Alice hears:", ", ", list(map(lambda s: states[s], alice_hears)))


