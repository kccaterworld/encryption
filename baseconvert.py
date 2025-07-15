hexValue = "4D361"
hexDec = {"0": 0, 
          "1": 1,
          "2": 2,
          "3": 3,
          "4": 4,
          "5": 5,
          "6": 6,
          "7": 7,
          "8": 8,
          "9": 9,
          "A": 10,
          "B": 11,
          "C": 12,
          "D": 13,
          "E": 14,
          "F": 15}

def hexDec(num: str,
           direction: bool = True):
    if type(num) != str:
        num = str(num)
    if direction:
        sum = 0
        for digit in num:
        sum += hexDec[digit] * (16 ** (len(num) - num.index(digit) - 1))
        return sum
    if not direction:
        ...


print(hexDec(hexValue))
print(hexDec("34"))
print(hexDec("AC"))
print(hexDec("5E"))