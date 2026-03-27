"""
Introduccion al pensamiento computacional
        con Python

"""

# -------------- #
#   Calculadora  #
# ----------------#


print(2 + 2)

import math

print(math.sqrt(16))


def calcular_el_radio(input):
    try:
        output = math.pi * input**2
        return output
    except:
        print("Error in this operation")


print(calcular_el_radio(15))


# ------------------------------------------#
#         EL manejo de Listas               #
# -------------------------------------------#

print("==" * 32)
print("Manejo de listas")
dias_de_la_semana = ["Lunes", "Viernes", "Domingo"]

print("Extraccion del dia de la semana: ", dias_de_la_semana[0])

dias_de_la_semana[0] = "Martes"

print(dias_de_la_semana)

dias_de_la_semana.append("Sabado")

print(dias_de_la_semana)
print(len(dias_de_la_semana))


print("==" * 32)
print("Iteracciones")

for i in dias_de_la_semana:
    print("Es un dia comun: ", i)


print("##" * 32)
for i in dias_de_la_semana:
    if i == "Viernes":
        print("Este dia es mi favorito", i)
    elif i == "Domingo":
        print(i, "Anda toca lavar Ropa!!!")
    else:
        print("Un Dia normal", i)

print("##" * 32)

# for i in range(30):
#    print("Mira el cuadrado de ese # es: ", i * i)

print("##" * 36)
print("Optimizacion")

[print(f"MIra el cuadrado de este input {i*i}") for i in range(30)]


print("==" * 32)
print("Belen" == "Facu")


# ==
# !=

print("==" * 32)
print("Creando Fibonacci")


def fibonacci():
    input_leng = input("Hey Dame un numero")
    input_leng = int(input_leng)
    seq = [0, 1]
    for i in range(2, input_leng):
        seq.append((seq[i - 1] + seq[i - 2]))
    print(seq)


fibonacci()


print("==" * 32)
print("Una funcion mas seria")


def fibo_con_peros(seq_leng):
    """un ejemplo de una funcion con varios peros"""
    seq = [0, 1]
    if seq_leng < 1:
        print("🚨 Hey necesito mas de un sample para poder operar")
        return
    if 0 < seq_leng < 4:
        print("Puedo operar")
        return seq[:seq_leng]
    for i in range(2, seq_leng):
        seq.append(seq[i - 1] + seq[i - 2])
    return seq


print(fibo_con_peros(3))
help(fibo_con_peros)
