# main.py
# Ponto de entrada do simulador RISC.
# Exemplo de uso: python3 main.py teste.hex
# Exemplo de uso: python3 assembler.py teste.asm teste.hex

import sys
from cpu import CPU, run
from memory import Memory

def load_program(memory, filename):
    """
    Carrega um programa em hexadecimal no formato <endereço>:<conteúdo>
    """
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            addr, value = line.split(':')
            addr = int(addr, 16)
            value = int(value, 16)
            memory.mem[addr] = value & 0xFFFF

def print_state(cpu, memory):
    print("Registradores:")
    for i in range(16):
        nome = f"SP" if i == 14 else ("PC" if i == 15 else f"R{i}")
        print(f"{nome}: 0x{cpu.regs[i]:04X}")
    print("\nMemória de Dados:")
    accessed = memory.get_accessed()
    if accessed:
        for addr in accessed:
            print(f"{addr:04X}: 0x{memory.mem[addr]:04X}")
    else:
        print("(nenhum endereço acessado)")
    if cpu.sp != 0x8000 and cpu.get_stack_accessed():
        print("\nPilha:")
        for addr in cpu.get_stack_accessed():
            print(f"{addr:04X}: 0x{memory.mem[addr]:04X}")
    print("\nFlags:")
    print(f"Z = {int(cpu.z)}")
    print(f"C = {int(cpu.c)}")
    print("\n--- Fim da execução ---")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <arquivo_programa>")
        return
    cpu = CPU()
    memory = Memory()
    load_program(memory, sys.argv[1])
    run(cpu, memory)
    print_state(cpu, memory)

if __name__ == "__main__":
    main()