import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from DataForInterface import Data
from CrystalDynamics.CoreCalculation.Core import Solution
import random as random
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")

DefinedNumbers = 0
GlobalInitialU = []
GlobalFlag = False

DefinedNumbersV = 0
GlobalInitialV = []
GlobalFlagV = False


def LocalDecoder(Text, Numbers):
    N = Numbers
    CommaNumber = Text.find(",")
    if CommaNumber == -1:
        return [int(eval(Text))]
    else:
        N1 = int(eval(Text[:CommaNumber]))
        N2 = int(eval(Text[CommaNumber + 1:]))
        return [N1, N2]


def AddInitialCondition():
    global DefinedNumbers
    global GlobalInitialU
    global GlobalFlag

    if entryU_numbers.get() != "":
        if GlobalFlag:
            if entry_N.get() != "":
                if len(GlobalInitialU) != int(entry_N.get()):
                    GlobalFlag = False
            else:
                if len(GlobalInitialU) != 30:
                    GlobalFlag = False

        if not GlobalFlag:
            try:
                N = int(entry_N.get())
            except:
                N = 30
            GlobalFlag = True
            GlobalInitialU = np.zeros(N)

        N = len(GlobalInitialU)
        DefinedNumbers = LocalDecoder(entryU_numbers.get(), N)

        Command = entryU_define.get()
        Addition = eval(Command)

        if len(DefinedNumbers) == 1:
            GlobalInitialU[DefinedNumbers] = Addition
        else:
            for n in range(DefinedNumbers[0], DefinedNumbers[1] + 1):
                GlobalInitialU[n] = Addition[n - DefinedNumbers[0]]

        print(GlobalInitialU)

    if entryV_numbers.get() != "":
        global DefinedNumbersV
        global GlobalInitialV
        global GlobalFlagV

        if GlobalFlagV:
            if entry_N.get() != "":
                if len(GlobalInitialV) != int(entry_N.get()):
                    GlobalFlagV = False
            else:
                if len(GlobalInitialV) != 30:
                    GlobalFlagV = False

        if not GlobalFlagV:
            try:
                N = int(entry_N.get())
            except:
                N = 30
            GlobalFlagV = True
            GlobalInitialV = np.zeros(N)

        N = len(GlobalInitialV)
        DefinedNumbersV = LocalDecoder(entryV_numbers.get(), N)

        Command = entryV_define.get()
        Addition = eval(Command)

        if len(DefinedNumbersV) == 1:
            GlobalInitialV[DefinedNumbersV] = Addition
        else:
            for n in range(DefinedNumbersV[0], DefinedNumbersV[1] + 1):
                GlobalInitialV[n] = Addition[n - DefinedNumbersV[0]]
        print(GlobalInitialV)

