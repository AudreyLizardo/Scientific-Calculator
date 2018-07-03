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
        while n < len(num):
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
    dec1 = min(decimal(num1), decimal(num2))
    num = num1 + num2
    dec2 = decimal(num)
    num = list(str(num))
    while dec1 > dec2:
        num.append("0")
        dec2 += 1
    if dec1 < dec2:
        if int(num[dec1 + num.index(".") + 1]) > 4:
            if dec1 == 0:
                dec1 = -1
            num[dec1 + num.index(".")] = str(int(num[dec1 + num.index(".")]) + 1)
        while "10" in num:
            num.reverse()
            x = num.index("10")
            num[x] = "0"
            if x + 1 < len(num):
                if num[x + 1] == ".":
                    x += 1
                num[x + 1] = str(int(num[x + 1]) + 1)
            else:
                num.append("1")
            num.reverse()
        while dec1 < dec2:
            if dec1 == 0:
                dec1 -= 1
            num.reverse()
            del num[0]
            dec2 -= 1
            num.reverse()
    return "".join(num)

def round_s(num1, num2):
    if num1 >= num2:
        num2 = -1 * num2
        return round_a(num1, num2)
    else:
        num1 = -1 * num1
        return "-" + round_a(num1, num2)

def round_md(num1, num2):
    digs = min(digits(num1), digits(num2))
    num = num1 * num2
    num = list(str(num))
    s = 0
    t = 1
    if "-" in num:
        s = 1
        num.remove("-")
    if "." in num:
        i = num.index(".")
        num.remove(".")
    else:
        i = len(num)
    while num[0] == "0":
        del num[0]
        t += 1
    n = i - t
    if digs < len(num):
        if int(num[digs]) > 4:
            num[digs - 1] = str(int(num[digs - 1]) + 1)
            while "10" in num:
                num.reverse()
                x = num.index("10")
                num[x] = "0"
                if x + 1 < len(num):
                    if num[x + 1] == ".":
                        x += 1
                    num[x + 1] = str(int(num[x + 1]) + 1)
                else:
                    num.append("1")
                num.reverse()
        num = num[:digs]
    else:
        while len(num) < digs:
            num.append("0")
    if digs != 1:
        num.insert(1, ".")
    if s == 1:
        num.insert(0, "-")
    if n == 0:
        return "".join(num)
    elif n == 1:
        return str("".join(num)) + " X 10"
    else:
        return str("".join(num)) + " X 10^" + str(n)

#################################################################################

while True:
    i = input("Do you want to do (a)dding, (s)ubtracting, (m)ultiplying, or (d)ividing?")
    if i == "a":
        num1, num2 = [str(n) for n in input("Please enter the two numbers that you want to be added: ").split()]
    elif i == "s":
        num1, num2 = [str(n) for n in input("Please enter the two numbers that you want to be subtracted: ").split()]
    elif i == "m":
        num1, num2 = [str(n) for n in input("Please enter the two numbers that you want to be multiplied: ").split()]
    elif i == "d":
        num1, num2 = [str(n) for n in input("Please enter the two numbers that you want to be divided: ").split()]
    else:
        print("The input is invalid, please re-enter")
        continue

    if "." in num1:
        num1 = float(num1)
    else:
        num1 = int(num1)
    if "." in num2:
        num2 = float(num2)
    else:
        num2 = int(num2)

    if i == "a":
        print(round_a(num1, num2))
    elif i == "s":
        print(round_s(num1, num2))
    elif i == "m":
        print(round_md(num1, num2))
    else:
        print(round_md(num1, 1/num2))

    i = input("Do you want to do another calculation? press y to continue, enter to escape")
    if i == "y":
        continue
    else:
        break

