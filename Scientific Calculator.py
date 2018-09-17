import re

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
    num = list(num)
    if "." in num:
        num.remove(".")
    if "-" in num:
        num.remove("-")

    #------If Dumb User Inputs 0-----#
    try:
        while num[0] == "0":
            del num[0]
    except IndexError:
        return 1 #----Return Something Other Than 0 to Make the Process Continue----#

    return len(num)

def add(num1, num2):

    #------Find the Correct Decimal Place to Round To------#
    dec1 = min(decimal(num1), decimal(num2))

    #------Get the Sum Without Rounding------#
    num1 = float(num1)
    num2 = float(num2)
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

def subtract(num1, num2):

    #------Make the Smaller Number Negative So That the Answer will Always be Positive------#
    num1 = float(num1)
    num2 = float(num2)
    if num1 >= num2:
        num2 = -1 * num2
        return add(num1, num2)
    else:
        num1 = -1 * num1

        #----Add the Negative Sign Afterward----#
        return "-" + add(num1, num2)

def mutiply_divide(num1, num2, operation):

    #------Get the Significant Digit------#
    digs = min(digits(num1), digits(num2))

    #------Calculation------#
    num1 = float(num1)
    num2 = float(num2)
    if operation == "multiply":
        num = num1 * num2
    else:
        #----Test Division by 0----#
        try:
            num = num1/num2
        except ZeroDivisionError:
            return("undefined")
    if num == 0:
        return "0"
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

def give_unit(equation):
    match = re.search(r"(-?\d+\.?\d*)(\w*)([\+\-\*\/])(-?\d+\.?\d*)(\w*)", equation)
    if match:
        unit1 = match.group(2)
        unit2 = match.group(5)
        if "*" in equation:
            if unit1 == unit2:
                return unit1 + "^2"
            else:
                pass
        elif "/" in equation:
            if unit1 == unit2:
                return ""
            else:
                return unit1 + "/" + unit2
        elif "+" in equation or "-" in equation:
            if unit1 == unit2:
                return unit1
            else:
                pass
        return "Can't perform calculation with different units yet, sorry"
    return ""

#---------------------UI---------------------#

print("Enter 'quit' to quit at anytime'")
while True:
    equation = str(input("Enter the equation"))

    #----Remove the spaces to make the output look better----#
    equation = re.sub(r" ", "", equation)
    
    try:
        if equation == "quit":
            break
        num1, num2 = re.findall(r"-?\d+\.?\d*", equation)
        unit = give_unit(equation)
    except ValueError:
        print("Please enter two numbers with one operation")
        continue

    if unit == "Can't perform calculation with different units yet, sorry":
        print(unit)
    else:
        if "*" in equation:
            print(equation + "=" + mutiply_divide(num1, num2, "multiply") + unit)
        elif "/" in equation:
            print(equation + "=" + mutiply_divide(num1, num2, "divide") + unit)
        elif "+" in equation:
            print(equation + "=" + add(num1, num2) + unit)
        elif "-" in equation:
            print(equation + "=" + subtract(num1, num2) + unit)
        else:
            print("Invalid operation, please re-enter")

    continue
