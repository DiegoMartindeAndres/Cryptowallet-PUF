import sys
import os
# Se importa Pypuf y elementos necesarios
from pypuf.simulation import XORBistableRingPUF
from pypuf.io import random_inputs
from numpy.random import default_rng
# Se importa la función de cifrado simétrico AES
from Crypto.Cipher import AES
# Se importa la función hash SHA3_256
from Crypto.Hash import SHA3_256

# Encripta con la clave generada por la PUF simulada
def PUFCipher( walletName, walletKey, UserPassword):

    codification = 'cp1252'

    directoryName = "./BBDD_wallets/"

    KeyInBytes = PUFKeyGenerator()
        
    # ciframos walletKey con response de la PUF en formato byte 
    noncePUF, encryptedWalletKeyPUF, tagPUF = encrypt(KeyInBytes, walletKey.encode(codification))

    # HASH del UserPassword en Bytes
    hash_obj = SHA3_256.new(UserPassword.encode(codification))
    UserPasswordHash = hash_obj.hexdigest()
    UserPasswordHashBytes = bytes.fromhex(UserPasswordHash)

   
    # ciframos encryptedWalletKeyPUF con el hash de la contraseña en formato byte 
    noncePwd, encryptedWalletKeyPUFPwd, tagPwd = encrypt(UserPasswordHashBytes, encryptedWalletKeyPUF)

    # y guardamos llave cifrada 2 (encryptedWalletKeyPUFPwd) y los nonce y tags de ambos procesos de encriptación
    # No es necesario guardar challenge porque son reproducibles
    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    with open(directoryName + walletName + '.bin', 'wb') as f:
        f.write(noncePUF)
        f.write(tagPUF)
        f.write(noncePwd)
        f.write(tagPwd)
        f.write(encryptedWalletKeyPUFPwd)

# Desencripta con la clave generada por la PUF simulada
def PUFDecipher(walletName, UserPassword):
    codification = 'cp1252'

    directoryName = "./BBDD_wallets/"

    PUFKeyInBytes = PUFKeyGenerator()
    # recogemos llave cifrada y challenges del fichero
    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    with open(directoryName+ walletName + '.bin', 'rb') as f:          
        noncePUF = f.readline(16)
        f.seek(16)
        tagPUF = f.readline(16)
        f.seek(32)
        noncePwd = f.readline(16)
        f.seek(48)
        tagPwd = f.readline(16)
        f.seek(64)
        encryptedWalletKeyPUFPwd = f.readline()
    
    # HASH del UserPassword en Bytes
    hash_obj = SHA3_256.new(UserPassword.encode(codification))
    UserPasswordHash = hash_obj.hexdigest()
    UserPasswordHashBytes = bytes.fromhex(UserPasswordHash)
    
    # Desciframos la llave privada de la cartera
    try:    
        encryptedWalletKeyPUF = decrypt(UserPasswordHashBytes, encryptedWalletKeyPUFPwd, tagPwd, noncePwd)
    except ValueError:
        print("\n\tLa contrasena de la cartera no es correcta.\n")
        exit()

    try:
        decryptedWalletKey = decrypt(PUFKeyInBytes, encryptedWalletKeyPUF, tagPUF, noncePUF)
        return decryptedWalletKey.decode(codification)
    except ValueError:
        print("\n\tEste dispositivo no esta autorizado para descifrar.\n")

# Genera la clave de 256 bits mediante el simulador PUF
def PUFKeyGenerator():

    # Se evaluan 256 challenges en el simulador PUF,
    # devuelve array de 256 bits
    k, n = 8, 64
    weights = default_rng(1).normal(size=(k, n+1))
    puf = XORBistableRingPUF(n=64, k=8,  weights=weights)
    challenges = random_inputs(n=64, N=256, seed=1)
    response = puf.eval(challenges)

    #Transforma las respuestas a bytes para poder pasarlo por el AES
    bitsArray = list(map(transform_array, response))
    bitsString = "".join(bitsArray)
    responseBytes = int(bitsString, 2).to_bytes(len(bitsString) // 8, byteorder='big')
    return responseBytes


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag


def decrypt(key, data, tag, nonce):

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(data, tag)


#Change every bit of the array to be a string,
# and if it's -1 change it to 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"
