# io.py
# Módulo responsável pelo sistema de entrada e saída mapeado em memória (endereços especiais de E/S).

# io.py
def read_char():
    return input("Digite um caractere: ")

def read_int():
    return int(input("Digite um inteiro: "))

def write_char(char):
    print(char, end="")

def write_int(int):
    print(int, end="")