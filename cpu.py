# cpu.py
# Módulo responsável pela lógica dos registradores, flags e execução das instruções do processador RISC simulado.

def sign_extend(val, bits):
    """Faz sign-extend de um valor de bits bits para 16 bits."""
    if val & (1 << (bits - 1)):
        return val | (~((1 << bits) - 1) & 0xFFFF)
    return val & ((1 << bits) - 1)

OPCODES = {
    0x0: 'JMP',
    0x1: 'JEQ',
    0x2: 'JNE',
    0x3: 'JLT',
    0x4: 'JGE',
    0x5: 'LDR',
    0x6: 'STR',
    0x7: 'MOV',
    0x8: 'ADD',
    0x9: 'ADDI',
    0xA: 'SUB',
    0xB: 'SUBI',
    0xC: 'AND',
    0xD: 'OR',
    0xE: 'MISC',  # SHR, SHL, CMP, PUSH, POP (subop)
    0xF: 'HALT'
}

class CPU:
    def __init__(self):
        self.regs = [0] * 16
        self.SP = 14
        self.PC = 15
        self.ir = 0
        self.FLAGS = 0
        self.stack_accessed = set()

    def reset(self):
        self.regs = [0] * 16
        self.ir = 0
        self.FLAGS = 0
        self.sp = 0x8000
        self.stack_accessed.clear()

    @property
    def sp(self):
        return self.regs[self.SP]

    @sp.setter
    def sp(self, value):
        self.regs[self.SP] = value & 0xFFFF

    @property
    def pc(self):
        return self.regs[self.PC]

    @pc.setter
    def pc(self, value):
        self.regs[self.PC] = value & 0xFFFF

    @property
    def z(self):
        return (self.FLAGS & 0x1) != 0

    @z.setter
    def z(self, value):
        if value:
            self.FLAGS |= 0x1
        else:
            self.FLAGS &= ~0x1

    @property
    def c(self):
        return (self.FLAGS & 0x2) != 0

    @c.setter
    def c(self, value):
        if value:
            self.FLAGS |= 0x2
        else:
            self.FLAGS &= ~0x2

    def update_flags(self, result, carry=False):
        self.z = (result & 0xFFFF) == 0
        self.c = carry

    def set_ir(self, value):
        self.ir = value & 0xFFFF

    def get_ir(self):
        return self.ir

    def push(self, memory, value):
        print(f"PUSH: SP antes = 0x{self.sp:04X}, valor = 0x{value:04X}")
        if self.sp == 0x0000:
            raise OverflowError("Stack overflow: SP atingiu o limite inferior da memória.")
        self.sp -= 1
        memory.write(self.sp, value)
        self.stack_accessed.add(self.sp)
        print(f"PUSH: SP depois = 0x{self.sp:04X}")

    def pop(self, memory):
        print(f"POP: SP antes = 0x{self.sp:04X}")
        if self.sp >= 0x8000:
            raise OverflowError("Stack underflow: SP atingiu o topo da pilha.")
        value = memory.read(self.sp)
        self.stack_accessed.add(self.sp)
        self.sp += 1
        print(f"POP: SP depois = 0x{self.sp:04X}, valor = 0x{value:04X}")
        return value

    def get_stack_accessed(self):
        return sorted(self.stack_accessed)

    def execute_instruction(self, instr, memory):
        opcode = (instr >> 12) & 0xF
        op = OPCODES.get(opcode, 'NOP')

        rd = (instr >> 8) & 0xF
        rm = (instr >> 4) & 0xF
        rn = instr & 0xF
        imm8 = instr & 0xFF
        imm4 = instr & 0xF

        if op == 'JMP':
            offset = sign_extend(instr & 0x0FFF, 12)
            if offset == 0:
                return True
            self.pc = (self.pc + offset) & 0xFFFF
            return True
        elif op == 'JEQ':
            offset = sign_extend(instr & 0x3FF, 10)
            if self.z:
                self.pc = (self.pc + offset) & 0xFFFF
            return True
        elif op == 'JNE':
            offset = sign_extend(instr & 0x3FF, 10)
            if not self.z:
                self.pc = (self.pc + offset) & 0xFFFF
            return True
        elif op == 'JLT':
            offset = sign_extend(instr & 0x3FF, 10)
            if not self.z and self.c:
                self.pc = (self.pc + offset) & 0xFFFF
            return True
        elif op == 'JGE':
            offset = sign_extend(instr & 0x3FF, 10)
            if self.z or not self.c:
                self.pc = (self.pc + offset) & 0xFFFF
            return True
        elif op == 'LDR':
            self.regs[rd] = memory.read(self.regs[rm])
            self.update_flags(self.regs[rd])
            return True
        elif op == 'STR':
            memory.write(self.regs[rm], self.regs[rn])
            return True
        elif op == 'MOV':
            self.regs[rd] = imm8
            self.update_flags(self.regs[rd])
            return True
        elif op == 'ADD':
            result = (self.regs[rm] + self.regs[rn]) & 0xFFFF
            carry = (self.regs[rm] + self.regs[rn]) > 0xFFFF
            self.regs[rd] = result
            self.update_flags(result, carry)
            return True
        elif op == 'ADDI':
            result = (self.regs[rm] + imm4) & 0xFFFF
            carry = (self.regs[rm] + imm4) > 0xFFFF
            self.regs[rd] = result
            self.update_flags(result, carry)
            return True
        elif op == 'SUB':
            result = (self.regs[rm] - self.regs[rn]) & 0xFFFF
            carry = self.regs[rm] < self.regs[rn]
            self.regs[rd] = result
            self.update_flags(result, carry)
            return True
        elif op == 'SUBI':
            result = (self.regs[rm] - imm4) & 0xFFFF
            carry = self.regs[rm] < imm4
            self.regs[rd] = result
            self.update_flags(result, carry)
            return True
        elif op == 'AND':
            result = self.regs[rm] & self.regs[rn]
            self.regs[rd] = result
            self.update_flags(result)
            print(f"AND: R{rd} = 0x{result:04X}")
            return True
        elif op == 'OR':
            result = self.regs[rm] | self.regs[rn]
            self.regs[rd] = result
            self.update_flags(result)
            return True
        elif op == 'MISC':
            subop = (instr >> 8) & 0xF
            if subop == 0x0:  # SHR Rd, Rm, #Im
                result = (self.regs[rm] >> imm4) & 0xFFFF
                self.regs[rd] = result
                self.update_flags(result)
            elif subop == 0x1:  # SHL Rd, Rm, #Im
                result = (self.regs[rm] << imm4) & 0xFFFF
                self.regs[rd] = result
                self.update_flags(result)
            elif subop == 0x2:  # CMP Rm, Rn
                self.z = self.regs[rm] == self.regs[rn]
                self.c = self.regs[rm] < self.regs[rn]
            elif subop == 0x3:  # PUSH Rn
                print(f"PUSH instruction: registrador R{rn} = 0x{self.regs[rn]:04X}")
                self.push(memory, self.regs[rn])
                print(f"SP após PUSH: 0x{self.sp:04X}")
            elif subop == 0x4:  # POP Rd (bits 7-4)
                rd_pop = (instr >> 4) & 0xF
                value = self.pop(memory)
                self.regs[rd_pop] = value
                print(f"POP instruction: registrador R{rd_pop} = 0x{value:04X}")
                print(f"SP após POP: 0x{self.sp:04X}")
            return True
        elif op == 'HALT':
            return False
        else:
            return True

# Exemplo de ciclo principal (para colocar no main.py):
def run(cpu, memory):
    cpu.reset()
    running = True
    instruction_count = 0
    max_instructions = 10000
    while running:
        instr = memory.read(cpu.pc)
        cpu.set_ir(instr)
        cpu.pc = (cpu.pc + 1) & 0xFFFF
        running = cpu.execute_instruction(instr, memory)
        instruction_count += 1
        if instruction_count >= max_instructions:
            print("WARNING: Limite máximo de instruções executadas atingido. Possível loop infinito.")
            break
