# Se importa Pypuf y elementos necesarios
from pypuf.simulation import XORBistableRingPUF
from pypuf.io import random_inputs
from numpy.random import default_rng
# Se importa la función hash SHA3_256
from Crypto.Hash import SHA3_256


def main():

	# Número de respuestas
	N = 1000
	
	# Creamos PUF
	k, n = 8, 64
	weights = default_rng(1).normal(size=(k, n+1))
	puf = XORBistableRingPUF(n=64, k=8,  weights=weights)

	# creamos las N respuestas de 128bits a partir de N sets de 64 challenges de 64bits 
	# (cada challenge da una respuesta de 1 bit, por lo que resultan respuestas de 64 bits)
	for i in range(0 ,N ):

		# n = challenge length, N = response length
		challenges = random_inputs(n=64, N=64, seed=i)
		response = puf.eval(challenges)

		# transforma array de 1s y -1s a string de 0s y 1s
		response = "".join(list(map(transform_array, response)))
		responseBytes = int(response, 2).to_bytes(len(response) // 8, byteorder='big')


    	# HASH
		hash_obj = SHA3_256.new(responseBytes)
		responseHash = hash_obj.hexdigest()

		# escribimos (en modo adición) cada hash
		with open('BBDD_CRPs.txt', 'a') as f:
			f.write(responseHash+"\n")
		

# Cambia cada int del array para que sea string,
# y si el valor es -1 lo cambia a 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"
