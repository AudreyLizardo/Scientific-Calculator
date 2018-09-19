import re

def decimal(num):
    num = list(str(num))
    if "." in num:
        count = 0
        zero_index = num.index(".") + 1

        #------Move the decimal to the right------#
        while zero_index < len(num):

            #----Count how many places the decimal moved----#
            count += 1
            zero_index += 1

        return count
    else:
        return 0

def digits(num):
    num = list(num)
    if "." in num:
        num.remove(".")
    if "-" in num:
        num.remove("-")

    #------If dumb User inputs 0-----#
    try:
        while num[0] == "0":
            del num[0]
    except IndexError:
        return 1 #----Return something other than 0 to make the process continue----#

    return len(num)

def add(num1, num2, ratio1, ratio2):

    #------Find the correct decimal place to round To------#
    dec1 = min(decimal(num1), decimal(num2))

    #------Get the sum without rounding------#
    num1 = float(num1) * ratio1
    num2 = float(num2) * ratio2
    num = num1 + num2
    dec2 = decimal(num)
    num = list(str(num))

    #------Add 0s if the answer needs more decimal places------#
    while dec1 > dec2:
        num.append("0")
        dec2 += 1

    #------Round------#
    if dec1 < dec2:

        #------Check if the number after the correct decimal place is greater than 4------#
        if int(num[dec1 + num.index(".") + 1]) > 4:
            #----Move the Decimal to the Left if the Answer Shouldn't Have Any Decimal So That
            #----the Number Before the Decimal Rounds Properly----#
            if dec1 == 0:
                dec1 = -1

            #----Round the number by increasing it by 1----#
            num[dec1 + num.index(".")] = str(int(num[dec1 + num.index(".")]) + 1)

        #----Carry the 10 to the next digit----#
        while "10" in num:

            #------Reverse the list so that it checks from the right-most 10------#
            num.reverse()
            x = num.index("10")

            #------Leave the 0------#
            num[x] = "0"
            if x + 1 < len(num):

                #----Carry the 1 to the next digit----#
                if num[x + 1] == ".":
                    x += 1
                num[x + 1] = str(int(num[x + 1]) + 1)
            else:

                #----Add 1 infront of the number if there are no digit to carry to----#
                num.append("1")

            #------Reverse the list back------#
            num.reverse()

        #------After rounding------#
        #----Cut off the extra digits----#
        while dec1 < dec2:
            if dec1 == 0:
                dec1 -= 1

            #--Remove the last digit--#
            num.reverse()
            del num[0]
            dec2 -= 1
            num.reverse()

    return "".join(num)

def subtract(num1, num2, ratio1, ratio2):

    #------Make the smaller number negative so that the answer will always be positive------#
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

    #------Get the significant digit------#
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
    removed_zero = 1
    if "-" in num:
        negative = True
        num.remove("-")

    #------Remember the decimal index------#
    if "." in num:
        exponent = num.index(".")
        num.remove(".")
    else:
        exponent = len(num)

    #------Remove the frontal 0s so the answer can be written in scientific notation------#
    while num[0] == "0":
        del num[0]

        #----Count the 0s removed----#
        removed_zero += 1

    #------Update the decimal index------#
    exponent -= removed_zero

    #------Rounding------#
    if digs < len(num):
        try:
            if int(num[digs]) > 4:
                num[digs - 1] = str(int(num[digs - 1]) + 1)

                #----Carry the 10s----#
                while "10" in num:
                    num.reverse()
                    x = num.index("10")
                    num[x] = "0"

                    #--Check if the next digit is the decimal--#
                    if x + 1 < len(num):
                        if num[x + 1] == ".":
                            x += 1
                        num[x + 1] = str(int(num[x + 1]) + 1)
                    else:
                        num.append("1")
                    num.reverse()
        except ValueError:
            return("Out of range!")

        #------Cut Off the Extra Digits------#
        num = num[:digs]

    #------Add 0s if the answer needs more digits------#
    else:
        while len(num) < digs:
            num.append("0")

    #------Add the decimal, negative sign, and scientific notation------#
    if digs != 1:
        num.insert(1, ".")
    if negative == True:
        num.insert(0, "-")
    if exponent == 0:
        return "".join(num)
    elif exponent == 1:
        return str("".join(num)) + " X 10"
    if exponent > 1:
        if exponent <= 3:
            return str("".join(num)) + " X 10" + eval(r'"\u00b' + str(exponent) + '"') #--Unicode for 2 and 3 is 00b--#
        elif exponent <= 9:
            return str("".join(num)) + " X 10" + eval(r'"\u207' + str(exponent) + '"') #--Unicode for 4 to 9 is 207--#
        elif exponent == 10:
            return str("".join(num)) + " X 10\u00b9\u2070" #--Return 10--#
        elif exponent == 11:
            return str("".join(num)) + " X 10\u00b9\u00b9" #--Return 11--#
        elif exponent <= 13:
            return str("".join(num)) + " X 10\u00b9" + eval(r'"\u00b' + str(exponent)[1] + '"') #--Return 12 to 13--#
        else:
            return "Out of range!"
    else:
        exponent *= -1
        if exponent == 1:
            return str("".join(num)) + "X 10\u207B\u00b9"
        elif exponent <= 3:
            return str("".join(num)) + " X 10\u207B" + eval(r'"\u00b' + str(exponent) + '"')
        else:
            return "Out of range!"

        #------For superscript unicode, see https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts------#