def Plot():
    global GlobalInitialU
    global GlobalFlag
    global GlobalInitialV
    global GlobalFlagV

    try:
        a = float(entry_a.get())
    except:
        a = 1
    try:
        m = float(entry_m.get())
    except:
        m = 1
    try:
        C1 = float(entry_C1.get())
    except:
        C1 = 1
    try:
        C2 = float(entry_C2.get())
    except:
        C2 = 0
    try:
        C3 = float(entry_C3.get())
    except:
        C3 = 0
    try:
        N = int(entry_N.get())
    except:
        N = 30
    try:
        Time = float(entry_Time.get())
    except:
        Time = 10
    try:
        tau = float(entry_tau.get())
    except:
        tau = 0.1

    if not GlobalFlag:
        GlobalInitialU = np.zeros(N)
        GlobalInitialU[int(N / 2)] = 1
    if not GlobalFlagV:
        GlobalInitialV = np.zeros(N)
        GlobalInitialV[int(N / 2)-1] = 1
        GlobalInitialV[int(N / 2)] = 0.5
        GlobalInitialV[int(N / 2) + 1] = -1

    ChainParameters = [a, m, C1, C2, C3, N, Time, tau, "", "", "", GlobalInitialU, GlobalInitialV]
    U = Solution(ChainParameters)
    plt.close()

    EnCenterStFlag = EnergyCenterStSwitch()
    EnCenterFullFlag = EnergyCenterFullSwitch()
    PlCenterStFlag = PulseCenterStSwitch()
    PulseCenterFullFlag = PulseCenterFullSwitch()
    PulseCenterStVelocityFlag = PulseCenterStVelocitySwitch()
    PulseCenterFullVelocityFlag = PulseCenterFullVelocitySwitch()
    FullEnergyFlag = FullEnergySwitch()
    EnergyCenterStVelocityFlag = EnergyCenterStVelocitySwitch()
    EnergyCenterFullVelocityFlag = EnergyCenterFullVelocitySwitch()
    EnergyCenterStAccelerationFlag = EnergyCenterStAccelerationSwitch()
    EnergyCenterFullAccelerationFlag = EnergyCenterFullAccelerationSwitch()

    ManFuncOne = ManualFunctionOne.get()
    ManFuncTwo = ManualFunctionTwo.get()
    ManFuncThree = ManualFunctionThree.get()
    if EnCenterStFlag == 1:
        [X, Y] = Data("Standard Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Standard Energy Center")

    if EnCenterFullFlag == 1:
        [X, Y] = Data("Full Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Full Energy Center")

    if PlCenterStFlag == 1:
        [X, Y] = Data("Standard Pulse Center", U, ChainParameters)
        plt.plot(X, Y, label="Standard Pulse Center")

    if PulseCenterFullFlag == 1:
        [X, Y] = Data("Full Pulse Center", U, ChainParameters)
        plt.plot(X, Y, label="Full Pulse Center")

    if PulseCenterStVelocityFlag == 1:
        [X, Y] = Data("Velocity of Standard Pulse center", U, ChainParameters)
        plt.plot(X, Y, label="Velocity of Standard Pulse center")

    if PulseCenterFullVelocityFlag == 1:
        [X, Y] = Data("Velocity of Full Pulse center", U, ChainParameters)
        plt.plot(X, Y, label="Velocity of Full Pulse center")

    if FullEnergyFlag == 1:
        [X, Y] = Data("Full Energy", U, ChainParameters)
        plt.plot(X, Y, label="Full energy")

    if EnergyCenterStVelocityFlag == 1:
        [X, Y] = Data("Velocity of Standard Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Velocity of Standard Energy Center")

    if EnergyCenterFullVelocityFlag == 1:
        [X, Y] = Data("Velocity of Full Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Velocity of Full Energy Center")
    if EnergyCenterStAccelerationFlag == 1:
        [X, Y] = Data("Acceleration of St Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Acceleration of St Energy Center")

    if EnergyCenterFullAccelerationFlag == 1:
        [X, Y] = Data("Acceleration of Full Energy Center", U, ChainParameters)
        plt.plot(X, Y, label="Acceleration of Full Energy Center")

    if ManFuncOne != "":
        ChainParameters[8] = ManFuncOne
        [X, Y] = Data("Manual Function One", U, ChainParameters)
        # plt.plot(X, Y, label=f"{ManFuncOne}")
        plt.plot(X, Y, label="Manual function 1")

    if ManFuncTwo != "":
        ChainParameters[9] = ManFuncTwo
        [X, Y] = Data("Manual Function Two", U, ChainParameters)
        # plt.plot(X, Y, label=f"{ManFuncTwo}")
        plt.plot(X, Y, label="Manual function 2")

    if ManFuncThree != "":
        ChainParameters[10] = ManFuncThree
        [X, Y] = Data("Manual Function Three", U, ChainParameters)
        # plt.plot(X, Y, label=f"{ManFuncThree}")
        plt.plot(X, Y, label="Manual function 3")
    Y_lower_str = entry_y_lower.get()
    Y_upper_str = entry_y_upper.get()
    if Y_lower_str != '':
        Y_lower = float(Y_lower_str)
        Y_upper = float(Y_upper_str)
        plt.ylim(Y_lower, Y_upper)

    StartTime_str = entry_StartTime.get()
    EndTime_str = entry_EndTime.get()
    # Time = float(entry_Time.get())
    if StartTime_str != '':
        StartTime = float(StartTime_str)
    else:
        StartTime = 0
    if EndTime_str != '':
        EndTime = float(EndTime_str)
    else:
        EndTime = Time
    plt.xlim(StartTime, EndTime)

    plt.legend()
    plt.show()


