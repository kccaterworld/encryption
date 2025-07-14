from english_words import get_english_words_set # type: ignore
web2 = get_english_words_set(['web2'])#, lower=True)

with open("web2List.txt", "r") as web2file:
    web2List = web2file.read().split()

with open("words_pos.csv", "r") as words_pos:
    words_pos = words_pos.read()
    wordsSplit = words_pos.split("\n")
    wordsPosList = [line.split(",")[1] for line in wordsSplit[1:-1]]

def myStrip(text, chars):
    for char in text:
        if char in chars:
            text = text.replace(char, " ")
    return text.strip()

def caesarCipher(shift: int = 0,
                 text:str = "",
                 encrypt:bool = True) -> str:
    shifted = ""
    if encrypt:
        for character in text:
            if not character.isalpha():
                shifted += character
                continue
            if character.isspace():
                shifted += " "
                continue
            if character.islower():
                shifted += list("abcdefghijklmnopqrstuvwxyz")[(list("abcdefghijklmnopqrstuvwxyz").index(character) + shift) % 26]
                continue
            if character.isupper():
                shifted += [letter.upper() for letter in list("abcdefghijklmnopqrstuvwxyz")][([letter.upper() for letter in list("abcdefghijklmnopqrstuvwxyz")].index(character) + shift) % 26]
                continue
        return shifted
    if not encrypt:
        return caesarCipher(-shift, text, True)

def bruteDecryptCaesar(shifted:str) -> tuple:
    allSols = []
    for shiftVal in range(1, 27):
        allSols.append(caesarCipher(shiftVal, shifted, False))
    allSols = tuple(allSols)
    return allSols

def testCaesarDecrypt(allSols:tuple) -> tuple[str, float]:
    results = []
    for attempt in allSols:
        attemptStrip = myStrip(attempt, "!?.,'")
        attemptList = attemptStrip.split()
        validWords = 0
        totalWords = len(attemptList)
        for word in attemptList:
            if word.lower().strip() in web2List:
                validWords += 1
        results.append((attempt, "Validity: " + str(round(validWords / totalWords, 2))))
    return results

def grabLeastWrongCaesar(results:tuple) -> str:
    returnStat = []
    validities = [attempt[1] for attempt in results if attempt[1] != "Validity: 0.0"]
    highestValidities = tuple(max(validities) for i in range(validities.count(max(validities))))
    for value in highestValidities:
        returnStat.append(results[validities.index(value)][0])
    leastWrong = results[validities.index(max(validities))]
    if len(highestValidities) == 1:
        return "The most likely answer had a shift of " + str(results.index(leastWrong) + 1) + ": " + leastWrong[0]
    elif len(highestValidities) == 0:
        return "Something went really wrong, maybe try again?"
    elif len(highestValidities) > 1:
        multMaybe = "".join(returnStat + "\n")
        return f"There were {len(highestValidities)} answers with similar probabilities:\n {multMaybe}"

def decryptCaesar(shifted:str) -> str:
    # Setting empty lists
    allSols = []
    results = []
    returnStat = []
    
    # Adds every possible decryption to allSols,
    # then changes it to a tuple to preserve data integrity
    for shiftVal in range(1, 27):
        allSols.append(caesarCipher(shiftVal, shifted, False))
    allSols = tuple(allSols)

    # Checks validity of every word against web2List.txt,
    # and appends validity value to the decryption itself 
    for attempt in allSols:
        attemptStrip = myStrip(attempt, "!?.,'")
        attemptList = attemptStrip.split()
        validWords = 0
        totalWords = len(attemptList)
        for word in attemptList:
            if word.lower().strip() in words_pos:
                validWords += 1
        results.append((attempt, "Validity: " + str(round(validWords / totalWords, 2))))
    
    # Finds the validities of each decryption and finds the highest value(s)
    validities = [attempt[1] for attempt in results if attempt[1] != "Validity: 0.0"]
    highestValidities = tuple(max(validities) for i in range(validities.count(max(validities))))

    # Creates a list of all decryptions with equal and highest validities,
    # in case multiple are all equal to the highest validity.
    ## If this happens, check your work
    for value in highestValidities:
        returnStat.append(results[validities.index(value)][0])
    leastWrong = results[validities.index(max(validities))]

    # Return messages for 1, 0, or more than one highest validity values
    if len(highestValidities) == 1:
        return "The most likely answer had a shift of " + str(results.index(leastWrong) + 1) + ": " + leastWrong[0]
    elif len(highestValidities) == 0:
        return "Something went really wrong, maybe try again?"
    elif len(highestValidities) > 1:
        multMaybe = "".join(returnStat + "\n")
        return f"There were {len(highestValidities)} answers with similar probabilities:\n {multMaybe}"

# Test Cases
## Setting text easily, as well as encrypted text for checking
text = "Hi, my name's not a cipher"
shift = 13
encryptedText = caesarCipher(shift, text, encrypt = True)

## Testing encryption and decryption function, provided
## the shift is known. In this case, the shift is 13.
### Testing encryption
print(f"Encrypting '{text}' with a shift of {shift}:")
print(f"Test:   " + caesarCipher(shift, text, encrypt = True))
print(f"Actual: {encryptedText}")

### Testing decryption
print(f"\nDecrypting the previously encrypted text:")
print(f"Test:   " + caesarCipher(shift, encryptedText, encrypt = False))
print(f"Actual: {text}")

## Testing the solving function
### Initially just printing out all possibilities, will be checked
### against an English dictionary for valid words.
### Testing standard use case, with only one 
print(f"\nAll possible decryptions of the previously encrypted text:")
print(*bruteDecryptCaesar(encryptedText), sep="\n")
print(f"\nAll possible decryptions of the previously encrypted text and their validities:")
print(*testCaesarDecrypt(bruteDecryptCaesar(encryptedText)), sep="\n")
print(f"\nMost likely decryption of the previously encrypted text and its shift value:")
print(grabLeastWrongCaesar(testCaesarDecrypt(bruteDecryptCaesar(encryptedText))))

print(f"\nDecrypted text and its validity:")
print(decryptCaesar(encryptedText))