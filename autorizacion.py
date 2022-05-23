# Se importa Pypuf y elementos necesarios
from pypuf.simulation import XORBistableRingPUF
from pypuf.io import random_inputs
from numpy.random import default_rng
# Se importa la función hash SHA3_256
from Crypto.Hash import SHA3_256
# Módulo random propio de python
import random

def main():

	# Número de respuestas totales
	N = 1000
	# Número de respuestas aleatorias
	N_random = 250

	randomChallenges = [ ]
 	
 	# Generación de 250 números pseudoaleatorios
	for i in range (N_random):
		randomChallenges.append(random.randint(0, N-1))
	

	# Creamos instancia PUF
	k, n = 8, 64
	weights = default_rng(1).normal(size=(k, n+1))
	puf = XORBistableRingPUF(n=64, k=8,  weights=weights)

	# Inicializamos autorized a 0 (autorizado )
	authorized = 0

	try:
		# Leemos los hashes y los guardamos en realHashes
		realHashes = ""
		with open('BBDD_CRPs.txt', 'r') as f:
			realHashes = f.readlines()
	except:
		# Recoge excepción FileNotFoundError
		# Si no existe el fichero significa que no esta emparejado, devolvemos un 2
		authorized = 2
		return authorized

	# creamos los N respuestas de 64bits a partir de N challenges de 64bits
	for i in randomChallenges:

		# n = challenge length, N = response length
		challenges = random_inputs(n=64, N=64, seed=i)
		response = puf.eval(challenges)

		# transforma array de 1s y -1s a string de 0s y 1s
		response = "".join(list(map(transform_array, response)))
		responseBytes = int(response, 2).to_bytes(len(response) // 8, byteorder='big')

    	# HASH
		hash_obj = SHA3_256.new(responseBytes)
		responseHash = hash_obj.hexdigest()

		# Comparamos cada hash, si alguno fuera distinto, no se autoriza al dispositivo
		# Se usa [:-1] para eliminar el salto de linea del fichero ("\n")
		if (responseHash != realHashes[i][:-1]):
			# authized a 1 (no autorizado)
			authorized = 1

	return authorized

	
# Cambia cada int del array para que sea string,
# y si el valor es -1 lo cambia a 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"

