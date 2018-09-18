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

def add(num1, num2, ratio1, ratio2):

    #------Find the Correct Decimal Place to Round To------#
    dec1 = min(decimal(num1), decimal(num2))

    #------Get the Sum Without Rounding------#
    num1 = float(num1) * ratio1
    num2 = float(num2) * ratio2
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

def subtract(num1, num2, ratio1, ratio2):

    #------Make the Smaller Number Negative So That the Answer will Always be Positive------#
    if "." in num1:
        num1 = float(num1) * ratio1
    else:
        num1 = int(num1) * ratio1
    if "." in num2:
        num2 = float(num2) * ratio2
    else:
        num2 = int(num2) * ratio2

    return add(str(num1), str(num2), 1, 1) #----Units are already converted----#

def mutiply_divide(num1, num2, ratio1, ratio2, operation):

    #------Get the Significant Digit------#
    digs = min(digits(num1), digits(num2))

    #------Calculation------#
    num1 = float(num1) * ratio1
    num2 = float(num2) * ratio2
    if operation == "multiply":
        num = num1 * num2
    else:
        num = num1/num2
    if num == 0:
        return "0"
    num = list(str(num))

    negative = False
    t = 1
    if "-" in num:
        negative = True
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
    if negative == True:
        num.insert(0, "-")
    if i == 0:
        return "".join(num)
    elif i == 1:
        return str("".join(num)) + " X 10"
    else:
        return str("".join(num)) + " X 10^" + str(i)

def give_units_and_ratios(equation):
    match = re.search(r"(-?\d+\.?\d*)(\w*)([\+\-\*\/])(-?\d+\.?\d*)(\w*)", equation)
    if match:
        unit1 = match.group(2)
        unit2 = match.group(5)
        if unit1 != unit2:
            unit1, unit2, ratio1, ratio2 = unit_conversion(unit1, unit2)
        else:
            ratio1, ratio2 = (1, 1)

        if "*" in equation:
            if unit1 == "" and unit2 == "": #----If there are no units----#
                return "", ratio1, ratio2
            if unit1 != "" and unit1 == unit2: #----If the units are the same----#
                return unit1 + "\u00b2", ratio1, ratio2
            else: #----If the units are different----#
                return unit1 + unit2, ratio1, ratio2
        elif "/" in equation:
            if unit1 == unit2:
                return "", ratio1, ratio2 #----Because the units cancel each other out----#
            else:
                return unit1 + "/" + unit2, ratio1, ratio2
        elif "+" in equation or "-" in equation:
            if unit1 == unit2:
                return unit1, ratio1, ratio2
            else:
                pass
        return "They are in different units ¯\_(ツ)_/¯", ratio1, ratio2
    return "", ratio1, ratio2 #----Return nothing and 1 as ratio if there are no units----#

def unit_conversion(unit1, unit2):

    prefixes = {
    r"(P)(.)": 1000000000000000, r"(T)(.)": 1000000000000, r"(G)(.)": 1000000000, r"(M)(.)": 1000000,
    r"(k)(.)": 1000, r"(h)(.)": 100, r"(da)(.)": 10, r"(d)(.)": 0.1, r"(c)(.)": 0.01, r"(m)(.)": 0.001,
    r"(µ)(.)": 0.000001, r"(n)(.)": 0.000000001, r"(p)(.)": 0.000000000001, r"(f)(.)": 0.000000000000001
    }

    update1 = False #----Changes this to True when unit1 is updated----#
    update2 = False #----Changes this to True when unit2 is updated----#

    for prefix in prefixes:

        #----So that the prefix only changes once----#
        if update1 == False:
            match = re.match(prefix, unit1)
            if match:
                unit1 = re.sub(prefix, r"\2", unit1) #----Convert to Standard Unit----#
                ratio1 = prefixes[prefix]
                update1 = True
            else:
                ratio1 = 1

        #----So that the prefix only changes once----#
        if update2 == False:
            match = re.match(prefix, unit2)
            if match:
                unit2 = re.sub(prefix, r"\2", unit2) #----Convert to Standard Unit----#
                ratio2 = prefixes[prefix]
                update2 = True
            else:
                ratio2 = 1

    return unit1, unit2, ratio1, ratio2

#---------------------UI---------------------#
print("Enter 'quit' to quit at anytime")
while True:
    equation = str(input("Enter the equation"))

    #----Remove the spaces to make the output look better----#
    equation = re.sub(" ", "", equation)

    try:
        if equation == "quit":
            break
        num1, num2 = re.findall(r"-?\d+\.?\d*", equation)
        try:
            unit, ratio1, ratio2 = give_units_and_ratios(equation)
        except UnboundLocalError:
            print("Invalid operation, please re-enter")
            continue
    except ValueError:
        print("Please enter two numbers with one operation")
        continue

    if unit == "They are in different units ¯\_(ツ)_/¯":
        print(unit)
    else:
        if "*" in equation:
            print(equation + "=" + mutiply_divide(num1, num2, ratio1, ratio2, "multiply") + unit)
        elif "/" in equation:
            if float(num2) == 0.0:
                print(equation + "=" + "undefined")
            else:
                print(equation + "=" + mutiply_divide(num1, num2, ratio1, ratio2, "divide") + unit)
        elif "+" in equation:
            print(equation + "=" + add(num1, num2, ratio1, ratio2) + unit)
        elif "-" in equation:
            print(equation + "=" + subtract(num1, num2, ratio1, ratio2) + unit)
        else:
            print("Invalid operation, please re-enter")

    continue
