# -*- coding: utf-8 -*-
"""
---------------------------------------------------
--------------------Modelo de Markov---------------
---------------------------------------------------

"""
#Paso 1 ¿Como se obtienen las probabilidades de transición?
#El nuemero de empresas que cambiaron a una calificacion al terminar elperiodo
#dividido entre todas las empresas que tenian la misma calificacion al empezar
#el periodo

#Paso 2 ¿Cuál es el periodo de tiempo de la Transición?
#El periodo de transicion es de 1 año

#Paso 3 ¿Cuál es con las hipotesis del modelo?
#


import numpy as np
T=np.matrix([[0.9043,0.0600,0.0234,0.0123,0.0000,0.0000,0.0000,0.0000],
             [0.0097,0.8563,0.0777,0.0465,0.0098,0.0000,0.0000,0.0000],
             [0.0008,0.0078,0.8893,0.0763,0.0213,0.0045,0.0000,0.0000],
             [0.0003,0.0021,0.0088,0.8379,0.0743,0.0412,0.0354,0.0000],
             [0.0000,0.0002,0.0021,0.0058,0.8172,0.0943,0.0568,0.0236],
             [0.0000,0.0000,0.0005,0.0179,0.0467,0.7689,0.0987,0.0673],
             [0.0000,0.0000,0.0000,0.0007,0.0234,0.0456,0.7609,0.1694],
             [0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,1.0000]])
             
#Paso 4 Represente graficamente la matriz de transició

#Paso 5 Clasifique los estados
             
             
#Descomposicion  en valores y vextores propios
def propios(A):
    ValProp=np.linalg.eig(A)
    ValPropios=np.diag(ValProp[0])
    VecPropios=ValProp[1]
    return(ValPropios,VecPropios)  
    
#Pasos en una Matriz
def markov(A,n):
    ValProp=np.linalg.eig(A)
    ValPropios=np.diag(ValProp[0])
    VecPropios=ValProp[1]
    
    lambda_n=ValPropios**n
    matriz_n=VecPropios*lambda_n*np.linalg.inv(VecPropios)
    
    return matriz_n
#Paso 6 Descomposicion de valores y vectores propios de la matriz de transición T
PropiosT=propios(T)
#Paso 7 Probabilidad de que de AAA pase a default en 2 pasos
T2=markov(T,2)
#Paso 8  Distribucion Terminal de T
Tn=markov(T,10000)
#Paso 9 Matriz T en forma canonica encontrando Q
Q=np.delete(T,7,0)
Q=np.delete(Q,7,1)
#Paso 10 Descomposicion de valores y vectores propios de la matriz Q
PropiosQ=propios(Q)
#Paso 8  Distribucion Terminal de Q
Qn=markov(Q,10000)

##Distrubiciones terminales mediante la simulacion montecarlo

n=10000
mat_alea=np.matrix(np.random.uniform (size=[n,np.shape(T,)[1]]))
otra_matriz=np.apply_over_axes(np.sum,mat_alea,1)

mat_valores_iniciales=mat_alea/otra_matriz

mat_final2=mat_valores_iniciales*(Tn**n)
matriz_montecarlo=np.apply_over_axes(np.mean,mat_final2,0)

P_matriz=matriz_montecarlo*Tn

############
N=np.linalg.inv(np.diag([1,1,1,1,1,1,1])-Q)
paso_esperado=np.round(np.sum(N,1))