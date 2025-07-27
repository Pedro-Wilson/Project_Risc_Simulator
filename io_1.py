# io.py
def read_char():
    entrada = input("Digite um caractere: ")
    return entrada[0] if entrada else '\0'

def read_int():
    while True:
        try:
            valor = int(input("Digite um inteiro: "))
            return valor & 0xFFFF  # limita a 16 bits
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro válido.")

def write_char(char):
    print(char, end="", flush=True)

def write_int(num):
    print(num, end="", flush=True)
