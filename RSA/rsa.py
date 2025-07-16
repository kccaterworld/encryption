# Helper functions
## idfk so far

def keyToAN(file: str = "NO FILE"):
    ...


def rsaEncrypt(plaintext, key: tuple | str | int):
    if type(key) == tuple:
        ciphertext = (plaintext ** key[0]) % key[1]
    if type(key) == str:
        ... #TODO: Figure out how the hell to go from long ahh key to a and N
    if type(key) == int:
        ... #Same issue as with str, just straight into int. STR might be in hex? unsure if thats a thing
    return ciphertext

def rsaDecrypt():
    ...

def rsaBruteForce():
    ...