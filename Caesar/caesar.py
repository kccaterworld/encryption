import os
import string
import time
timeStart = time.time()

def compileWords(lenText = 0):
    timeStart = time.time()
    # Finds all the files with word lists in the WordLists directory
    os.chdir(os.path.dirname(__file__))
    # Creates a set of all the words in the files in wordListFiles, all lowercase
    if lenText == 0:
        allWordFiles = {word.lower() for word in open("WordLists/allWords.txt", 'r').read().split()}
    if lenText > 0:
        allWordFiles = {word.lower() for word in open("WordLists/allWords.txt", 'r').read().split() if len(word) <= lenText}
    print("WORD LIST COMPILE TIME: " + str(time.time() - timeStart))
    return set(allWordFiles)
chars = "!?.,'_-;:\"()[]{}<>@#$%^&*~`+=/\\|\n\r\t"

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
                 encrypt:bool = True) -> str | tuple:
    shifted = ""
    if encrypt:
        for glyph in text:
            if not glyph.isalpha():
                shifted += glyph
                continue
            if glyph.isspace():
                shifted += " "
                continue
            if glyph.islower():
                shifted += string.ascii_lowercase[(string.ascii_lowercase.index(glyph) + shift) % 26]
                continue
            if glyph.isupper():
                shifted += string.ascii_uppercase[(string.ascii_uppercase.index(glyph) + shift) % 26]
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
def bruteDecryptCaesar(shifted:str, **kwargs) -> tuple:
    debug = kwargs.get('debug', False)
    printOut = kwargs.get('print', False)
    timeStart = time.time()
    allSols = tuple((caesarCipher(shiftVal, shifted, False), shiftVal) for shiftVal in range(1, 27))
    if not debug:
        output:tuple[str,int] = tuple(sol[0] for sol in allSols)
    if debug:
        output:tuple[tuple[str,int]] = allSols
    if printOut:
        print(*output, sep='\n')
        if debug: print(time.time() - timeStart)
        return tuple(sol[0] for sol in allSols)
    if not printOut:
        if debug: print(time.time() - timeStart)
        return tuple(sol[0] for sol in allSols)

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
def testCaesarDecrypt(allSols:tuple, **kwargs) -> tuple[str, float]:
    debug = kwargs.get('debug', False)
    printOut = kwargs.get('print', False)
    timeStart = time.time()
    output = []
    
    for attempt in allSols:
        attemptStrip = attempt.translate(str.maketrans('', '', chars))
        attPerms = [attemptStrip[i:j+1].lower() for i in range(len(attemptStrip)) for j in range(i+1, len(attemptStrip))]
        attPermsVals = sum(1 for item in attPerms if item in words) / len(attPerms)
        attemptList = attemptStrip.split()
        totalWords = len(attemptList)
        validWords = sum(1 for word in attemptList if word.lower() in words)
        if not debug: output.append((attempt, attPermsVals, round(validWords / totalWords, 2)))
        if debug: output.append(((attempt, attPermsVals, round(validWords / totalWords, 2)), attPerms, [item for item in attPerms if item in words]))

    if printOut:
        print(*output, sep='\n')
        if debug: print(time.time() - timeStart)
        if debug: return tuple(res[0] for res in output)
        if not debug: return output
    if not printOut:
        if debug: print(time.time() - timeStart)
        if debug: return tuple(res[0] for res in output)
        if not debug: return output
    return "How did we get here"


