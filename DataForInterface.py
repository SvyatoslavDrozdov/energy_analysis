from CrystalDynamics.CoreCalculation.Core import InputData
from Decoder import transformation
import numpy as np

[a, m, C1, C2, C3] = [0, 0, 0, 0, 0]


def Data(choice, U, ChainParameters):
    global U_disp
    U_disp = U
    global a
    global m
    global C1
    global C2
    global C3
    C1 = ChainParameters[2]
    C2 = ChainParameters[3]
    C3 = ChainParameters[4]
    Info = InputData(ChainParameters)
    V_0 = Info[1]
    PotentialEnergy = Info[3]
    EndTime = Info[4]
    tau = Info[5]
    N = Info[6]
    m = Info[7]
    a = Info[8]

    TimeIterationEnd = int(EndTime / tau)
    Time = tau * np.arange(0, TimeIterationEnd - 1)

    if C2 == 0 and C3 == 0:
        ChainType = 1
    elif C3 == 0 and C2 != 0:
        ChainType = 2
    else:
        ChainType = 3

    def F(Deformation):
        match ChainType:
            case 1:
                FF = C1 * Deformation
                return FF
            case 2:
                FF = C1 * (Deformation + C2 * Deformation ** 2)
                return FF
            case 3:
                FF = C1 * (Deformation + C2 * Deformation ** 2 + C3 * Deformation ** 3)
                return FF

    def Force(Deformation):
        force = F(Deformation)
        return force

    def EpsParticle(TimeIter, n):
        epsilon = U[TimeIter][n + 1] - U[TimeIter][n]
        return epsilon

    def Epsilon():
        Deformation = np.array([])
        # for TimeIter in range(0, TimeIterationEnd + 1):
        for TimeIter in range(0, TimeIterationEnd):
            for n in range(0, N - 1):
                Deformation = np.append(Deformation, EpsParticle(TimeIter, n))
        Deformation = Deformation.reshape(TimeIterationEnd, N - 1)
        return Deformation

    def sum(A):
        S = np.array([])
        # for TimeIter in range(0, TimeIterationEnd + 1):
        for TimeIter in range(0, TimeIterationEnd - 1):
            add = 0
            for i in range(0, len(A[TimeIter])):
                add += A[TimeIter][i]
            S = np.append(S, add)
        return S

    def PotEn(TimeIter, n):
        if n == 0:
            PE = 0.5 * PotentialEnergy(U[TimeIter][1] - U[TimeIter][0])
        elif n == N - 1:
            PE = 0.5 * PotentialEnergy(U[TimeIter][N - 1] - U[TimeIter][N - 2])
        else:
            PE = 0.5 * PotentialEnergy(U[TimeIter][n] - U[TimeIter][n - 1]) + 0.5 * PotentialEnergy(
                U[TimeIter][n + 1] - U[TimeIter][n])
        return PE

    def PotentialEnergyArray():
        Array = np.array([])
        for TimeIter in range(0, TimeIterationEnd + 1):
            for n in range(0, N - 1):
                Array = np.append(Array, PotEn(TimeIter, n))
        return Array.reshape(TimeIterationEnd + 1, N - 1)

    def SpringsEnergy():
        SP = PotentialEnergy(Epsilon())
        return SP

    def PotentialEnergyOfChain():
        Potential = np.array([])
        # for TimeIter in range(0, TimeIterationEnd + 1):
        for TimeIter in range(0, TimeIterationEnd):
            P = 0
            for n in range(0, N):
                P += PotEn(TimeIter, n)
            Potential = np.append(Potential, [P])
        # Potential = Potential.reshape(TimeIterationEnd + 1, 1)
        return Potential

    def Velocity(TimeIter, n):
        if TimeIter == 0:
            Vel = V_0[n]
        elif TimeIter == TimeIterationEnd:
            Vel = (U[TimeIter][n] - U[TimeIter - 1][n]) / tau
        else:
            Vel = (U[TimeIter + 1][n] - U[TimeIter - 1][n]) / (2 * tau)
        return Vel

    def VelocityArray():
        Array = np.array([])
        for TimeIter in range(0, TimeIterationEnd + 1):
            for n in range(0, N):
                Array = np.append(Array, Velocity(TimeIter, n))
        return Array.reshape(TimeIterationEnd + 1, N)

    def KinEn(TimeIter, n):
        KE = m * Velocity(TimeIter, n) ** 2 / 2
        return KE

    def KineticEnergyArray():
        Array = np.array([])
        for TimeIter in range(0, TimeIterationEnd + 1):
            for n in range(0, N):
                Array = np.append(Array, KinEn(TimeIter, n))
        return Array.reshape(TimeIterationEnd + 1, N)

    def KineticEnergy(TimeIter):
        KE = 0
        for n in range(0, N):
            KE += KinEn(TimeIter, n)
        return KE

    def KineticEnergyOfChain():
        Kinetic = np.array([])
        # for TimeIter in range(0, TimeIterationEnd + 1):
        for TimeIter in range(0, TimeIterationEnd):
            K = 0
            for n in range(0, N):
                K += KinEn(TimeIter, n)
            Kinetic = np.append(Kinetic, [K])
        # Kinetic = Kinetic.reshape(TimeIterationEnd + 1, 1)
        return Kinetic

    def Energy(TimeIter, n):
        En = PotEn(TimeIter, n) + KinEn(TimeIter, n)
        return En

    InitialEnergy = 0
    for k in range(0, N):
        InitialEnergy += Energy(0, k)

    def StandardEnergyCenter(TimeIter):
        SEC = 0
        for n in range(0, N):
            SEC += a * n * Energy(TimeIter, n)
        SEC = SEC / InitialEnergy
        return SEC

    def EnergyCenter_St():
        EnergyCenter = np.array(StandardEnergyCenter(0))
        for TimeIteration in range(1, TimeIterationEnd + 1):
            EnergyCenter = np.append(EnergyCenter, [StandardEnergyCenter(TimeIteration)])
        return EnergyCenter

    def FullEnergyCenter(TimeIter):
        FEC = 0
        for n in range(0, N):
            FEC += (a * n + U[TimeIter][n]) * Energy(TimeIter, n)
        FEC = FEC / InitialEnergy
        return FEC

    def EnergyCenter_Full():
        EnergyCenter = np.array(FullEnergyCenter(0)).reshape(1, 1)
        for TimeIteration in range(1, TimeIterationEnd + 1):
            EnergyCenter = np.append(EnergyCenter, [FullEnergyCenter(TimeIteration)])
        return EnergyCenter

    def Pulse(TimeIter, n):
        p = m * Velocity(TimeIter, n)
        return p

    InitialPulse = 0
    for k in range(0, N):
        InitialPulse += m * Velocity(0, k)

    def StandardPulseCenter(TimeIter):
        M = 0
        for n in range(0, N):
            M += a * n * Pulse(TimeIter, n)
        Center = M / InitialPulse
        return Center

    def Pulse_St():
        Pls = np.array(StandardPulseCenter(0)).reshape(1, 1)
        for TimeIter in range(1, TimeIterationEnd + 1):
            Pls = np.append(Pls, [StandardPulseCenter(TimeIter)])
        return Pls

    def FullPulseCenter(TimeIter):
        M = 0
        for n in range(0, N):
            M += (a * n + U[TimeIter][n]) * Pulse(TimeIter, n)
        Center = M / InitialPulse
        return Center

    def Pulse_Full():
        Pls = np.array(FullPulseCenter(0)).reshape(1, 1)
        for TimeIter in range(1, TimeIterationEnd + 1):
            Pls = np.append(Pls, [FullPulseCenter(TimeIter)])
        return Pls

    def Derivative(Func, TimeIter):
        try:
            df_dt = (Func[TimeIter + 1] - Func[TimeIter - 1]) / (2 * tau)
        except:
            try:
                df_dt = (Func[TimeIter + 1] - Func[TimeIter]) / tau
            except:
                df_dt = (Func[TimeIter] - Func[TimeIter - 1]) / tau
        return df_dt

    def DerivativeFunction(Func):
        df_dt = np.array([])
        for TimeIter in range(0, len(Func) - 1):
            df_dt = np.append(df_dt, Derivative(Func, TimeIter))
        return df_dt

    def Sum(Text):
        global a
        global m
        global C1
        global C2
        global C3
        global U_disp

        Array = np.array([])

        SE = SpringsEnergy()[:len(Time)]
        Kin = KineticEnergyArray()[:len(Time)]
        Pot = PotentialEnergyArray()[:len(Time)]
        Eps = Epsilon()[:len(Time)]
        For = Force(Eps)[:len(Time)]
        u = U_disp[:len(Time)]
        v = VelocityArray()[:len(Time)]

        for TimeIter in range(0, TimeIterationEnd + 1):
            try:
                S = 0
                for n in range(0, N):
                    try:
                        S += eval(Text)
                    except:
                        pass
                Array = np.append(Array, S)
            except:
                pass
        Array = Array[:len(Time)]
        return Array

    match choice:
        case "Full Energy":
            FullEnergy = np.array([])
            for time in range(0, TimeIterationEnd - 1):
                W = 0
                for k in range(0, N):
                    W += Energy(time, k)
                FullEnergy = np.append(FullEnergy, W)
            X = Time
            Y = FullEnergy
            return [X, Y]
        case "Standard Energy Center":
            X = Time
            Y = EnergyCenter_St()
            Y = Y[:len(Y) - 2]
            return [X, Y]
        case "Full Energy Center":
            X = Time
            Y = EnergyCenter_Full()
            Y = Y[:len(Y) - 2]
            return [X, Y]
        case "Standard Pulse Center":
            X = Time
            Y = Pulse_St()
            Y = Y[:len(Y) - 2]
            return [X, Y]
        case "Full Pulse Center":
            X = Time
            Y = Pulse_Full()
            Y = Y[:len(Y) - 2]
            return [X, Y]
        case "Velocity of Standard Pulse center":
            X = Time[1:]
            Fun = Pulse_St()
            Y = DerivativeFunction(Fun)
            Y = Y[1:len(Y) - 1]
            return [X, Y]
        case "Velocity of Full Pulse center":
            X = Time[1:]
            Fun = Pulse_Full()
            Y = DerivativeFunction(Fun)
            Y = Y[1:len(Y) - 1]
            return [X, Y]
        case "Velocity of Standard Energy Center":
            X = Time[1:]
            Fun = EnergyCenter_St()
            Y = DerivativeFunction(Fun)
            Y = Y[1:len(Y) - 1]
            return [X, Y]
        case "Velocity of Full Energy Center":
            X = Time[1:]
            Fun = EnergyCenter_Full()
            Y = DerivativeFunction(Fun)
            Y = Y[1:len(Y) - 1]
            return [X, Y]
        case "Acceleration of St Energy Center":
            X = Time[2:len(Time) - 1]
            Fun = EnergyCenter_St()
            Fun2 = DerivativeFunction(Fun)
            # Y = Fun2
            Y = DerivativeFunction(Fun2)
            Y = Y[2:len(Y) - 1]
            return [X, Y]
        case "Acceleration of Full Energy Center":
            X = Time[2:len(Time) - 1]
            Fun = EnergyCenter_Full()
            Fun2 = DerivativeFunction(Fun)
            # Y = Fun2
            Y = DerivativeFunction(Fun2)
            Y = Y[2:len(Y) - 1]
            return [X, Y]
        case "Manual Function One":
            # print(Sum("Eps[TimeIter][n])"))
            Kin = KineticEnergyOfChain()[:len(Time)]
            Pot = PotentialEnergyOfChain()[:len(Time)]
            Eps = Epsilon()[:len(Time)]
            For = Force(Eps)[:len(Time)]

            ManFuncOne = ChainParameters[8]
            ManFuncOne = transformation(ManFuncOne)

            print(ManFuncOne)
            Y = eval(ManFuncOne)
            Y = Y[:len(Time)]
            X = Time
            return [X, Y]

        case "Manual Function Two":
            Kin = KineticEnergyOfChain()[:len(Time)]
            Pot = PotentialEnergyOfChain()[:len(Time)]
            Eps = Epsilon()[:len(Time)]
            For = Force(Eps)[:len(Time)]

            ManFuncTwo = ChainParameters[9]
            ManFuncTwo = transformation(ManFuncTwo)

            Y = eval(ManFuncTwo)
            Y = Y[:len(Time)]
            X = Time
            return [X, Y]

        case "Manual Function Three":
            Kin = KineticEnergyOfChain()[:len(Time)]
            Pot = PotentialEnergyOfChain()[:len(Time)]
            Eps = Epsilon()[:len(Time)]
            For = Force(Eps)[:len(Time)]

            ManFuncThree = ChainParameters[10]
            ManFuncThree = transformation(ManFuncThree)

            Y = eval(ManFuncThree)
            Y = Y[:len(Time)]
            X = Time
            return [X, Y]