def EnergyCenterStSwitch():
    EnCenterSt = EnergyCenterSt.get()
    if EnCenterSt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def EnergyCenterFullSwitch():
    EnCenterFull = EnergyCenterFull.get()
    if EnCenterFull == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def PulseCenterStSwitch():
    PlCenterSt = PulseCenterSt.get()
    if PlCenterSt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def PulseCenterFullSwitch():
    PlCenterFull = PulseCenterFull.get()
    if PlCenterFull == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def PulseCenterStVelocitySwitch():
    dPlCenterSt_dt = PulseCenterStVelocity.get()
    if dPlCenterSt_dt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def PulseCenterFullVelocitySwitch():
    dPlCenterFull_dt = PulseCenterFullVelocity.get()
    if dPlCenterFull_dt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def FullEnergySwitch():
    Energy = FullEnergy.get()
    if Energy == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def EnergyCenterStVelocitySwitch():
    dEnCentSt_dt = EnergyCenterStVelocity.get()
    if dEnCentSt_dt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def EnergyCenterFullVelocitySwitch():
    dEnCentFull_dt = EnergyCenterFullVelocity.get()
    if dEnCentFull_dt == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def EnergyCenterStAccelerationSwitch():
    d2E_St_center_dt2 = EnergyCenterStAcceleration.get()
    if d2E_St_center_dt2 == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


def EnergyCenterFullAccelerationSwitch():
    d2E_Full_center_dt2 = EnergyCenterFullAcceleration.get()
    if d2E_Full_center_dt2 == 1:
        Flag = 1
    else:
        Flag = 0
    return Flag


window = ctk.CTk()
window.title('Interface')
window.resizable(False, False)
Height = 580
Wight = 1100
window.geometry(f'{Wight}x{Height}')

X1 = 30
X2 = 250
Y1 = 10
Y2 = 60
dY = 50
dX = 25
Y3 = Y2 + 6 * dY
StandardWidth = 80
StandardWidth2 = 120
X3 = X2 + 2 * StandardWidth + 2 * dX
X4 = X3 + 2 * StandardWidth + 2 * dX
X5 = X4 + 2 * StandardWidth + 2 * dX
# FIRST COLUMN -------------------------------------------------------------------------------------------------------
ctk.CTkLabel(window, text="Параметры цепочки", text_color='white', fg_color="#7F55F2", width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y1)