# grabLeastWrongCaesar(tuple) -> str
# Takes in a tuple of decryptions and their validities,
## and finds the decryption(s) with the highest validity.
# Outputs a string with the most likely decryption,
# or a message indicating that there were multiple and listing them.
# The third and final function used in decryptCaesar,
## which is the main function that compiles the results
## to decrypt a Caesar cipher with an unknown shift value.
def grabLeastWrongCaesar(results:tuple, **kwargs) -> tuple:
    debug = kwargs.get('debug', False)
    printOut = kwargs.get('print', False)
    timeStart = time.time()
    returnStat = []
    validities = [attempt[1] for attempt in results]
    highestValidities = [attempt for attempt in results if attempt[1] == max(validities)]
    for value in highestValidities:
        returnStat.append(results[validities.index(value[1])][0])
    leastWrong = results[validities.index(max(validities))]

    if len(highestValidities) == 1:
        output = ("The most likely answer had a shift of " + str(results.index(leastWrong) + 1) + ": " + leastWrong[0],f"New Validity Score: {leastWrong[1]}\t\tOld Validity Score: {leastWrong[2]}")
    elif len(highestValidities) > 1:
        multHighest = [f"There were {len(highestValidities)} answers with similar probabilities:"]
        for answer in highestValidities:
            multHighest.append(f"{answer[0]}\t\tNew Validity Score: {answer[1]}\t\tOld Validity Score: {answer[2]}")
        output = tuple(multHighest)
    if debug: print(time.time() - timeStart)
    if printOut:
        print(*output, sep='\n')
    return output

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
def decryptCaesar(shifted:str, **kwargs) -> str:
    debug = kwargs.get('debug', False)
    printOut = kwargs.get('print', False)
    timeStart = time.time()
    results = []
    resDeb = []
    # Creates a tuple of every possible decryption
    allSols = tuple([caesarCipher(shiftVal, shifted, False) for shiftVal in range(1, 27)])
    if debug: allSolsDeb = tuple([(caesarCipher(shiftVal, shifted, False), shiftVal) for shiftVal in range(1, 27)])
    if debug and printOut: print(*allSolsDeb, sep='\n')

    # Checks validity of every word against web2List.txt,
    # and appends validity value to the decryption itself
    for attempt in allSols:
        attemptStrip = attempt.translate(str.maketrans('', '', chars))
        attPerms = [attemptStrip[i:j+1].lower() for i in range(min(len(attemptStrip), 31)) for j in range(i+1, min(len(attemptStrip), 32))]
        attPermsVals = sum(1 for item in attPerms if item in words) / len(attPerms)
        attemptList = attemptStrip.split()
        totalWords = len(attemptList)
        validWords = sum(1 for word in attemptList if word.lower() in words)
        results.append((attempt, attPermsVals, round(validWords / totalWords, 2)))
        if debug: resDeb.append(((attempt, attPermsVals, round(validWords / totalWords, 2)), attPerms, [item for item in attPerms if item in words]))
    if debug and printOut: print(*resDeb, sep='\n')
    
    validities = [attempt[1] for attempt in results]
    highestValidities = [attempt for attempt in results if attempt[1] == max(validities)]
    leastWrong = results[validities.index(max(validities))]
    if len(highestValidities) == 1:
        output = ("The most likely answer had a shift of " + str(results.index(leastWrong) + 1) + ": " + leastWrong[0],f"New Validity Score: {leastWrong[1]}\t\tOld Validity Score: {leastWrong[2]}")
    elif len(highestValidities) > 1:
        multHighest = [f"There were {len(highestValidities)} answers with similar probabilities:"]
        for answer in highestValidities:
            multHighest.append(f"{answer[0]}\t\tNew Validity Score: {answer[1]}\t\tOld Validity Score: {answer[2]}")
        output = tuple(multHighest)
    if debug: print(time.time() - timeStart)
    if printOut:
        print(*output, sep='\n')
    return output


if __name__ == "__main__":
    ## Setting text easily, as well as the shift value.
    shift = 13
    text = """dichlorodiphenyltrichloroethane"""
    encryptedText = caesarCipher(shift, text, encrypt = True)

    # Finds all the files with word lists in the WordLists directory
    os.chdir(os.path.dirname(__file__))
    # Creates a set of all the words in the files in wordListFiles, all lowercase
    allWordFiles = {word.lower() for word in open("WordLists/allWords.txt", 'r').read().split() if len(word) <= len(encryptedText)}
    global words
    words = set(allWordFiles)

    ## Testing encryption and decryption function, provided the shift is known.
    ### Testing encryption
    print(f"Encrypting '{text}' with a shift of {shift}:")
    print("caesarCipher(shift, text, encrypt = True)")
    print(f"Test:   " + caesarCipher(shift, text, encrypt = True))
    print(f"Actual: {encryptedText}")

    ### Testing decryption
    print(f"\nDecrypting the previously encrypted text:")
    print("caesarCipher(shift, encryptedText, encrypt = False)")
    print(f"Test:   " + caesarCipher(shift, encryptedText, encrypt = False))
    print(f"Actual: {text}")

    ## Testing the solving function
    ### Testing bruteDecryptCaesar, the first of three
    ### composite functions that make up decryptCaesar
    print(f"\nAll possible decryptions of the previously encrypted text:")
    print("bruteDecryptCaesar(encryptedText)")
    brute = bruteDecryptCaesar(encryptedText)
    print(*brute, sep="\n")

    ### Testing testCaesarDecrypt, the second of three
    ### composite functions that make up decryptCaesar
    print(f"\nAll possible decryptions of the previously encrypted text and their validities:")
    print("testCaesarDecrypt(bruteDecryptCaesar(encryptedText))")
    test = testCaesarDecrypt(brute, print = True, debug = True)
    print(*test, sep="\n")

    ### Testing grabLeastWrongCaesar, the third of three
    ### composite functions that make up decryptCaesar
    print(f"\nMost likely decryption of the previously encrypted text and its shift value:")
    print("grabLeastWrongCaesar(testCaesarDecrypt(bruteDecryptCaesar(encryptedText)))")
    least = grabLeastWrongCaesar(test)
    print(*least, sep="\n")

    ### Testing decryptCaesar, the main function that compiles the results
    print(f"\nDecrypted text and its validity:")
    print("decryptCaesar(encryptedText)")
    deTime = time.time()
    decrypt = decryptCaesar(encryptedText)
    print(*decrypt, sep="\n")

    print(f"\nExecution Time: {time.time() - timeStart} seconds")
    print(f"Decryption Time: {time.time() - deTime} seconds")