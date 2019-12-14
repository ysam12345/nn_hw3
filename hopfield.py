
import numpy as np

# Data Type
uintType = np.uint8
floatType = np.float32

class HOP(object):
    def __init__(self, N):
        self.N = N
        self.W = np.zeros((N, N), dtype = floatType)

    def kroneckerSquareProduct(self, factor):
        ksProduct = np.zeros((self.N, self.N), dtype = floatType)

        for i in range(0, self.N):
            ksProduct[i] = factor[i] * factor

        return ksProduct

    def trainOnce(self, inputArray):
        mean = float(inputArray.sum()) / inputArray.shape[0]
        self.W = self.W + self.kroneckerSquareProduct(inputArray - mean) / (self.N * self.N) / mean / (1 - mean)

        index = range(0, self.N)
        self.W[index, index] = 0.

    def hopTrain(self, stableStateList):
        stableState = np.asarray(stableStateList, dtype = uintType)

        if np.amin(stableState) < 0 or np.amax(stableState) > 1:
            return

        # Train
        if len(stableState.shape) == 1 and stableState.shape[0] == self.N:
            self.trainOnce(stableState)
        elif len(stableState.shape) == 2 and stableState.shape[1] == self.N:
            for i in range(0, stableState.shape[0]):
                self.trainOnce(stableState[i])
        else:
            return

    # Run HOP to output
    def hopRun(self, inputList):
        inputArray = np.asarray(inputList, dtype = floatType)

        if len(inputArray.shape) != 1 or inputArray.shape[0] != self.N:
            return

        matrix = np.tile(inputArray, (self.N, 1))
        matrix = self.W * matrix
        ouputArray = matrix.sum(1)

        m = float(np.amin(ouputArray))
        M = float(np.amax(ouputArray))
        ouputArray = (ouputArray - m) / (M - m)


        ouputArray[ouputArray < 0.5] = 0.
        ouputArray[ouputArray > 0] = 1.

        return np.asarray(ouputArray, dtype = uintType)

    def hopReset(self):
        self.W = np.zeros((self.N, self.N), dtype = floatType)