ctk.CTkLabel(window, text="a =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2)
entry_a = ctk.CTkEntry(window, width=StandardWidth)
entry_a.place(x=X1 + StandardWidth + dX, y=Y2)

ctk.CTkLabel(window, text="m =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2 + dY)
entry_m = ctk.CTkEntry(window, width=StandardWidth)
entry_m.place(x=X1 + StandardWidth + dX, y=Y2 + dY)

ctk.CTkLabel(window, text="C_1=", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2 + 2 * dY)
entry_C1 = ctk.CTkEntry(window, width=StandardWidth)
entry_C1.place(x=X1 + StandardWidth + dX, y=Y2 + 2 * dY)

ctk.CTkLabel(window, text="С_2 =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2 + 3 * dY)
entry_C2 = ctk.CTkEntry(window, width=StandardWidth)
entry_C2.place(x=X1 + StandardWidth + dX, y=Y2 + 3 * dY)

ctk.CTkLabel(window, text="С_3 =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2 + 4 * dY)
entry_C3 = ctk.CTkEntry(window, width=StandardWidth)
entry_C3.place(x=X1 + StandardWidth + dX, y=Y2 + 4 * dY)

ctk.CTkLabel(window, text="N =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1, y=Y2 + 5 * dY)
entry_N = ctk.CTkEntry(window, width=StandardWidth)
entry_N.place(x=X1 + StandardWidth + dX, y=Y2 + 5 * dY)

ctk.CTkLabel(window, text="Длительность колебаний", text_color='white', fg_color="#7F55F2",
             width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y2 + 6 * dY)

ctk.CTkLabel(window, text="Time = ", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1,
                                                                                                      y=Y2 + 7 * dY)
entry_Time = ctk.CTkEntry(window, width=StandardWidth)
entry_Time.place(x=X1 + StandardWidth + dX, y=Y2 + 7 * dY)

ctk.CTkLabel(window, text="Шаг интегрирования", text_color='white', fg_color="#7F55F2", width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y2 + 8 * dY)

ctk.CTkLabel(window, text="tau = ", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X1,
                                                                                                     y=Y2 + 9 * dY)
entry_tau = ctk.CTkEntry(window, width=StandardWidth)
entry_tau.place(x=X1 + StandardWidth + dX, y=Y2 + 9 * dY)

# ---------------------------------------------------------------------------------------------------------------------

# SECOND COLUMN -------------------------------------------------------------------------------------------------------
ctk.CTkLabel(window, text="Функции f(t)", text_color='white', fg_color="#7F55F2", width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X2, y=Y1)

ctk.CTkLabel(window, text="Energy center St", fg_color="#0066CC", width=StandardWidth2, corner_radius=10).place(x=X2,
                                                                                                                y=Y2)
EnergyCenterSt = ctk.CTkSwitch(window, text="")
EnergyCenterSt.place(x=X2 + StandardWidth2 + dX, y=Y2)

ctk.CTkLabel(window, text="Energy center Full", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X2, y=Y2 + dY)
EnergyCenterFull = ctk.CTkSwitch(window, text="")
EnergyCenterFull.place(x=X2 + StandardWidth2 + dX, y=Y2 + dY)

ctk.CTkLabel(window, text="Pulse center St", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X2, y=Y2 + 2 * dY)
PulseCenterSt = ctk.CTkSwitch(window, text="")
PulseCenterSt.place(x=X2 + StandardWidth2 + dX, y=Y2 + 2 * dY)

ctk.CTkLabel(window, text="Pulse center Full", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X2, y=Y2 + 3 * dY)
PulseCenterFull = ctk.CTkSwitch(window, text="")
PulseCenterFull.place(x=X2 + StandardWidth2 + dX, y=Y2 + 3 * dY)

ctk.CTkLabel(window, text="Full Energy", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X2, y=Y2 + 4 * dY)
FullEnergy = ctk.CTkSwitch(window, text="")
FullEnergy.place(x=X2 + StandardWidth2 + dX, y=Y2 + 4 * dY)

# ---------------------------------- MANUAL FUNCTIONS -----------------------------------------------------------------

ctk.CTkLabel(window, text="Manual functions", text_color='white', fg_color="#7F55F2",
             width=4 * StandardWidth + 3 * dX,
             corner_radius=10).place(x=X2, y=Y2 + 6 * dY)

ctk.CTkLabel(window, text="F(t) =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X2,
                                                                                                     y=Y2 + 7 * dY)
ManualFunctionOne = ctk.CTkEntry(window, width=3 * StandardWidth + 2 * dX)
ManualFunctionOne.place(x=X2 + StandardWidth + dX, y=Y2 + 7 * dY)

ctk.CTkLabel(window, text="G(t) =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X2,
                                                                                                     y=Y2 + 8 * dY)
ManualFunctionTwo = ctk.CTkEntry(window, width=3 * StandardWidth + 2 * dX)
ManualFunctionTwo.place(x=X2 + StandardWidth + dX, y=Y2 + 8 * dY)

ctk.CTkLabel(window, text="H(t) =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X2,
                                                                                                     y=Y2 + 9 * dY)
ManualFunctionThree = ctk.CTkEntry(window, width=3 * StandardWidth + 2 * dX)
ManualFunctionThree.place(x=X2 + StandardWidth + dX, y=Y2 + 9 * dY)

# ---------------------------------------------------------------------------------------------------------------------

# THIRD COLUMN --------------------------------------------------------------------------------------------------------
ctk.CTkLabel(window, text="Производные df(t) / dt", text_color='white', fg_color="#7F55F2",
             width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X3, y=Y1)

ctk.CTkLabel(window, text="En. Velocity St", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X3, y=Y2)
EnergyCenterStVelocity = ctk.CTkSwitch(window, text="")
EnergyCenterStVelocity.place(x=X3 + StandardWidth2 + dX, y=Y2)

ctk.CTkLabel(window, text="En. Velocity Full", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X3, y=Y2 + dY)
EnergyCenterFullVelocity = ctk.CTkSwitch(window, text="")
EnergyCenterFullVelocity.place(x=X3 + StandardWidth2 + dX, y=Y2 + dY)

ctk.CTkLabel(window, text="Pulse Velocity St", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X3, y=Y2 + 2 * dY)
PulseCenterStVelocity = ctk.CTkSwitch(window, text="")
PulseCenterStVelocity.place(x=X3 + StandardWidth2 + dX, y=Y2 + 2 * dY)

ctk.CTkLabel(window, text="Pulse Velocity Full", fg_color="#0066CC",
             width=StandardWidth2, corner_radius=10).place(x=X3, y=Y2 + 3 * dY)
PulseCenterFullVelocity = ctk.CTkSwitch(window, text="")
PulseCenterFullVelocity.place(x=X3 + StandardWidth2 + dX, y=Y2 + 3 * dY)

# ---------------------------------------------------------------------------------------------------------------------

# FORTH COLUMN --------------------------------------------------------------------------------------------------------
ctk.CTkLabel(window, text="Производные d^2 f(t) / dt^2", text_color='white', fg_color="#7F55F2",
             width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X4, y=Y1)

ctk.CTkLabel(window, text="En. Acceleration St", fg_color="#0066CC",
             width=int(1.1 * StandardWidth2), corner_radius=10).place(x=X4, y=Y2)
EnergyCenterStAcceleration = ctk.CTkSwitch(window, text="")
EnergyCenterStAcceleration.place(x=X4 + StandardWidth2 + dX, y=Y2)

ctk.CTkLabel(window, text="En. Acceleration Full", fg_color="#0066CC",
             width=int(1.1 * StandardWidth2), corner_radius=10).place(x=X4, y=Y2 + dY)
EnergyCenterFullAcceleration = ctk.CTkSwitch(window, text="")
EnergyCenterFullAcceleration.place(x=X4 + StandardWidth2 + dX, y=Y2 + dY)

# Initial condition ---------------------------------------------------------------------------------------------------

ctk.CTkLabel(window, text="Initial condition", text_color='white', fg_color="#7F55F2",
             width=4 * StandardWidth + 3 * dX,
             corner_radius=10).place(x=X4, y=Y3)

ctk.CTkLabel(window, text="U:", fg_color="#0066CC", width=int(StandardWidth / 3), corner_radius=10).place(x=X4,
                                                                                                          y=Y3 + dY)

entryU_numbers = ctk.CTkEntry(window, width=int(0.8 * StandardWidth))
entryU_numbers.place(x=X4 + int(StandardWidth / 3) + int(0.45 * dX), y=Y3 + dY)

entryU_define = ctk.CTkEntry(window, width=3 * StandardWidth + 2 * dX)
entryU_define.place(x=X4 + int(StandardWidth / 3) + int(3.2 * dX), y=Y3 + dY)

ctk.CTkLabel(window, text="V:", fg_color="#0066CC", width=int(StandardWidth / 3), corner_radius=10).place(x=X4,
                                                                                                          y=Y3 + 2 * dY)

entryV_numbers = ctk.CTkEntry(window, width=int(0.8 * StandardWidth))
entryV_numbers.place(x=X4 + int(StandardWidth / 3) + int(0.45 * dX), y=Y3 + 2 * dY)

entryV_define = ctk.CTkEntry(window, width=3 * StandardWidth + 2 * dX)
entryV_define.place(x=X4 + int(StandardWidth / 3) + int(3.2 * dX), y=Y3 + 2 * dY)

EnterIC = ctk.CTkButton(window, width=3 * StandardWidth + 2 * dX, text='Add initial condition', fg_color="#418433",
                        hover_color="#1F4618", command=AddInitialCondition)
EnterIC.place(x=X4 + int(StandardWidth / 3) + int(3.2 * dX), y=Y3 + 3 * dY)

# ---------------------------------------------------------------------------------------------------------------------

# FIFTH COLUMN --------------------------------------------------------------------------------------------------------
ctk.CTkLabel(window, text="Параметры отображения", text_color='white', fg_color="#7F55F2", width=2 * StandardWidth + dX,
             corner_radius=10).place(x=X5, y=Y1)

ctk.CTkLabel(window, text="Start time =", fg_color="#0066CC", width=StandardWidth,
             corner_radius=10).place(x=X5, y=Y2)
entry_StartTime = ctk.CTkEntry(window, width=StandardWidth)
entry_StartTime.place(x=X5 + StandardWidth + dX, y=Y2)

ctk.CTkLabel(window, text="End time =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X5,
                                                                                                         y=Y2 + dY)
entry_EndTime = ctk.CTkEntry(window, width=StandardWidth)
entry_EndTime.place(x=X5 + StandardWidth + dX, y=Y2 + dY)

ctk.CTkLabel(window, text="Y limit =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(x=X5,
                                                                                                        y=Y2 + 2 * dY)
entry_y_lower = ctk.CTkEntry(window, width=int(StandardWidth / 2))
entry_y_lower.place(x=X5 + StandardWidth + dX, y=Y2 + 2 * dY)

entry_y_upper = ctk.CTkEntry(window, width=int(StandardWidth / 2))
entry_y_upper.place(x=X5 + int(StandardWidth * 1.8), y=Y2 + 2 * dY)
# ---------------------------------------------------------------------------------------------------------------------

btn_interval = ctk.CTkButton(window, width=StandardWidth + int(0.88 * dX), text='Calculate', command=Plot,
                             fg_color="#418433", hover_color="#1F4618")
btn_interval.place(x=X4, y=Y3 + 3 * dY)

window.mainloop()
