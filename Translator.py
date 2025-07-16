# Hex Translator
hexDec = {"0":0, 
          "1":1,
          "2":2,
          "3":3,
          "4":4,
          "5":5,
          "6":6,
          "7":7,
          "8":8,
          "9":9,
          "A":10,
          "B":11,
          "C":12,
          "D":13,
          "E":14,
          "F":15}
def hexTranslate():
    sum = 0
    hexVal = input("Hex value?")
    for digit in hexVal:
        sum += hexDec[digit]*(16**(len(hexVal)-hexVal.index(digit)-1))
    print(sum)

#Base64
base64 = {"A":0,
          "B":1,
          "C":2,
          "D":3,
          "E":4,
          "F":5,
          "G":6,
          "H":7,
          "I":8,
          "J":9,
          "K":10,
          "L":11,
          "M":12,
          "N":13,
          "O":14,
          "P":15,
          "Q":16,
          "R":17,
          "S":18,
          "T":19,
          "U":20,
          "V":21,
          "W":22,
          "X":23,
          "Y":24,
          "Z":25,
          "a":26,
          "b":27,
          "c":28,
          "d":29,
          "e":30,
          "f":31,
          "g":32,
          "h":33,
          "i":34,
          "j":35,
          "k":36,
          "l":37,
          "m":38,
          "n":39,
          "o":40,
          "p":41,
          "q":42,
          "r":43,
          "s":44,
          "t":45,
          "u":46,
          "v":47,
          "w":48,
          "x":49,
          "y":50,
          "z":51,
          "0":52,
          "1":53,
          "2":54,
          "3":55,
          "4":56,
          "5":57,
          "6":58,
          "7":59,
          "8":60,
          "9":61,
          "+":62,
          "/":63,
          "=":""}
def base64Translate():
    sum = 0
    base64Val = input("Base64 value?")
    for digit in base64Val:
        sum += base64[digit]*(64**(len(base64Val)-base64Val.index(digit)-1))
    print(sum)
# This is where things get decided

cipherType = input("What kind of cipher?")
if cipherType == "Hexadecimal":
    hexTranslate()
elif cipherType == "Base64":
    base64Translate()