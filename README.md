# Tarea 4:

## Autor
```
Jorge Muñoz Taylor
A53863
jorge.munoztaylor@ucr.ac.cr
```

## Modo de uso
```
>python3 tarea4 bits10k.csv
```

## Bibliotecas
```
1. scipy
2. numpy
```

# Solución

## 1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.

Para crear un sistema de modulacón se necesitan dos señales: 
* Una señal portadora 
* Una señal moduladora

La señal portadora generalmente es una onda senoidal con una frecuencia conocida, esta señal es la que transportará la información por el tiempo y el espacio. En Python esta onda se simulará utilizando la funcióm *sin* de *numpy*, la función *pi* de *numpy*. Se utilizó una frecuencia de 5*KHz*.

La señal modulada mediante el esquema *BPSK* consiste en asigna a cada símbolo una fase de la señal portadora, en nuestro caso, al símbolo 0 se le asignó la fase negativa, al 1 la positiva. Cuando una cadena de símbolos es transmitida se analiza y se asigna la fase uno por uno y luego se suman, para generar una nueva señal, esta nueva onda será la que viajará hasta el receptor.

Para simular este esquema se utilizó el siguiente algoritmo:


    for k, bit in enumerate(DATOS):
    
        if bit == 1:
            senal_BPSK [k*p:(k+1)*p] = senoidal

        else:
            senal_BPSK [k*p:(k+1)*p] = -senoidal

Como se puede ver, al array *senal_BPSK* se le asignan los valores positivos o negativos en base al código que se está analizando, donde *bit* es el código y *k* es el número de código.

Finalmente la señal modulada con el esquema *BPSK* se muestra en la figura 1.


<div align="center">
<img src=imagenes/bpsk.png width=450\textwidth>
<p>Figura 1 - </p>
</div>

---
## 2. Calcular la potencia promedio de la señal modulada generada.


La potencia promedio viene dada por la ecuación ![pxx](https://latex.codecogs.com/gif.latex?P_%7BXX%7D).


* ![PXX](https://latex.codecogs.com/gif.latex?P_%7BXX%7D%20%3D%20%5Clim_%7BT%5Crightarrow%20%5Cinfty%20%7D%20%5Cfrac%7B1%7D%7B2T%7D%5Cint_%7BT%7D%5E%7B-T%7D%20E%5BX%5E2%28t%29%5Ddt)      

En este caso la ecuación, como *X(t)* es un valor conocido, ![pxx](https://latex.codecogs.com/gif.latex?P_%7BXX%7D) es equivalente a la esperanza de la función al cuadrado.


* ![PXX2](https://latex.codecogs.com/gif.latex?P_%7BXX%7D%20%3D%20E%5BX%5E2%28t%29%5D)


Al introducir este resultado en Python y utilizar *X* como la función *BPSK* generada se tiene un valor de potencia promedio de alrededor de 0.4899999999999997 *Watts*.

---
## 3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

Se tiene para *SNR* en dB:

![](https://latex.codecogs.com/gif.latex?SNR_%7BdB%7D%20%3D%2010log%20%28SNR%29)


Despejando *SNR*:

* ![](https://latex.codecogs.com/gif.latex?SNR%20%3D%2010%5E%7B%5Cfrac%7BSNR_%7BdB%7D%7D%7B10%7D%20%7D)


Que es igual a :

* ![](https://latex.codecogs.com/gif.latex?SNR%20%3D%20%28%20%5Cfrac%7BA_%7Bsenal%7D%7D%7B%20A_%7Bruido%7D%20%7D%20%29%5E2)


Ahora despejamos el valor de la amplitud de la señal ruidosa:

* ![](https://latex.codecogs.com/gif.latex?A_%7Bruido%7D%20%3D%20%5Csqrt%7B%20%5Cfrac%7BA_%7Bsenal%7D%5E2%20%7D%7B%2010%5E%7B%5Cfrac%7BSNR_%7BdB%7D%7D%7B10%7D%7D%20%7D%20%7D)


Con este resultado es posible obtener los valores de amplitud máximos que puede tener la señal ruidosa que se sumará a la señal *BPSK*, en la siguiente tabla se muestran los valores de dichas amplitudes para los *SNR* en *dB* propuestos en el enunciado:



| dB |      -2     |      -1     | 0 |       1      |       2      |       3      |
|:--:|:-----------:|:-----------:|:-:|:------------:|:------------:|:------------:|
|  A | 1.258925412 | 1.122018454 | 1 | 0.8912509381 | 0.7943282347 | 0.7079457844 |


Estos valores se utilizaron a la hora de simular el canal ruidoso en *Python* -ver archivo **tarea4.py**-.



<div align="center">
<img src=imagenes/ruido.png width=450\textwidth>
<p>Figura 2 - Señal ruidosa correspondiente a un SNR de -2 dB. Los valores pseudoaleatorios se generaron con una función de distribución Gaussiana. </p>
</div>


---
## 4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.


<div align="center">
<img src=imagenes/espectral_antes.png width=450\textwidth>
<p>Figura 3  </p>
</div>

<div align="center">
<img src=imagenes/espectral_despues.png width=450\textwidth>
<p>Figura 4 </p>
</div>

---
## 5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.


Para demodular y decodificar la señal modulada BPSK se siguen los pasos a continuación:

* Se multiplica la señal por una onda -generalmente senoidal- con una frecuencia igual a la de la portadora que dio origen a la señal modulada.

* Se toma cada período y se suman sus elementos.

* Determinamos si la sumatoria es mayor o menor a 0.

* Si la sumatoria es positiva, asignamos un 1 a ese período.

* Si la sumatoria es negativa, asignamos un 0 a ese período.



---
## 6. Graficar BER versus SNR.
---

<div align="center">
<img src=imagenes/ber_vs_snr.png width=450\textwidth>
<p>Figura 5 </p>
</div>