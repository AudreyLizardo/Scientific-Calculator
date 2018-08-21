'''
Title: Python Calculator
Author: Ching Chang
Date Created: May 16th, 2018
'''

def decimal(num):
    num = list(str(num))
    if "." in num:
        count = 0
        n = num.index(".") + 1

        #------Move the Decimal to the Right------#
        while n < len(num):

            #----Count How Many Places the Decimal Moved----#
            count += 1
            n += 1

        return count
    else:
        return 0

def digits(num):
    num = list(str(num))
    if "." in num:
        num.remove(".")
    if "-" in num:
        num.remove("-")
    while num[0] == "0":
        del num[0]
    return len(num)

def round_a(num1, num2):

    #------Find the Correct Decimal Place to Round To------#
    dec1 = min(decimal(num1), decimal(num2))

    #------Get the Sum Without Rounding------#
    num = num1 + num2
    dec2 = decimal(num)
    num = list(str(num))

    #------Add 0s If the Answer Needs More Decimal Places------#
    while dec1 > dec2:
        num.append("0")
        dec2 += 1

    #------Round------#
    if dec1 < dec2:

        #------Check If the Number After the Correct Decimal Place is Greater Than 4------#
        if int(num[dec1 + num.index(".") + 1]) > 4:
            #----Move the Decimal to the Left if the Answer Shouldn't Have Any Decimal So That
            #----the Number Before the Decimal Rounds Properly----#
            if dec1 == 0:
                dec1 = -1

            #----Round the Number by Increasing It by 1----#
            num[dec1 + num.index(".")] = str(int(num[dec1 + num.index(".")]) + 1)

        #----Carry the 10 to the Next Digit----#
        while "10" in num:

            #------Reverse the List So That it Checks From the Right-Most 10------#
            num.reverse()
            x = num.index("10")

            #------Leave the 0------#
            num[x] = "0"
            if x + 1 < len(num):

                #----Carry the 1 to the Next Digit----#
                if num[x + 1] == ".":
                    x += 1
                num[x + 1] = str(int(num[x + 1]) + 1)
            else:

                #----Add 1 Infront of the Number if There Are No Digit to Carry To----#
                num.append("1")

            #------Reverse the List Back------#
            num.reverse()

        #------After Rounding------#
        #----Cut Off the Extra Digits----#
        while dec1 < dec2:
            if dec1 == 0:
                dec1 -= 1

            #--Remove the Last Digit--#
            num.reverse()
            del num[0]
            dec2 -= 1
            num.reverse()

    return "".join(num)

def round_s(num1, num2):

    #------Make the Smaller Number Negative So That the Answer will Always be Positive------#
    if num1 >= num2:
        num2 = -1 * num2
        return round_a(num1, num2)
    else:
        num1 = -1 * num1

        #----Add the Negative Sign Afterward----#
        return "-" + round_a(num1, num2)

def round_md(num1, num2):

    #------Get the Significant Digit------#
    digs = min(digits(num1), digits(num2))

    #------Calculation------#
    num = num1 * num2
    num = list(str(num))

    #------s = 1 If the Answer if Negative------#
    s = 0
    t = 1
    if "-" in num:
        s = 1
        num.remove("-")

    #------Remember the Decimal Index------#
    if "." in num:
        i = num.index(".")
        num.remove(".")
    else:
        i = len(num)

    #------Remove the Frontal 0s So the Answer Can Be Written In Scientific Notation------#
    while num[0] == "0":
        del num[0]

        #----Count the 0s Removed----#
        t += 1

    #------Update the Decimal Index------#
    i = i - t

    #------Rounding------#
    if digs < len(num):
        if int(num[digs]) > 4:
            num[digs - 1] = str(int(num[digs - 1]) + 1)

            #----Carry the 10s----#
            while "10" in num:
                num.reverse()
                x = num.index("10")
                num[x] = "0"

                #--Check If the Next Digit is the Decimal--#
                if x + 1 < len(num):
                    if num[x + 1] == ".":
                        x += 1
                    num[x + 1] = str(int(num[x + 1]) + 1)
                else:
                    num.append("1")
                num.reverse()

        #------Cut Off the Extra Digits------#
        num = num[:digs]

    #------Add 0s if the Answer Needs More Digits------#
    else:
        while len(num) < digs:
            num.append("0")

    #------Add the Decimal, Negative Sign, and Scientific Notation------#
    if digs != 1:
        num.insert(1, ".")
    if s == 1:
        num.insert(0, "-")
    if i == 0:
        return "".join(num)
    elif i == 1:
        return str("".join(num)) + " X 10"
    else:
        return str("".join(num)) + " X 10^" + str(i)

#---------------------User's Inputs---------------------#

print("Note: When entering 2 numbers, seperate them with a space.")

while True:
    userInput = input("Do you want to do (a)dding, (s)ubtracting, (m)ultiplying, or (d)ividing?")
    if userInput == "a":
        operation = "added"
    elif userInput == "s":
        operation = "subtracted"
    elif userInput == "m":
        operation = "multiplied"
    elif userInput == "d":
        operation = "divided"
    else:
        print("The input is invalid, please re-enter")
        continue

    num1, num2 = [str(n) for n in input("Please enter the two numbers that you want to be " + operation + ": ").split()]

    if "." in num1:
        num1 = float(num1)
    else:
        num1 = int(num1)
    if "." in num2:
        num2 = float(num2)
    else:
        num2 = int(num2)

    if userInput == "a":
        print(round_a(num1, num2))
    elif userInput == "s":
        print(round_s(num1, num2))
    elif userInput == "m":
        print(round_md(num1, num2))
    else:
        print(round_md(num1, 1/num2))

    userInput = input("Do you want to do another calculation? press y to continue, enter to escape")
    if userInput == "y":
        continue
    else:
        break
