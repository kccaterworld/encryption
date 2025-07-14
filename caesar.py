# Reads the first of two files containing a list of
# common English words, web2List.txt.
# Proceeds to split it into a list to be used to check
# validity of words in the decrypted text. 
with open("web2List.txt", "r") as web2file:
    web2List = web2file.read().split()

# Reads the second of two files containing a list of
# common English words, words_pos.csv.
# Proceeds to split it into a list to be used to check
# validity of words in the decrypted text.
with open("words_pos.csv", "r") as words_pos:
    words_pos = words_pos.read()
    wordsSplit = words_pos.split("\n")
    wordsPosList = [line.split(",")[1] for line in wordsSplit[1:-1]]

# myStrip(string, string) -> string
# Takes in a string and a string of characters,
## and replaces every instance of the characters in the string
## with a space, then strips the string of leading
## and trailing whitespace.
# Outputs the modified string.
# This is used to remove punctuation and other characters
# Used in my decryptCaesar function to remove punctuation
## for checking against the word bank.
def myStrip(text, chars):
    for char in text:
        if char in chars:
            text = text.replace(char, " ")
    return text.strip()

# caesarCipher(integer, string, bool) -> string
# Takes in a string to be encrypted or decrypted, a
## shift value, and a boolean value to determine
## whether to encrypt or decrypt the string.
# Outputs the encrypted or decrypted string.
# The function uses a list of the alphabet to shift a
## certain number of characters forward or backward,
## depending on the boolean value.
# Encrypt = true to shift forward and encrypt the string.
# Decrypt = false to shift backward and decrypt the string.
# Decrypt just recursively calls caesarCipher with a negative shift value.
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


# bruteDecryptCaesar(string) -> tuple
# Takes in a string encrypted with a Caesar cipher
## and generates every possible decryption.
# Outputs a tuple of every possible decryption.
# This function uses caesarCipher to decrypt the string
## with every possible shift value from 1 to 26.
# The first of three functions used in decryptCaesar,
## which is the main function that compiles the results
## to decrypt a Caesar cipher with an unknown shift value.
def bruteDecryptCaesar(shifted:str) -> tuple:
    allSols = []
    for shiftVal in range(1, 27):
        allSols.append(caesarCipher(shiftVal, shifted, False))
    allSols = tuple(allSols)
    return allSols

# testCaesarDecrypt(tuple) -> tuple
# Takes in a tuple of all possible decryptions of a Caesar
## cipher and uses an external list of English words
## to check the validity of each word in each decryption.
# Outputs a tuple of each decryption and its validity.
# This function uses myStrip to remove punctuation in
## order to match with the word bank, which does not
## have any apostrophes or other punctuation.
# The second of three functions used in decryptCaesar,
## which is the main function that compiles the results
## to decrypt a Caesar cipher with an unknown shift value.
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

# grabLeastWrongCaesar(tuple) -> str
# Takes in a tuple of decryptions and their validities,
## and finds the decryption(s) with the highest validity.
# Outputs a string with the most likely decryption,
# or a message indicating that there were multiple and listing them.
# The third and final function used in decryptCaesar,
## which is the main function that compiles the results
## to decrypt a Caesar cipher with an unknown shift value.
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

# decryptCaesar(string) -> string
# Takes in a string encrypted with a Caesar cipher,
## generates every possible decryption, and uses a
## dictionary of approximately 370,000 English words
## to see which decryption is most likely correct.
# Outputs the most likely decryption.
# Accounts for the possibility of multiple decryptions
## having the same validity, and returns all of them.
# The compilation of three smaller functions I originally made,
## which are: bruteDecryptCaesar, testCaesarDecrypt,
## and grabLeastWrongCaesar. decryptCaesar removes the need
## for three different functions and nested calls.
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
            if word.lower().strip() in web2List:
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
## Setting text easily, as well as the shift value.
text = "Hi, my name's not a cipher"
shift = 13
encryptedText = caesarCipher(shift, text, encrypt = True)

## Testing encryption and decryption function, provided the shift is known.
### Testing encryption
print(f"Encrypting '{text}' with a shift of {shift}:")
print(f"Test:   " + caesarCipher(shift, text, encrypt = True))
print(f"Actual: {encryptedText}")

### Testing decryption
print(f"\nDecrypting the previously encrypted text:")
print(f"Test:   " + caesarCipher(shift, encryptedText, encrypt = False))
print(f"Actual: {text}")

## Testing the solving function
### Testing bruteDecryptCaesar, the first of three
### composite functions that make up decryptCaesar
print(f"\nAll possible decryptions of the previously encrypted text:")
print(*bruteDecryptCaesar(encryptedText), sep="\n")
### Testing testCaesarDecrypt, the second of three
### composite functions that make up decryptCaesar
print(f"\nAll possible decryptions of the previously encrypted text and their validities:")
print(*testCaesarDecrypt(bruteDecryptCaesar(encryptedText)), sep="\n")
### Testing grabLeastWrongCaesar, the third of three
### composite functions that make up decryptCaesar
print(f"\nMost likely decryption of the previously encrypted text and its shift value:")
print(grabLeastWrongCaesar(testCaesarDecrypt(bruteDecryptCaesar(encryptedText))))
### Testing decryptCaesar, the main function that compiles the results
print(f"\nDecrypted text and its validity:")
print(decryptCaesar(encryptedText))