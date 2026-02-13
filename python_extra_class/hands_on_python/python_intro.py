"""
Method #1 de python
"""

#######################
# --- Calculadora --- #
#######################

# Suma
print(8 + 8)
# Resta
print(7 - 1)
# Multiplicacion
print(8 * 8)
# Division
print(8 / 2)

# -------------
import math

print(math.sqrt(81))


# -------- Funciones --------- #


def circunferencia(radio):
    """pi * radius"""
    try:
        pi = math.pi
        area = pi * radio**2
        return print(area)
    except TypeError as e:
        print(f"{radio} No es un valor que pueda ejecutar!!!! 😅")
        pass


circunferencia("Carlos")


# -------------------------


lista_de_nombres = ["Adri", "El Mauro", "El Carlos", "El Pato"]
# lista_de_nombres[0] = int(1)
# print(lista_de_nombres)

for i in lista_de_nombres:
    print(f"Es {i} miembro del curso")


for i in list(range(2, 8)):
    cualquier_cosa = 8 * i
    print(cualquier_cosa)


def cuadraro(i):
    return i**2


for i in range(101):
    new_val = cuadraro(i)
    print(f"el cuadrado de {i} es {new_val}")


# ----------------------------

dias = ["lunes", "martes", "viernes", "sabado"]

for i in dias:
    if i == "viernes":
        print(f"{i} Es hora de tomar unas buenas cervezas con el Carlos !!!")
    elif i == "sabado":
        print(f"{i} NO me llamen, estoy durmiendo")
    else:
        print(f"{i} Toca estudiar programacion!")


def quehaypahacer(day):
    if day == "Viernes":
        # print("Toca Cervecita!!")
        return print(f"{day} es dia de desordenarse!")
    else:
        print("TOca Estudiar")


day = "Viernes"

quehaypahacer(day)


# -----------------------------
# n = int(input("Hey dame un numero del 1 al 10!!! "))

# seq = [0, 1]

# for i in range(2, n):
#    seq.append(seq[i - 1] + seq[i - 2])
# print(seq)


# -------------------


def fib(sec_len):
    """fibonacci function"""
    sec = [0, 1]
    if sec_len <= 1:
        print("Hey Bro esto no tiene elementos !!!")
        return
    elif 0 < sec_len < 3:
        return sec[:sec_len]
    for i in range(2, sec_len):
        sec.append(sec[i - 1] + sec[i - 2])
    return sec


print(fib(1))
print(fib(4))
print(fib(10))


# -----------------
# ===========================
# Tuplas
# =========================

lista_de_estudiantes = {"Pato": 20, "Adri": 15}

print(len(lista_de_estudiantes))


# -------------

import numpy as np
import scipy as sp

array = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
# print(array * 2)

print(np.zeros((3, 3)))


df = np.linspace(0, 2)
# print(np.sin(df))

import matplotlib.pyplot as plt


# plt.plot(df, np.sin(df))
# plt.title("El grafico de sin")
# plt.show()

print()
print()
print("==" * 64)
# ----------------------
import pandas as pd


df = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-01-13/africa.csv"
)
print(df.head())

print(df.isnull().sum())


print(df["country"].value_counts(ascending=False))
