def transformation(ManFunc):
    ManFunc = ManFunc.replace("t", "Time")
    ManFunc = ManFunc.replace(" ", "")
    ManFunc = ManFunc.replace("K", "Kin")
    ManFunc = ManFunc.replace("P", "Pot")
    ManFunc = ManFunc.replace("C_1", "C1")
    ManFunc = ManFunc.replace("C_2", "C2")
    ManFunc = ManFunc.replace("C_3", "C3")
    ManFunc = ManFunc.replace("F", "For")
    ManFunc = ManFunc.replace("_n", "")
    ManFunc = ManFunc.replace("p_0", "InitialPulse")
    # ------------------------------------------------
    if "[" in ManFunc:

        ManFunc = ManFunc.replace("[n", "[TimeIter][n")
        ManFunc = ManFunc.replace("{", """('""")
        ManFunc = ManFunc.replace("}", """')""")

    return ManFunc
