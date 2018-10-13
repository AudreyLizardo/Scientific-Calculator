import re

def decimal(num):
    num = str(num)
    if "." in num:
        waste, num = num.split(".")
        return len(num)
    else:
        return 0

def digits(num):
    num = str(num)
    if "." in num:
        num = num.replace(".", "")
    if "-" in num:
        num = num.replace("-", "")

    #------If dumb User inputs 0-----#
    try:
        while num[0] == "0":
            num = num[1:]
    except IndexError:
        return 1 #----Return something other than 0 to make the process continue----#
    return len(num)

def add(num1, num2, ratio1, ratio2):

    #------Find the correct decimal place to round To------#
    decimal_allowed = min(decimal(num1), decimal(num2))

    #------Get the sum without rounding------#
    num1 = float(num1) * ratio1
    num2 = float(num2) * ratio2
    num = num1 + num2
    decimal_in_answer = decimal(num)

    #----If python changes num to scientific notation----#
    if "e-" in str(num):
        base, index = str(num).split("e-")
        num = list(base)
        if "." in num:
            num.remove(".")
        for i in range(int(index)):
            num.insert(0, "0")
        num.insert(1, ".")
    else:
        num = list(str(num))

    decimal_in_answer = decimal("".join(num))

    #------Add 0s if the answer needs more decimal places------#
    while decimal_allowed > decimal_in_answer:
        num.append("0")
        decimal_in_answer += 1

    #------Round------#
    if decimal_allowed < decimal_in_answer:

        #------Check if the number after the correct decimal place is greater than 4------#
        if int(num[decimal_allowed + num.index(".") + 1]) > 4:
            #----Move the Decimal to the Left if the Answer Shouldn't Have Any Decimal So That
            #----the Number Before the Decimal Rounds Properly----#
            if decimal_allowed == 0:
                decimal_allowed = -1

            #----Round the number by increasing it by 1----#
            num[decimal_allowed + num.index(".")] = str(int(num[decimal_allowed + num.index(".")]) + 1)

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
        while decimal_allowed < decimal_in_answer:
            if decimal_allowed == 0:
                decimal_allowed -= 1

            #--Remove the last digit--#
            num.reverse()
            del num[0]
            decimal_in_answer -= 1
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

    #----Units are already converted----#
    return add(str(num1), str(num2), 1, 1)

def multiply_divide(num1, num2, ratio1, ratio2, operation):

    #------Get the significant digit------#
    digit_allowed = min(digits(num1), digits(num2))

    #------Calculation------#
    num1 = float(num1) * ratio1
    num2 = float(num2) * ratio2
    if operation == "multiply":
        num = num1 * num2
    else:
        num = num1 / num2
    if num == 0:
        return "0"

    #----If python changes num to scientific notation----#
    if "e-" in str(num):
        base, index = str(num).split("e-")
        num = list(base)
        if "." in num:
            num.remove(".")
        for i in range(int(index)):
            num.insert(0, "0")
        num.insert(1, ".")
    else:
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
    if digit_allowed < len(num):
        try:
            if int(num[digit_allowed]) > 4:
                num[digit_allowed - 1] = str(int(num[digit_allowed - 1]) + 1)

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
        num = num[:digit_allowed]

    #------Add 0s if the answer needs more digits------#
    else:
        while len(num) < digit_allowed:
            num.append("0")

    #------Add the decimal, negative sign, and scientific notation------#
    if digit_allowed != 1:
        num.insert(1, ".")
    if negative == True:
        num.insert(0, "-")
    if exponent == 0:
        return "".join(num)
    elif exponent == 1:
        return str("".join(num)) + " X 10"
    if exponent > 1:
        if exponent <= 3:
            #--Unicode for 2 and 3 is 00b--#
            return str("".join(num)) + " X 10" + eval(r'"\u00b' + str(exponent) + '"')
        elif exponent <= 9:
            #--Unicode for 4 to 9 is 207--#
            return str("".join(num)) + " X 10" + eval(r'"\u207' + str(exponent) + '"')
        elif exponent == 10:
            #--Return 10--#
            return str("".join(num)) + " X 10\u00b9\u2070"
        elif exponent == 11:
            #--Return 11--#
            return str("".join(num)) + " X 10\u00b9\u00b9"
        else:
            return "Out of range!"
    else:
        exponent *= -1
        if exponent == 1:
            return str("".join(num)) + " X 10\u207B\u00b9"
        elif exponent <= 3:
            return str("".join(num)) + " X 10\u207B" + eval(r'"\u00b' + str(exponent) + '"')
        elif exponent <= 9:
            return str("".join(num)) + " X 10\u207B" + eval(r'"\u207' + str(exponent) + '"')
        elif exponent == 10:
            #--Return 10--#
            return str("".join(num)) + " X 10\u207B\u00b9\u2070"
        elif exponent == 11:
            #--Return 11--#
            return str("".join(num)) + " X 10\u207B\u00b9\u00b9"
        elif exponent <= 13:
            return str("".join(num)) + " X 10\u207B\u00b9" + eval(r'"\u00b' + str(exponent)[1] + '"')
        else:
            return "Out of range!"

        #------For superscript unicode, see https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts------#

