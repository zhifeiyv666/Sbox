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

def hanming(a, b):
    c = a ^ b
    res = 0
    while c != 0:
        res += c & 1
        c >>= 1
    return res

def f1():
    S = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab,
         0x76,
         0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72,
         0xc0,
         0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31,
         0x15,
         0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2,
         0x75,
         0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f,
         0x84,
         0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58,
         0xcf,
         0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f,
         0xa8,
         0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3,
         0xd2,
         0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
         0x73,
         0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b,
         0xdb,
         0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4,
         0x79,
         0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae,
         0x08,
         0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b,
         0x8a,
         0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d,
         0x9e,
         0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28,
         0xdf,
         0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb,
         0x16]
    lst = [i for i in range(len(S)) if ((S[i] >> 7) & 1) == 1]
    print(lst)
    lst.sort()
    result = []
    min = 10000
    for i in lst:
        sum = 0
        for j in lst:
            sum += hanming(i, j)
        result.append(sum)
        if min > sum:
            min = sum
    print(min)
    print(lst)
    print(result)

if __name__ == "__main__" :
    f1()
    # sbox = Sbox(K = 0.356, A = 4, KStep = 0.001)
    # X0, newSbox = sbox.start()
    # print(X0)
    # print(newSbox)