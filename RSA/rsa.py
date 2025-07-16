# Helper functions
## keyToeN(string) -> tuple
## Takes in the path to a file containing a
## public RSA key, and returns a tuple with e
## and N values.
## Intended for use with rsaEncrypt(), to be
## piped into the key parameter in tuple form,
## or users can use the string form and just
## pass the file path to the function. 
def pubKeyToeN(file: str | None = None, key: str | int | None = None):
    if (file == None) and (key == None):
        raise ValueError("Either file or key must be provided")
    #TODO: Figure out how the hell to go from long ahh key to a and N

def privKeyTodN(file: str | None = None, key: str | int | None = None):
    ... #TODO: idfk

def rsaEncrypt(plaintext, key: tuple | str | int):
    if type(key) == tuple:
        ciphertext = (plaintext ** key[0]) % key[1]
    if type(key) == str:
        ciphertext = (plaintext ** pubKeyToeN(key)[0]) % pubKeyToeN(key)[1]
    if type(key) == int:
        ciphertext = (plaintext ** pubKeyToeN(key)[0]) % pubKeyToeN(key)[1]
    if (type(key) != str) and (type(key) != int) and (type(key) != tuple):
        raise TypeError("Invalid key type")
    return ciphertext

def rsaDecrypt(ciphertext, key: tuple | str | int):
    if type(key) == tuple:
        ...
    if type(key) == str:
        ...
    if type(key) == int:
        ...
    if (type(key) != str) and (type(key) != int) and (type(key) != tuple):
        raise TypeError("Invalid key type")
    return ciphertext

def rsaBruteForce():
    ...