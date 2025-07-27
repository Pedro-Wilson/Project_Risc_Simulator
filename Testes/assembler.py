# assembler.py
# Módulo responsável por traduzir código Assembly para binário/hexadecimal, permitindo pontos extras no projeto.

import sys
import re


OPCODES = {
    'JMP':  0x0,
    'JEQ':  0x1,
    'JNE':  0x2,
    'JLT':  0x3,
    'JGE':  0x4,
    'LDR':  0x5,
    'STR':  0x6,
    'MOV':  0x7,
    'ADD':  0x8,
    'ADDI': 0x9,
    'SUB':  0xA,
    'SUBI': 0xB,
    'AND':  0xC,
    'OR':   0xD,
    'SHR':  0xE0,  # MISC subop 0
    'SHL':  0xE1,  # MISC subop 1
    'CMP':  0xE2,  # MISC subop 2
    'PUSH': 0xE3,  # MISC subop 3
    'POP':  0xE4,  # MISC subop 4
    'HALT': 0xF,
    'NOP':  0x0,   # NOP é JMP #0
}

REGS = {f'R{i}': i for i in range(16)}
REGS['SP'] = 14
REGS['PC'] = 15

def parse_reg(s):
    s = s.strip().upper()
    if s in REGS:
        return REGS[s]
    raise ValueError(f"Registrador inválido: {s}")

def parse_imm(s):
    s = s.strip()
    if s.startswith('#'):
        s = s[1:]
    if s.startswith('0x'):
        return int(s, 16)
    return int(s)

def assemble_line(line, labels, addr):
    # Remove comentários
    line = line.split('//')[0].strip()
    if not line:
        return None
    # Label
    if ':' in line:
        label, rest = line.split(':', 1)
        line = rest.strip()
        if not line:
            return None
    if not line:
        return None
    tokens = re.split(r'[,\s]+', line)
    instr = tokens[0].upper()
    args = tokens[1:]
    opcode = OPCODES.get(instr)
    if opcode is None:
        raise ValueError(f"Instrução desconhecida: {instr}")

    # Montagem por instrução
    if instr == 'JMP':
        # JMP label ou JMP #im
        if args[0] in labels:
            offset = labels[args[0]] - addr
        else:
            offset = parse_imm(args[0])
        code = (opcode << 12) | (offset & 0x0FFF)
    elif instr in ('JEQ', 'JNE', 'JLT', 'JGE'):
        if args[0] in labels:
            offset = labels[args[0]] - addr
        else:
            offset = parse_imm(args[0])
        code = (opcode << 12) | (offset & 0x03FF)
    elif instr == 'LDR':
        if len(args) != 2 or not (args[1].startswith('[') and args[1].endswith(']')):
            raise ValueError(f"Formato inválido para LDR: {args}")
        rd = parse_reg(args[0])
        rm = parse_reg(args[1][1:-1])  # [Rm]
        code = (opcode << 12) | (rd << 8) | (rm << 4)
    elif instr == 'STR':
        if len(args) != 2 or not (args[1].startswith('[') and args[1].endswith(']')):
            raise ValueError(f"Formato inválido para STR: {args}")
        rn = parse_reg(args[0])
        rm = parse_reg(args[1][1:-1])  # [Rm]
        code = (opcode << 12) | (rm << 4) | rn
    elif instr == 'MOV':
        rd = parse_reg(args[0])
        im = parse_imm(args[1])
        code = (opcode << 12) | (rd << 8) | (im & 0xFF)
    elif instr == 'ADD':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        rn = parse_reg(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | rn
    elif instr == 'ADDI':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        im = parse_imm(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | (im & 0xF)
    elif instr == 'SUB':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        rn = parse_reg(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | rn
    elif instr == 'SUBI':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        im = parse_imm(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | (im & 0xF)
    elif instr == 'AND':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        rn = parse_reg(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | rn
    elif instr == 'OR':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        rn = parse_reg(args[2])
        code = (opcode << 12) | (rd << 8) | (rm << 4) | rn
    elif instr == 'SHR':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        im = parse_imm(args[2])
        code = (0xE << 12) | (0x0 << 8) | (rd << 4) | (rm << 0) | (im & 0xF)
    elif instr == 'SHL':
        rd = parse_reg(args[0])
        rm = parse_reg(args[1])
        im = parse_imm(args[2])
        code = (0xE << 12) | (0x1 << 8) | (rd << 4) | (rm << 0) | (im & 0xF)
    elif instr == 'CMP':
        rm = parse_reg(args[0])
        rn = parse_reg(args[1])
        code = (0xE << 12) | (0x2 << 8) | (rm << 4) | rn
    elif instr == 'PUSH':
        rn = parse_reg(args[0])
        code = (0xE << 12) | (0x3 << 8) | rn
    elif instr == 'POP':
        rd = parse_reg(args[0])
        code = (0xE << 12) | (0x4 << 8) | (rd << 4)
    elif instr == 'HALT':
        code = 0xFFFF
    elif instr == 'NOP':
        code = 0x0000
    else:
        raise ValueError(f"Instrução não suportada: {instr}")
    return code

def assemble_file(input_file, output_file):
    # Primeira passagem: encontrar labels
    labels = {}
    lines = []
    addr = 0
    with open(input_file) as f:
        for line in f:
            l = line.split('//')[0].strip()
            if not l:
                continue
            if ':' in l:
                label = l.split(':')[0].strip()
                labels[label] = addr
                l = l.split(':', 1)[1].strip()
                if not l:
                    continue
            lines.append((addr, line.strip()))
            addr += 1

    # Segunda passagem: montar instruções
    with open(output_file, 'w') as out:
        for addr, line in lines:
            try:
                code = assemble_line(line, labels, addr)
                if code is not None:
                    out.write(f"{addr:04X}:{code:04X}\n")
            except Exception as e:
                print(f"Erro na linha {addr}: {e}")
                sys.exit(1)

    print(f"Montagem concluída: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: assembler.py <arquivo_entrada.asm> <arquivo_saida.hex>")
        sys.exit(1)
    assemble_file(sys.argv[1], sys.argv[2])