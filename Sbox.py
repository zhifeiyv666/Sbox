import math

class Sbox:

    def __init__(self, K = 0.356, A = 4, M = 256, n = 2000, DPmax = 10, LPmin = 100, maxIteration = 1000, KStep = 0.1):
        """
        初始化参数
        :param K:
        :param A:
        :param M:
        :param n:
        :param DPmax: 第8，9步的判断阈值
        :param LPmin: 第8，9步的判断阈值
        :param maxIteration:  最大迭代次数, 第十步返回第一步的判断阈值
        :param KStep: K每次递增的量，用于第十步返回第一步。
        """
        self.setX0(K)
        self.A = A
        self.M = M
        self.n = n

        self.DPmax = DPmax
        self.LPmin = LPmin
        self.maxIteration = maxIteration
        self.KStep = KStep

    def initSbox(self):
        return [i for i in range(self.M)]

    def setX0(self, K):
        self.K = K
        self.X0 = K

    def increaseK(self):
        self.K = self.K + self.KStep

    def chaosIterationFunc(self):
        X = [self.X0]
        tmp = self.X0
        for i in range(self.n):
            cur = self.A * tmp * (1 - tmp)
            X.append(cur)
        return X

    def mapFunc(self, X):
        """
        将向量X映射
        :param X:
        :return:
        """
        Y = []
        for x in X :
            Y.append(math.floor(self.M * x))
        return Y

    def swap(self, Sbox, i, j):
        """
        原地交换数组Sbox的第i个和第j个元素
        :param Sbox:
        :param i:
        :param j:
        :return:
        """
        tmp = Sbox[i]
        Sbox[i] = Sbox[j]
        Sbox[j] = tmp
        return Sbox

    def getNewSbox(self):
        """
        感觉有点问题：一次置换的定义到底是一个i还是对分组全部进行置换。
        就是，置换一次后的数组和原来的数组不同点是两个元素还是几乎全部
        :param count: 置换次数
        :return:
        """
        newSbox = [i for i in self.Sbox]
        self.swap(newSbox, self.Y[0], self.Y[len(self.Y) - 1])
        for i in range(1, math.floor(len(self.Y ) / 2)) :
            self.swap(newSbox, self.Y[i], self.Y[2 * i])
        return newSbox

    def DP(self):
        pass

    def LP(self):
        pass

    def start(self):
        """
        没完善，有一个小问题：一次置换的定义
        :return:
        """
        while True:
            self.setX0(self.K)
            self.X = self.chaosIterationFunc()
            self.Y = self.mapFunc(self.X)
            self.Sbox = self.initSbox()
            i = 0
            while i < self.maxIteration:
                self.newSbox = self.getNewSbox()
                LP = self.LP()
                DP = self.DP()
                if DP > self.DPmax or LP < self.LPmin:
                    i += 1
                    continue
                if DP < self.DPmax and LP > self.LPmin:
                    return [self.X0, self.newSbox]
            self.increaseK() ## 返回第一步应该又变量，这里我感觉变量应该是K,K应该是递增的
            if self.K - 1 >= -0.000001: ## 区间不在（0，1）
                return [-1, -1]


if __name__ == "__main__" :
    sbox = Sbox(K = 0.356, A = 4, KStep = 0.001)
    X0, newSbox = sbox.start()
    print(X0)
    print(newSbox)