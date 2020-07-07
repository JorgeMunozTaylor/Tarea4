#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tarea 4: Procesos aleatorios.
"""

""" 
Autor: Jorge Muñoz Taylor
Carné: A53863
Curso: Modelos probabilísticos de señales y sistemas
Grupo: 01
Fecha: 07/07/2020
"""

import sys
import numpy as np
from scipy import signal # Permite dibujar el espectro de frecuencias.
from math import sqrt # Permite hacer raíces cuadradas.

import matplotlib.pyplot as plt # Contiene las funciones necesarias para las gráficas.


# Función que recibe la potencia de la señal y regresa la potencia del ruido.
#
# [in] p_senal: Valor del SNR en decibeles.
# [in] snr: Valor del SNR NO en dB
# [out] Regresa el valor de la potencia del ruido. 
def p_ruido ( p_senal, snr ):
    return (p_senal/snr)

# Función que recibe el SNR_dB devuelve el SNR.
#
# [in] snr_db: SNR en decibeles.
# [out] Regresa el SNR.
def SNR_ ( snr_db ):
    return ( 10**(snr_db/10) )


# Función princiapl del programa.
if __name__=="__main__":

    archivo = sys.argv #Abre el archivo en base a la dirección dada como primer argumento. 

    #Se lee el archivo xp.csv y se coloca en un array tipo numpy. 
    DATOS = np.genfromtxt (archivo[1], dtype=int)



    ###############################################################################
    #1. Crear un esquema de modulación BPSK (Binary phase shift keying) para los bits presentados. Esto implica asignar una 
    #forma de onda senoidal normalizada (amplitud unitaria) para cada bit y luego una 
    #concatenación de todas estas formas de onda.
    ###############################################################################


    print ("\n\n***** Pregunta #1 *****\n")

    # EN BSPK el parámetro que varía en la portadora es la fase.

    N = len(DATOS) # Número de bits.
    f = 5000 # Hz
    T = 1/f # Período.
    p = 50 # Número de puntos de muestreo por período.

    # Puntos de muestreo para cada período de la señal portadora.
    tp = np.linspace (0, T, p)   
    
    # Frecuencia de muestreo.
    fs = p/T

    # Puntos de muestreo para la señal modulada.
    t = np.linspace(0, N*T, N*p)

    # Señal portadora.
    senoidal = np.sin (2 * np.pi * f * tp)

    # Señal modulada.
    senal_BPSK = np.zeros (t.shape)

    # Se general la señal modulada BPSK. Al bit 0 le corresponde la fase 0, al bit 1 le 
    # corresponde la fase 180. 
    for k, bit in enumerate(DATOS):
    
        if bit == 1:
            senal_BPSK [k*p:(k+1)*p] = senoidal

        else:
            senal_BPSK [k*p:(k+1)*p] = -senoidal

    # Indica cuantos bit se van a graficar.
    pb = 10
    
    # Se genera el gráfico.
    print ("--> Generando gráfico de señal BPSK...")
    plt.figure ()
    plt.title  ("Señal BPSK")
    plt.plot   ( senal_BPSK[0:pb*p] )
    plt.xlabel ("Puntos de muestreo")
    plt.ylabel ("Amplitud")
    plt.savefig("imagenes/bpsk.png")
    plt.show   ()



    ###############################################################################
    #2. Calcular la potencia promedio de la señal modulada generada.
    ###############################################################################


    print ("\n\n***** Pregunta #2 *****\n")

    # La potencia promedio de una señal está dada por el promedio temporal del segundo momento
    # de la señal.
    segundo_momento_BPSK = np.mean ( (senal_BPSK)**2 )

    print ("--> Potencia promedio =", segundo_momento_BPSK, "Watts")



    ###############################################################################
    #3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación 
    #señal a ruido (SNR) desde -2 hasta 3 dB.
    ###############################################################################

    print ("\n\n***** Pregunta #3 *****\n")

    # Se declararán los valores de decibeles que se desean usar para la simulación
    dB = np.empty  ( 0, int ) 
    dB = np.append ( dB, -2 )
    dB = np.append ( dB, -1 )
    dB = np.append ( dB, 0 )
    dB = np.append ( dB, 1 )
    dB = np.append ( dB, 2 )
    dB = np.append ( dB, 3 )
     
    # Se crea un vector vacío donde se guardarán los valores de amplitud para el ruido.
    P_ruido = np.empty(0, float)  

    # Se crea un vector vacío donde se guardarán los valores de SNR.
    SNR = np.empty(0,float)

    # Se agregan al array ASNR los valores que se utilizarán como límites para la amplitud
    # de la señal ruidosa.
    #for i in dB:
    #    ASNR = np.append ( ASNR, amplitud_ruido (i) )

    # Se agregan al array SNR los valores de SNR (no dB) para los SNR dB -2,-1,0,1,2,3 dB 
    # respectivamente.
    for i in dB:
        SNR  = np.append ( SNR, SNR_ (i) ) 

    # Obtiene los valores de la potencia del ruido para los SNR.
    P_ruido = np.append ( P_ruido, p_ruido ( segundo_momento_BPSK, SNR ) )

    # Array que contendrá la señal BPSK más la señal ruidosa.
    Rx = np.zeros ( shape = ( len(SNR), len(senal_BPSK) ) )

    # Genera la señal ruidosa.
    for RUIDO in P_ruido:
        ruido = np.random.normal ( 0, RUIDO, senal_BPSK.shape ) 
         
    # Matriz que contiene los la señal BPSK con cada una de las señales ruidosas.     
    for i,_ in enumerate(SNR):
        Rx[i] = senal_BPSK + ruido 


    print ("--> Generando gráfico de la señal ruidosa...")

    # Se genera el gráfico.
    plt.figure  ()
    plt.plot    ( Rx[0][0:pb*p] )
    plt.title   ( "Señal AWGN" )
    plt.xlabel  ( "Puntos de muestreo" )
    plt.ylabel  ( "Amplitud" )
    plt.savefig ( "imagenes/ruido.png" )
    plt.title   ("Señal BPSK")
    plt.show    () 



    ###############################################################################
    #4. Graficar la densidad espectral de potencia de la señal con el método de 
    # Welch (SciPy), antes y después del canal ruidoso.
    ###############################################################################


    print ("\n\n***** Pregunta #4 *****\n")
    
    # Se genera la densidad espectral para la señal BPSK.
    f_BPSK, P_BPSK = signal.welch ( senal_BPSK, f, nperseg = 1024 )

    # Se genera el gráfico.
    print ("--> Generando gráfico de la densidad espectral antes del canal ruidoso...")
    plt.figure   ()
    plt.semilogy (f_BPSK, P_BPSK)
    plt.ylim     ( [1e-10, 0.1] )
    plt.title    ( "Densidad espectral antes del canal ruidoso" )
    plt.xlabel   ( "Frecuencia [Hz]" )
    plt.ylabel   ( "Densidad espectral [dB]" )
    plt.savefig  ("imagenes/espectral_antes.png")
    plt.show     ()

    # Se genera la densidad espectral para después del canal ruidoso.
    fx, Pxx_den = signal.welch ( Rx[0], f, nperseg = 1024 )

    # Se genera el gráfico.
    print ("--> Generando gráfico de la densidad espectral después del canal ruidoso...")
    plt.figure   ()
    plt.semilogy (fx, Pxx_den)
    plt.ylim     ( [1e-5, 0.1] )
    plt.title    ( "Densidad espectral después del canal ruidoso" )
    plt.xlabel   ( "Frecuencia [Hz]" )
    plt.ylabel   ( "Densidad espectral [dB]" )
    plt.savefig  ("imagenes/espectral_despues.png")
    plt.show     ()



    ###############################################################################
    #5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits   
    #(BER, bit error rate) para cada nivel SNR.
    ###############################################################################


    print ("\n\n***** Pregunta #5 *****\n")

    # Nueva señal senoidal que se utilizará para demodular la señal modulada.
    senoidal2 = np.sin (2*np.pi*f*t)

    # Matriz de ceros donde se guardarán los valores decodificados para cada SNR.
    decodificada = np.zeros ( shape = ( len(SNR), len(DATOS) ) )
 
    # Se multiplicará la señal modulada por una señal con la misma frecuencia de la portadora.
    sen = []
    for i,_ in enumerate(SNR):
        sen.append ( Rx[i]*senoidal2 )

    # El proceso de decodificación consiste en tomar un rango de la señal recibida
    # y sumar dichos valores, luego se determina si el resultado es mayor o menor
    # a 0, si es mayor a 0 el código corresponde a un 1, si es negativo el 
    # código es un 0.
    for i,_ in enumerate(SNR):
        for k, bits in enumerate (DATOS):

            sumatoria = np.sum ( sen [i][k*p:(k+1)*p] )
            
            if sumatoria >= 0:
                decodificada [i][k] = 1 

            else:
                decodificada [i][k] = 0

    # Array vacío que contendra los valores de BER asociados a cada señal ruidosa.
    BER = []

    # Se recorre cada señal decodificada y se recorre cada uno de sus bits para 
    # compararlos con los bits originales, si no es así se toma como un error y
    # guarda el bit rate error en el array BER.
    for i,_ in enumerate(SNR): 

        error = 0
        for j, bits in enumerate (decodificada[i]):
            
            if bits != DATOS [j]:
                error += 1

        BER.append (error/len(DATOS))

    # Muestra en pantalla los valores de BER para cada SNR.
    for i,ber in enumerate(BER):
        print ( "-> BER para SNR", dB[i] ,"dB:", ber )
    


    ###############################################################################
    #6. Graficar BER versus SNR.
    ###############################################################################

    print ("\n\n***** Pregunta #6 *****\n")

    print ("--> Generando gráfica BER vs SNR...\n")
    plt.figure()

    
    # Se genera el gráfico BER vs SNR.
    plt.plot    ( SNR, BER ) 
    plt.xticks  ( SNR, dB )
    plt.title   ( "BER vs SNR" )
    plt.xlabel  ( "SNR [dB]" )
    plt.ylabel  ( "BER [%]" )
    plt.grid    ()
    plt.savefig ("imagenes/ber_vs_snr.png")
    plt.show    ()


    # Acaba el programa.
    print ("\n\n***** Fin del programa *****\n\n")