def give_units_and_ratios(expression):
    match = re.search(r"(-?\d+\.?\d*)(\w*)([\+\-\*\/])(-?\d+\.?\d*)(\w*)", expression)
    if match:
        unit1 = match.group(2)
        unit2 = match.group(5)
        if unit1 != unit2:
            unit1, unit2, ratio1, ratio2 = unit_conversion(unit1, unit2)
        else:
            ratio1, ratio2 = (1, 1)

        if "*" in expression:
            if unit1 == "" and unit2 == "": #----If there are no units----#
                return "", ratio1, ratio2
            if unit1 != "" and unit1 == unit2: #----If the units are the same----#
                return unit1 + "\u00b2", ratio1, ratio2
            else: #----If the units are different----#
                return unit1 + unit2, ratio1, ratio2
        elif "/" in expression:
            if unit1 == unit2:
                return "", ratio1, ratio2 #----Because the units cancel each other out----#
            else:
                return unit1 + "/" + unit2, ratio1, ratio2
        elif "+" in expression or "-" in expression:
            if unit1 == unit2:
                return unit1, ratio1, ratio2
            else:
                pass
        return "They are in different units ¯\_(ツ)_/¯", ratio1, ratio2
    return "", ratio1, ratio2 #----Return nothing and 1 as ratio if there are no units----#

def unit_conversion(unit1, unit2):

    prefixes = {
    r"(P)(\w)": 1000000000000000, r"(T)(\w)": 1000000000000, r"(G)(\w)": 1000000000, r"(M)(\w)": 1000000,
    r"(k)(\w)": 1000, r"(h)(\w)": 100, r"(da)(\w)": 10, r"(d)(\w)": 0.1, r"(c)(\w)": 0.01, r"(m)(\w)": 0.001,
    r"(µ)(\w)": 0.000001, r"(n)(\w)": 0.000000001, r"(p)(\w)": 0.000000000001, r"(f)(\w)": 0.000000000000001
    }

    exceptions = [r"cd", r"mol", r"nit"]
    exception1 = ""
    exception2 = ""

    update1 = False #----Changes this to True when unit1 is updated----#
    update2 = False #----Changes this to True when unit2 is updated----#
    checked1 = False
    checked2 = False

    #----Get Convert to standard unit and give ratio----#
    for prefix in prefixes:

        #----Check if exceptions are in the units----#
        for exception in exceptions:
            exception_check = re.search(exception, unit1)
            if exception_check and checked1 == False:
                exception1 = exception
                checked1 == True
            exception_check = re.search(exception, unit2)
            if exception_check and checked2 == False:
                exception2 = exception
                checked2 == True

        if len(unit1) > len(exception1) and update1 == False: #----So that the prefix only changes once----#
            match = re.match(prefix, unit1)
            if match: #----If there is a prefix----#
                prefix1 = match.group(1)
                unit1 = re.sub(prefix, r"\2", unit1) #----Convert to Standard Unit----#
                ratio1 = prefixes[prefix]
                update1 = True
            else: #----No prefix----#
                prefix1 = ""
                ratio1 = 1
        elif update1 == False:
            prefix1 = ""
            ratio1 = 1

        if len(unit2) > len(exception2) and update2 == False: #----So that the prefix only changes once----#
            match = re.match(prefix, unit2)
            if match: #----If there is prefix----#
                prefix2 = match.group(1)
                unit2 = re.sub(prefix, r"\2", unit2) #----Convert to Standard Unit----#
                ratio2 = prefixes[prefix]
                update2 = True
            else: #----No prefix----#
                prefix2 = ""
                ratio2 = 1
        elif update2 == False:
            prefix2 = ""
            ratio2 = 1

    if unit1 == unit2: #----Check if they are in the same units----#
        #----Conver to the smaller unit----#
        if ratio1 > ratio2:
            unit1 = prefix2 + unit1
            unit2 = prefix2 + unit2
            ratio1 /= ratio2
            ratio2 = 1
        else:
            unit1 = prefix1 + unit1
            unit2 = prefix1 + unit2
            ratio2 /= ratio1
            ratio1 = 1

    return unit1, unit2, ratio1, ratio2

#---------------------UI---------------------#
print("Enter 'quit' to quit at anytime")
while True:
    expression = str(input("Enter the expression"))

    #----Remove the spaces to make the output look better----#
    expression = re.sub(" ", "", expression)

    try:
        if expression == "quit":
            break
        num1, num2 = re.findall(r"-?\d+\.?\d*", expression)
        try:
            unit, ratio1, ratio2 = give_units_and_ratios(expression)
        except UnboundLocalError:
            print("Invalid operation, please re-enter")
            continue
    except ValueError:
        print("Please enter two numbers with one operation")
        continue

    if unit == "They are in different units ¯\_(ツ)_/¯":
        print(unit)
    else:
        if "*" in expression:
            print(expression + "=" + mutiply_divide(num1, num2, ratio1, ratio2, "multiply") + unit)
        elif "/" in expression:
            if float(num2) == 0.0:
                print(expression + "=" + "undefined")
            else:
                print(expression + "=" + mutiply_divide(num1, num2, ratio1, ratio2, "divide") + unit)
        elif "+" in expression:
            print(expression + "=" + add(num1, num2, ratio1, ratio2) + unit)
        elif "-" in expression:
            print(expression + "=" + subtract(num1, num2, ratio1, ratio2) + unit)
        else:
            print("Invalid operation, please re-enter")
