# Tarea 4: Procesos aleatorios

## Autor
```
Jorge Muñoz Taylor
A53863
jorge.munoztaylor@ucr.ac.cr
```

## Modo de uso

El programa se creó y se diseñó para ser usado en *Ubuntu* bajo *python3* por lo que no se puede garantizar que funcione adecuadamente en otros sistemas operativos. 

Para ejecutar el programa primero debe ubicarse en la carpeta Tarea4.
```
>cd PATH/Tarea4
```
Una vez en dicha carpeta puede ejecutar el programa con el comando python3.

```
>python3 tarea4 bits10k.csv
```

## Dependencias
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

<br>
<div align="center">
<img src=imagenes/bpsk.png width=450\textwidth>
<p>Figura 1 - Note que cada 50 puntos de muestro son 200us o un período completo.</p>
</div>

<br>

## 2. Calcular la potencia promedio de la señal modulada generada.


La potencia promedio viene dada por la ecuación ![pxx](https://latex.codecogs.com/gif.latex?P_%7BXX%7D).


<center>

![PXX](https://latex.codecogs.com/gif.latex?P_%7BXX%7D%20%3D%20%5Clim_%7BT%5Crightarrow%20%5Cinfty%20%7D%20%5Cfrac%7B1%7D%7B2T%7D%5Cint_%7BT%7D%5E%7B-T%7D%20E%5BX%5E2%28t%29%5Ddt)      
</center>

En este caso la ecuación, como *X(t)* es un valor conocido, ![pxx](https://latex.codecogs.com/gif.latex?P_%7BXX%7D) es equivalente a la esperanza de la función al cuadrado.


<center>

![PXX2](https://latex.codecogs.com/gif.latex?P_%7BXX%7D%20%3D%20E%5BX%5E2%28t%29%5D)
</center>

Al introducir este resultado en Python y utilizar *X* como la función *BPSK* generada se tiene un valor de potencia promedio de alrededor de 0.4899999999999997 *Watts*.


<br>

## 3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

Se tiene para *SNR* en dB:

<center>

![](https://latex.codecogs.com/gif.latex?SNR_%7BdB%7D%20%3D%2010log%20%28SNR%29)
</center>

Despejando *SNR*:

<center>

![](https://latex.codecogs.com/gif.latex?SNR%20%3D%2010%5E%7B%5Cfrac%7BSNR_%7BdB%7D%7D%7B10%7D%20%7D)
</center>

Que es igual a :

<center>

![](https://latex.codecogs.com/gif.latex?SNR%20%3D%20%28%20%5Cfrac%7BA_%7Bsenal%7D%7D%7B%20A_%7Bruido%7D%20%7D%20%29%5E2)
</center>

Ahora despejamos el valor de la amplitud de la señal ruidosa:

<center>

![](https://latex.codecogs.com/gif.latex?A_%7Bruido%7D%20%3D%20%5Csqrt%7B%20%5Cfrac%7BA_%7Bsenal%7D%5E2%20%7D%7B%2010%5E%7B%5Cfrac%7BSNR_%7BdB%7D%7D%7B10%7D%7D%20%7D%20%7D)
</center>

Con este resultado es posible obtener los valores de amplitud máximos que puede tener la señal ruidosa que se sumará a la señal *BPSK*, en la siguiente tabla se muestran los valores de dichas amplitudes para los *SNR* en *dB* propuestos en el enunciado, dichos valores se utilizaron a la hora de simular el canal ruidoso en *Python* (ver archivo **tarea4.py**):

<br>
<center>

| dB |      -2     |      -1     | 0 |       1      |       2      |       3      |
|:--:|:-----------:|:-----------:|:-:|:------------:|:------------:|:------------:|
|  A | 1.258925412 | 1.122018454 | 1 | 0.8912509381 | 0.7943282347 | 0.7079457844 |

</center>
<br>




En la figura 2 se muestra la salida para un *SNR* de -2 dB, se despliega sólo una gráfica porque todas son muy similares entre si. 

<br>
<div align="center">
<img src=imagenes/ruido.png width=450\textwidth>
<p>Figura 2 - Señal ruidosa. Los valores pseudoaleatorios se generaron con una función de distribución Gaussiana. </p>
</div>

<br>

## 4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.


La densidad espectral muestra la distribución de la potencia para todas las frecuencias de onda de una señal, en las figuras 3 y 4 se muestra la distribución de potencia para la señal *BPSK* sin y con ruido.

<br>

<div align="center">
<img src=imagenes/espectral_antes.png width=450\textwidth>
<p>Figura 3 - Note el tren de ondas bien marcado y como la primera onda claramente tiene un rango de potencia mayor a las demás, esto ocurre debido a que se trata de la frecuencia fundamental de la señal. </p>
</div>
<br><br>
<div align="center">
<img src=imagenes/espectral_despues.png width=450\textwidth>
<p>Figura 4 - En este caso la potencia de la señal se estabiliza en 40^-4, que corresponde a la densidad de potencia del ruido que se le sumó a la señal BPSK.</p>
</div>

<br>

## 5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.


Para demodular y decodificar la señal modulada BPSK se siguen los pasos a continuación:

* Se multiplica la señal por una onda -generalmente senoidal- con una frecuencia igual a la de la portadora que dio origen a la señal modulada.

* Se toma cada período y se suman sus elementos.

* Determinamos si la sumatoria es mayor o menor a 0.

* Si la sumatoria es positiva, asignamos un 1 a ese período.

* Si la sumatoria es negativa, asignamos un 0 a ese período.

* Por último comparamos la cadena de símbolos con la original para determinar el grado de error (*BER*).


Para los valores de *SNR* dados y para múltiples ejecuciones del código, el error promedio obtenido es de 0% para todos los niveles *SNR* pedidos. Esto ocurre debido a que el modelo *BPSK* es muy robusto, por esa razón es empleado para la transmisión de datos en sistemas inalámbricos, sin embargo puede fallar para valores de ruido mucho mayores. 


<br>

## 6. Graficar BER versus SNR.
---

 La curva *BER vs SNR* muestra el grado de error que existe en base a los dB de ruido, en la figura 5 se muestra dicha gráfica. La linealidad horizontal indica que para los dB (eje X) el grado de error fué de 0 para la simulación (aunque en algunas ocaciones, puede ocurrir un error de *0.0001%* para *SNR=-2dB*, sin embargo para los demás *SNR* siempre el porcentaje de error es de *0%*), es decir, todos los bits que se transmitieron a traves de la señal portadora fueron recibidos correctamente por el receptor sin falta de información. Cabe resaltar que este resultado se dió por dos causas: 
 * EL modelo *BPSK* es muy robusto.
 * Los dB utilizados para la simulación no fueron muy bajos, por lo que la señal original no se distorsionó mucho.
 
<br>
<div align="center">
<img src=imagenes/ber_vs_snr.png width=450\textwidth>
<p>Figura 5</p>
</div>