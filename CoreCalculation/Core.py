import numpy as np


def InputData(ChainParameters):
    a = ChainParameters[0]
    m = ChainParameters[1]
    C1 = ChainParameters[2]
    C2 = ChainParameters[3]
    C3 = ChainParameters[4]
    N = ChainParameters[5]
    EndTime = ChainParameters[6]
    tau = ChainParameters[7]

    U_0 = ChainParameters[11]
    V_0 = ChainParameters[12]
    # U_0 = np.zeros(N)
    # V_0 = np.zeros(N)
    # V_0[int(N / 2) - 1] = 1
    # U_0[int(N / 2)] = 1
    # V_0[int(N / 2) + 1] = -1.5
    # V_0[int(N / 2)] = 1

    if C2 == 0 and C3 == 0:
        ChainType = 1
    elif C3 == 0 and C2 != 0:
        ChainType = 2
    else:
        ChainType = 3

    def F(Deformation):
        match ChainType:
            case 1:
                Force = C1 * Deformation
                return Force
            case 2:
                Force = C1 * (Deformation + C2 * Deformation ** 2)
                return Force
            case 3:
                Force = C1 * (Deformation + C2 * Deformation ** 2 + C3 * Deformation ** 3)
                return Force

    def PotentialEnergy(Deformation):
        match ChainType:
            case 1:
                PotEn = C1 * Deformation ** 2 / 2
                return PotEn
            case 2:
                PotEn = C1 * Deformation ** 2 / 2 + C1 * C2 * Deformation ** 3 / 3
                return PotEn
            case 3:
                PotEn = C1 * Deformation ** 2 / 2 + C1 * C2 * Deformation ** 3 / 3 + C1 * C3 * Deformation ** 4 / 4
                return PotEn

    Information = [U_0, V_0, F, PotentialEnergy, EndTime, tau, N, m, a]
    return Information


def Solution(ChainParameters):
    Info = InputData(ChainParameters)
    U_0 = Info[0]
    V_0 = Info[1]
    F = Info[2]
    EndTime = Info[4]
    tau = Info[5]
    N = Info[6]
    m = Info[7]

    U = U_0.reshape(1, N)

    def Acceleration(TimeIter):
        Acc = np.array([])

        w_first = F(U[TimeIter][1] - U[TimeIter][0]) / m
        Acc = np.append(Acc, w_first)

        for n in range(1, N - 1):
            w = (F(U[TimeIter][n + 1] - U[TimeIter][n]) - F(U[TimeIter][n] - U[TimeIter][n - 1])) / m
            Acc = np.append(Acc, w)

        w_last = - F(U[TimeIter][N - 1] - U[TimeIter][N - 2]) / m
        Acc = np.append(Acc, w_last)

        return Acc

    W = np.array(Acceleration(0)).reshape(1, N)
    U_tau = U[0] + V_0 * tau + W[0] * tau ** 2 / 2
    U = np.append(U, [U_tau], axis=0)
    W = np.append(W, [Acceleration(1)], axis=0)

    def Displacement(TimeIter):
        Dis = 2 * U[TimeIter - 1] - U[TimeIter - 2] + W[TimeIter - 1] * tau ** 2
        return Dis

    TimeIterationEnd = int(EndTime / tau)

    for time in range(2, TimeIterationEnd + 1):
        U = np.append(U, [Displacement(time)], axis=0)
        W = np.append(W, [Acceleration(time)], axis=0)
    return U
