# Cryptowallet-PUF
Criptocartera software. Autenticación y encriptación de las llaves privadas mediante la tecnología PUF simulada.

Cryptowallet software. Authentication and encryptation based in simulated PUF technology.

IMPORTANTE: Se recomienda no usar este software para guardar sus llaves privadas. Este esta hecho mediante la tecnología PUF simulada, no protegerá sus llaves de la misma manera que lo haría una PUF no simulada.

IMPORTANT: It is recommended not to use this software to store your private keys. It is made using simulated PUF technology, it will not protect your keys the same way as a non-simulated PUF would.

## Manual de instalación
En un terminal Linux realice los siguientes pasos.
Necesario tener instalado python3:
```
sudo apt-get update
sudo apt-get install python3
```
y pip3:
```
sudo apt install python3-pip
```
Instalar Pypuf:
```
$ pip3 install pypuf
```
Instalar PyCriptodome:
```
pip3 install pycryptodome
```
Descargar repositorio mediante git:
```
git clone https://github.com/DiegoMartindeAndres/Cryptowallet-PUF.git 
cd Cryptowallet-PUF/
```
También es posible descargar repositorio mediante wget:
```
wget https://github.com/DiegoMartindeAndres/Cryptowallet-PUF/archive/refs/heads/main.zip
unzip main.zip
cd Cryptowallet-PUF-main
  ```
En este punto la cartera ya está instalada. Puede pasar al manual de uso.

## Manual de Uso

El uso del sistema es simple. Tan solo es necesario usar los dos comandos siguientes dentro de la carpeta con la cartera:
```
python3 main.py set <llave_privada> <nombre_cartera> <contraseña>
python3 main.py get <nombre_cartera> <contraseña>
```
Donde <llave_privada> es la llave privada de la criptocartera que queramos almacenar encriptada, <nombre_cartera> es el nombre que se le quiera dar a la cartera, es totalmente arbitrario y únicamente sirve como identificador, y <contraseña> es la contraseña que elija el usuario para cifrar la <llave_privada>, puede usar una distinta para cada cartera que genere.

Existe un manual de uso dentro de la aplicación, se puede obtener ejecutando el módulo main sin argumentos o con cualquier argumento que no sea “get” o “set”:
 ```
python3 main.py
```
Captura que lo muestra:

![image](https://user-images.githubusercontent.com/73550982/169874251-f2d16190-46db-4756-b204-9a34c7370030.png)


Comando *Set*:
```
python3 main.py set <llave_privada> <nombre_cartera> <contraseña>
```
El comando “set” sirve para cifrar y almacenar la <llave_privada> en el archivo <nombre_cartera>.bin, dentro de la carpeta BBDD_wallets mediante el cifrado con PUF y con la <contraseña>. No sin antes haber emparejado al dispositivo o, en el caso de ya estar emparejado, autorizarlo.

Este comando se puede ejecutar tantas veces como se quiera. En el caso de guardar una llave con el nombre de una cartera ya existente, esta se sobrescribirá. Si, por el contrario, se usa un nombre de cartera diferente se creará un archivo distinto, con el nombre de la nueva cartera. 

Se puede ver en la siguiente figura:

![image](https://user-images.githubusercontent.com/73550982/169873931-581b8673-6c3c-4975-a012-0d3f2a79bb8f.png)



Comando *Get*:
```
python3 main.py get <nombre_cartera> <contraseña>
```
El comando “get” sirve para descifrar la llave que guardamos con “set”. Al ejecutarlo primero se autorizará al dispositivo y si todo va bien se devolverá la clave descifrada de la cartera que le hemos pasado como parámetro, es decir, <nombre_cartera>. Debemos pasarle también la <contraseña> que usamos para cifrarlo.

Se puede ver en la siguiente figura:

 ![image](https://user-images.githubusercontent.com/73550982/169873823-6eb62dc5-9c7d-465e-a176-5dac2ecaae98.png)

## Referencias

- Pypuf:

Nils Wisiol, Christoph Gräbnitz, Christopher Mühl, Benjamin Zengin, Tudor Soroceanu, Niklas Pirnay, Khalid T. Mursi, & Adomas Baliuka. pypuf: Cryptanalysis of Physically Unclonable Functions (Version 2, June 2021). Zenodo. https://doi.org/10.5281/zenodo.3901410

GitHub:https://github.com/nils-wisiol/pypuf

- PyCryptodome:

GitHub:https://github.com/Legrandin/pycryptodome


