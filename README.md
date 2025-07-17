# Encryption

My repository for learning about encryption

Currently 2 different algorithms I'm working on:
Caesar: Caesar ciphers
- Encrypts and decrypts ciphers
- Can brute force to decrypt by comparing possible words to a database of English words
- Uses two databases: [english-words](github.com/dwyl/english-words) by dwyl and [370k English words corpus](kaggle.com/datasets/ruchi798/part-of-speech-tagging) by Ruchi Bhatia

RSA: RSA Encryption
- Can encrypt and decrypt given e, d, and N
- GOALS:
  - Be able to read private and public key files and convert them into e, d, and N
  - Be able to convert text data into numerical data
    - This will likely emulate how pycryptodome does it