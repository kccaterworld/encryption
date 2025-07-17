# Helper functions

def decodeBase64(s):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    char_to_val = {ch: i for i, ch in enumerate(base64_chars)}
    s = s.rstrip('=')
    bits = ""
    for char in s:
        if char not in char_to_val:
            raise ValueError(f"Invalid base64 character: {char}")
        val = char_to_val[char]
        bits += f"{val:06b}"
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            bytes_out.append(int(byte, 2))

    return bytes(bytes_out)

## keyToeN(string) -> tuple
## Takes in the path to a file containing a
## public RSA key, and returns a tuple with e
## and N values.
## Intended for use with rsaEncrypt(), to be
## piped into the key parameter in tuple form,
## or users can use the string form and just
## pass the file path to the function. 
def parsePublicKey(file: str | None = None,
                   key: str | int | None = None):
    if (file == None) and (key == None):
        raise ValueError("Either file or key must be provided")
    if (file != None) and (key != None):
        raise ValueError("Only one of file or key can be provided")
    if file != None:
        with open(file, "r") as keyfile:
            keyDER = keyfile.read().split("\n")[1]
    if key != None:
        keyDER = key.split("\n")[1]
    der = decodeBase64(keyDER)
    modulus_offset = der.find(b'\x02\x82\x01\x01') + 4
    exponent_offset = modulus_offset + 257
    assert der[exponent_offset] == 0x02
    e_len = der[exponent_offset + 1]
    modulus = der[modulus_offset:modulus_offset + 257]
    publicExponent = der[exponent_offset + 2:exponent_offset + 2 + e_len]

    return (int(publicExponent.hex(), 16), int(modulus.hex(), 16))

def parsePrivateKey(file: str | None = None,
                    key: str | int | None = None,
                    publicExp: bool = False):
    if (file == None) and (key == None):
        raise ValueError("Either file or key must be provided")
    if (file != None) and (key != None):
        raise ValueError("Only one of file or key can be provided")
    if file != None:
        with open(file, "r") as keyfile:
            keyDER = keyfile.read().split("\n")[1]
    if key != None:
        keyDER = key.split("\n")[1]
    der = decodeBase64(keyDER)

    def read_length(data, offset):
        first = data[offset]
        offset += 1
        if first & 0x80 == 0:
            return first, offset
        num_bytes = first & 0x7F
        length = int.from_bytes(data[offset:offset+num_bytes], "big")

        return length, offset + num_bytes

    def read_integer(data, offset):
        assert data[offset] == 0x02
        length, offset = read_length(data, offset + 1)
        value = int.from_bytes(data[offset:offset+length], "big")

        return value, offset + length

    def read_sequence(data, offset):
        assert data[offset] == 0x30
        length, offset = read_length(data, offset + 1)

        return offset, offset + length

    offset, _ = read_sequence(der, 0)
    _, offset = read_integer(der, offset)
    alg_start, alg_end = read_sequence(der, offset)
    offset = alg_end
    assert der[offset] == 0x04
    pk_len, offset = read_length(der, offset + 1)
    rsa_data = der[offset:offset + pk_len]
    offset, _ = read_sequence(rsa_data, 0)
    version, offset = read_integer(rsa_data, offset)
    modulus, offset = read_integer(rsa_data, offset)
    publicExponent, offset = read_integer(rsa_data, offset)
    privateExponent, _ = read_integer(rsa_data, offset)

    if publicExp:
        return (publicExponent, modulus)
    
    if not publicExp:
        return (privateExponent,modulus)

def encodetext(file: str | None = None,
               text: str | None = None,
               dest: str | None = None):
    if (file == None) and (text == None):
        raise ValueError("Either file or text must be provided")
    if (file != None) and (text != None):
        raise ValueError("Only one of file or text can be provided")
    if file != None:
        textfile = open(file, "r")
        text = textfile.read()
        encodetext(text=text)
    if text != None:
        if dest != None:
            with open(dest, "w") as file:
                file.write(text.encode("ascii").hex())
        return text.encode("ascii").hex()

def decodeText(file: str | None = None,
               text: str | None = None,
               dest: str | None = None):
    if (file == None) and (text == None):
        raise ValueError("Either file or text must be provided")
    if (file != None) and (text != None):
        raise ValueError("Only one of file or text can be provided")
    if file != None:
        textfile = open(file, "r")
        text = textfile.read()
        decodeText(text=text)
    if text != None:
        if dest != None:
            with open(dest, "w") as file:
                file.write(bytes.fromhex(text).decode("ascii"))
        return bytes.fromhex(text).decode("ascii")
    
def rsaEncrypt(plaintext, key: tuple):
    ciphertext = (plaintext ** key[0]) % key[1]
    return ciphertext

def rsaDecrypt(ciphertext, key: tuple):
    plaintext = (ciphertext ** key[0]) % key[1]
    return plaintext


# Testing with data.txt: Sherlock Holmes
# Step 1: Encode the text
print("Encoding text...")
encodedText = encodetext(file="RSA/teeny.txt", dest="RSA/teenyencodeddata.txt")
print("Text encoded successfully.")
# Step 2: Encrypt the encoded text
print("Encrypting text...")
encryptedText = rsaEncrypt(int(encodedText, 16), parsePublicKey("RSA/Practice Keys/practicepublic.pem"))
print("Text encrypted successfully.")
with open("RSA/teenyencrypteddata.txt", "w") as file:
    file.write(str(encryptedText))
print("Encrypted text written to teenyencrypteddata.txt.")

# Step 3: Decrypt the encrypted text and compare with encoded text
print("Decrypting text...")
readEncryptedText = int(open("RSA/teenyencrypteddata.txt", "r").read())
decryptedText = rsaDecrypt(readEncryptedText, parsePrivateKey("RSA/Practice Keys/practiceprivate.key"))
print("Text decrypted successfully.")
print("Comparing decrypted text with encoded text...")
print(decryptedText == encodedText)

# Step 4: Decode the decrypted text and compare with original text
print("Decoding text...")
decodedText = decodeText(text=decryptedText, dest="RSA/teenydecodeddata.txt")
print("Text decoded successfully.")
print("Comparing decoded text with original data...")
print(decodedText == open("RSA/teeny.txt", "r").read())