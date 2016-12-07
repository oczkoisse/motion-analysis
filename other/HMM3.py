__author__ = 'Prady'
import numpy as np

class HMM:
    def __init__(self, states, alphabets, modelFile = None):
        self.alphabets = alphabets
        self.states = states
        self.labels=self.alphabets
        if modelFile is None:
            self.initializeProbs()
        else:
            self.priorProbs, self.transitionProbs, self.observationProbs = self.readModelFile(modelFile)
        print(alphabets)
        print(self.priorProbs)
        print(self.transitionProbs)
        print(self.observationProbs)

    def initializeProbs(self):
        #Prior Probs
        self.priorProbs = np.array([1.0/len(self.states)]*len(self.states))

        #Transition probs
        diagonalEntry = 0.6
        offDiagonalEntry = 0.4/(len(self.states)-1)
        self.transitionProbs = np.ones((len(self.states),len(self.states)))*offDiagonalEntry
        np.fill_diagonal(self.transitionProbs, diagonalEntry)

        #observation Probs
        diagonalEntry = 0.5
        offDiagonalEntry = 0.5/(len(self.alphabets)-1)
        self.observationProbs = np.ones((len(self.states),len(self.alphabets)))*offDiagonalEntry
        np.fill_diagonal(self.observationProbs, diagonalEntry)
        #self.observationProbs=np.random.dirichlet(np.ones(len(self.alphabets)),size=len(self.states))

    def readModelFile(self,modelFile):
        '''
        Reads Model file and stores prior, transition and observation probabilities
        '''
        print("Reading model file",modelFile)
        n = len(self.alphabets)
        bottomRows = 2*n+2
        priorProbs = np.genfromtxt(modelFile, float, delimiter = ' ', skip_header = 1, skip_footer = bottomRows)
        transitionProbs = np.genfromtxt(modelFile, float, delimiter = ' ', skip_header = 3, skip_footer = n+1)
        observationProbs = np.genfromtxt(modelFile, float, delimiter = ' ', skip_header = n+4)
        return priorProbs,transitionProbs,observationProbs

    def forwardProbability(self,observationSequence,scaling=True):
        if scaling:
            c=[]

        forwardProbability = np.zeros((len(self.states), len(observationSequence)))
        observationIndex = self.labels.index(observationSequence[0])
        for stateIndex, _ in enumerate(self.states):
            forwardProbability[stateIndex][0] = self.priorProbs[stateIndex] * self.observationProbs[stateIndex][observationIndex]

        if scaling:
            c.append(sum(forwardProbability[:,0]))
            forwardProbability[:,0] /= sum(forwardProbability[:,0])


        for t in range(1,len(observationSequence)):
            #print observationSequence[t]
            observationIndex = self.labels.index(observationSequence[t])
            for stateIndex, _ in enumerate(self.states):
                temp = 0
                for i in range(len(self.states)):
                    temp += forwardProbability[i][t-1]*self.transitionProbs[i][stateIndex]*self.observationProbs[stateIndex][observationIndex]

                forwardProbability[stateIndex][t] = temp
            if scaling:
                c.append(sum(forwardProbability[:,t]))
                forwardProbability[:,t] /= sum(forwardProbability[:,t])

        if scaling:
            log_Prob_Obs=np.sum(np.log(c))
            return (log_Prob_Obs, forwardProbability, c )
        else:
            log_Prob_Obs = np.log(np.sum(forwardProbability[:,-1 ]))
            return (log_Prob_Obs, forwardProbability)

    def backwardProbability(self, observationSequence, c=None):
        backwardProbability = np.zeros((len(self.states), len(observationSequence)))
        backwardProbability.T[-1] = [1]*len(self.states)
        if c is not None:
            backwardProbability[:,-1] /= c[-1]

        for t in range(len(observationSequence)-2,-1, -1):
            observationIndex = self.labels.index(observationSequence[t+1])
            for stateIndex, _ in enumerate(self.states):

                temp = 0
                for j in range(len(self.states)):
                    temp += backwardProbability[j][t+1]*self.transitionProbs[stateIndex][j]*self.observationProbs[j][observationIndex]

                backwardProbability[stateIndex][t] = temp
            if c is not None:
                backwardProbability[:,t] /= c[t]
        return backwardProbability

    def xi(self,observationSequence, forwardProbability, backwardProbability, sequenceProbability):
        dim=len(self.states)
        transitionProbsTime = np.zeros((dim,dim,len(observationSequence)-1))
        for t in range(len(observationSequence)-1):
            observationIndex = self.labels.index(observationSequence[t+1])
            for i in range(dim):
                for j in range(dim):
                    transitionProbsTime[i][j][t] = (forwardProbability[i][t]*self.transitionProbs[i][j]*self.observationProbs[j][observationIndex]*backwardProbability[j][t+1])/sequenceProbability
        return transitionProbsTime

    def gamma(self,transitionProbsTime):
        #Gamma Transitions from state i
        gamma = np.sum(transitionProbsTime, axis = 1)
        gammaLast = np.reshape(np.sum(transitionProbsTime[:,:,-1],axis = 0),(-1,1))
        gamma = np.hstack((gamma,gammaLast))
        return gamma

    def calculateObsProbList(self, obsList):
        count = 0
        for observationSequence in obsList:
            log_Prob_Obs, _, _ =  self.forwardProbability(observationSequence)
            count += log_Prob_Obs
        return count/len(obsList)

    def train(self,observationSequenceList, epochs = 100, testSequence=None, priorLikelihood=True):
        print("Training HMM using Baum-Welch algorithm on %d sequences"%(len(observationSequenceList)))
        LLS=[]
        if priorLikelihood:
            LLS = [self.calculateObsProbList(observationSequenceList)]
            if testSequence is not None:
                testLLS = [self.calculateObsProbList(testSequence)]
        transPoint = self.transitionProbs.reshape((-1,1))

        for epoch in range(epochs):
            print("\n==================== Epoch %d ===================="%epoch)
            transitionNumerator = np.zeros((len(self.states),len(self.states)))
            transitionDenominator = np.zeros((len(self.states),len(self.states)))
            observationNumerator = np.zeros((len(self.states),len(self.labels)))
            observationDenominator = np.zeros((len(self.states),len(self.labels)))
            priorProbs = np.zeros(len(self.states))
            count=0
            for observationSequence in observationSequenceList:


                count+=1
                if len(observationSequence)<2:
                    continue
                #print observationSequence
                _, forwardProbability, c =  self.forwardProbability(observationSequence)
                backwardProbability = self.backwardProbability(observationSequence, c)
                transitionProbsTime = self.xi(observationSequence, forwardProbability, backwardProbability, 1)
                gamma = self.gamma(transitionProbsTime)

                priorProbs += gamma[:,0]
                transitionNumerator +=  np.sum(transitionProbsTime, axis = 2)
                denominator = np.sum(gamma[:,:-1], axis=1)

                obs = []
                for label in self.labels:
                    obs.append([i for i, x in enumerate(observationSequence) if x == label])

                for stateIndex in range(len(self.states)):
                    for observationIndex in range(len(self.labels)):
                        for time in obs[observationIndex]:
                            observationNumerator[stateIndex][observationIndex] += gamma[stateIndex][time]


                transitionDenominator += np.repeat(np.reshape(denominator,(-1,1)), len(self.states),axis = 1)
                observationDenominator += np.repeat(np.reshape(np.sum(gamma, axis = 1),(-1,1)), len(self.alphabets), axis = 1)


            priorProbs /= sum(priorProbs)
            transitionProbs = np.nan_to_num(transitionNumerator / transitionDenominator)
            observationProbs = np.nan_to_num(observationNumerator / observationDenominator)


            self.transitionProbs =  transitionProbs
            self.observationProbs = observationProbs

            print("\nTransition: \n", self.transitionProbs,"\n")

            print("Observation: \n",self.observationProbs ,"\n\n\n")
            LLS.append(self.calculateObsProbList(observationSequenceList))
            if testSequence is not None:
                testLLS.append(self.calculateObsProbList(testSequence))
            print(LLS[-1])
            try:
                if abs(LLS[-1]-LLS[-2])<0.0005:
                    print("True")
                    break
            except KeyboardInterrupt:
                raise
            except:
                pass

            transPoint = np.hstack((transPoint, self.transitionProbs.reshape((-1,1))))

        print(LLS)
        LLS += [LLS[-1]]*(epochs-len(LLS))

        if testSequence is not None:
            testLLS += [testLLS[-1]]*(epochs-len(testLLS))
            return self.priorTable, self.transitionTable, self.observationTable, transPoint, LLS, testLLS


        return self.priorProbs, self.transitionProbs, self.observationProbs, transPoint, LLS

    def writeHMM(self, destFile):

        print("Writing trained model to ", destFile)
        fd = open(destFile,'w')
        fd.write("Estimated Prior Probabilities\n")
        np.savetxt(fd, self.priorProbs, newline=" ", fmt = "%.4f")
        fd.write("\nEstimated Transition Table\n")
        np.savetxt(fd, self.transitionProbs, fmt = "%.4f")
        fd.write("Estimated Observation Table\n")
        np.savetxt(fd, self.observationProbs, fmt = "%.4f")
        fd.close()


    def viterbi(self,observationSequence):
        seqScore = np.zeros((len(self.states),len(observationSequence)))
        backPtr = np.zeros((len(self.states),len(observationSequence)))
        seqScore[:,0] = self.priorProbs
        backPtr[:,0]=[-1]*len(backPtr[:,0])

        for t in range(1,len(observationSequence)):
            k = self.alphabets.index(observationSequence[t])

            for i in range(0,len(self.states)):
                scoreList=[]
                for j in range(0,len(self.states)):
                    scoreList.append(seqScore[j][t-1]*self.transitionProbs[j][i]*self.observationProbs[j][k])

                seqScore[i][t] = max(scoreList)
                backPtr[i][t]= scoreList.index(max(scoreList))

            seqScore[:,t] = seqScore[:,t]/sum(seqScore[:,t])
            col = list(seqScore[:,t])
            index = col.index(max(col))
            #print col

        #print seqScore[:,-1]
        lastCol = list(seqScore[:,-1])
        lastIndex = lastCol.index(max(lastCol))
        sequence = self.findMostProbableSequence(backPtr,lastIndex)
        return sequence

    def findMostProbableSequence(self,backPtr,lastIndex):
        t = len(backPtr[0])
        sequence=[-1]*t
        sequence[-1]=lastIndex

        for i in range(t-2,-1,-1):
            sequence[i] = int(backPtr[sequence[i+1]][i+1])
        return sequence

    def viterbiSequenceList(self, observationSequenceList):
        stateSequenceList=[]
        for observationSequence in observationSequenceList:
            stateSequence = self.viterbi(observationSequence)
            stateSequence = [self.states[s] for s in stateSequence]
            stateSequenceList.append(stateSequence)
        return stateSequenceList



