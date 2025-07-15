def binDec(num: str):
    sum = 0
    power = 0
    for digit in reversed(num):
        if digit == '1':
            sum += int(digit) * (2 ** power)
            power += 1
        elif digit == '0':
            sum += 0
            power += 1
    return sum

def hexDec(num: str):
    hexDecDict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    if type(num) != str:
        num = str(num)
    sum = 0
    for digit in num:
        sum += hexDecDict[digit] * (16 ** (len(num) - num.index(digit) - 1))
    return sum

print(hexDec("4D361") == 316257)
print(binDec("1101010101") == 853)