def give_units_and_ratios(calculation):
    match = re.search(r"(-?\d*\.?\d*)(\w*)([\+\-\*\/])(-?\d*\.?\d*)(\w*)", calculation)
    if match:
        unit1 = match.group(2)
        unit2 = match.group(5)
        if unit1 != unit2:
            unit1, unit2, ratio1, ratio2 = unit_conversion(unit1, unit2)
        else:
            ratio1, ratio2 = (1, 1)

        if "*" in calculation:
            if unit1 == "" and unit2 == "": #----If there are no units----#
                return "", ratio1, ratio2
            if unit1 != "" and unit1 == unit2: #----If the units are the same----#
                return unit1 + "\u00b2", ratio1, ratio2
            else: #----If the units are different----#
                return unit1 + unit2, ratio1, ratio2
        elif "/" in calculation:
            if unit1 == unit2:
                return "", ratio1, ratio2 #----Because the units cancel each other out----#
            else:
                return unit1 + "/" + unit2, ratio1, ratio2
        elif "+" in calculation or "-" in calculation:
            if unit1 == unit2:
                return unit1, ratio1, ratio2
            else:
                pass
        return "They are in different units ¯\_(ツ)_/¯", ratio1, ratio2
    #----Return nothing and 1 as ratio if there are no units----#
    return "", 1, 1

def unit_conversion(unit1, unit2):

    prefixes = {
        r"(P)(\w)": 1e15, r"(T)(\w)": 1e12, r"(G)(\w)": 1e9, r"(M)(\w)": 1e6,
        r"(k)(\w)": 1e3, r"(h)(\w)": 1e2, r"(da)(\w)": 1e1, r"(d)(\w)": 1e-1,
        r"(c)(\w)": 1e-2, r"(m)(\w)": 1e-3, r"(µ)(\w)": 1e-6, r"(n)(\w)": 1e-9,
        r"(p)(\w)": 1e-12, r"(f)(\w)": 1e-15
    }

    exceptions = [r"cd", r"mol", r"nit"]
    exception1 = ""
    exception2 = ""

    update1 = False #----Changes this to True when unit1 is updated----#
    update2 = False #----Changes this to True when unit2 is updated----#
    checked1 = False #----Checks for the exception----#
    checked2 = False #----Checks for the exception----#

    #----Get Convert to standard unit and give ratio----#
    for prefix in prefixes:

        #----Check if exceptions are in the units----#
        for exception in exceptions:
            if exception in unit1 and checked1 == False:
                exception1 = exception
                checked1 == True
            if exception in unit2 and checked2 == False:
                exception2 = exception
                checked2 == True

        #----So that the prefix only changes once----#
        if len(unit1) > len(exception1) and update1 == False:
            match = re.match(prefix, unit1)
            if match: #----If there is a prefix----#
                prefix1 = match.group(1)
                #----Convert to Standard Unit----#
                unit1 = re.sub(prefix, r"\2", unit1)
                ratio1 = prefixes[prefix]
                update1 = True
            else: #----No prefix----#
                prefix1 = ""
                ratio1 = 1
        elif update1 == False:
            prefix1 = ""
            ratio1 = 1

        #----So that the prefix only changes once----#
        if len(unit2) > len(exception2) and update2 == False:
            match = re.match(prefix, unit2)
            if match: #----If there is prefix----#
                prefix2 = match.group(1)
                #----Convert to Standard Unit----#
                unit2 = re.sub(prefix, r"\2", unit2)
                ratio2 = prefixes[prefix]
                update2 = True
            else: #----No prefix----#
                prefix2 = ""
                ratio2 = 1
        elif update2 == False:
            prefix2 = ""
            ratio2 = 1

    #----Check if they are in the same units----#
    if unit1 == unit2:
        #----Convert to the smaller unit----#
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

#------Execution------#
print("Enter 'quit' to quit at anytime")
while True:
    calculation = str(input("Enter the calculation"))

    #----Remove the spaces to make the output look better----#
    calculation = calculation.replace(" ", "")

    try:
        if calculation == "quit":
            break

        num1, num2 = re.findall(r"-?\d+\.?\d*", calculation)
        #----Check for missing zero at the front----#
        match = re.search(r"\." + num1, calculation)
        if match:
            num1 = "0." + num1
        match = re.search(r"\." + num2, calculation)
        if match:
            num2 = "0." + num2

        #----Check for missing zero at the end----#
        if num1[-1] == ".":
            num1 = num1 + "0"
        if num2[-1] == ".":
            num2 = num2 + "0"

        #----Unit conversion----#
        try:
            unit, ratio1, ratio2 = give_units_and_ratios(calculation)
        except UnboundLocalError:
            print("Invalid operation, please re-enter")
            continue
    except ValueError:
        print("Please enter two numbers with one operation")
        continue

    if unit == "They are in different units ¯\_(ツ)_/¯":
        print(unit)
    else:
        if "*" in calculation:
            print(calculation + "=" + multiply_divide(num1, num2, ratio1, ratio2, "multiply") + unit)
        elif "/" in calculation:
            if float(num2) == 0.0:
                print(calculation + "=" + "undefined")
            else:
                print(calculation + "=" + multiply_divide(num1, num2, ratio1, ratio2, "divide") + unit)
        elif "+" in calculation:
            print(calculation + "=" + add(num1, num2, ratio1, ratio2) + unit)
        elif "-" in calculation:
            print(calculation + "=" + subtract(num1, num2, ratio1, ratio2) + unit)
        else:
            print("Invalid operation, please re-enter")
