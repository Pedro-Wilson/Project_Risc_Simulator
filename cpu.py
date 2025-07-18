# cpu.py
# Módulo responsável pela lógica dos registradores, flags e execução das instruções do processador RISC simulado.

def sign_extend(val, bits):
    """Faz sign-extend de um valor de bits bits para 16 bits."""
    if val & (1 << (bits - 1)):
        return val | (~((1 << bits) - 1) & 0xFFFF)
    return val & ((1 << bits) - 1)

# Tabela de opcodes conforme especificação do edital
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
        # 16 registradores de 16 bits (R0-R15)
        self.regs = [0] * 16
        # R14: Stack Pointer (SP), R15: Program Counter (PC)
        self.SP = 14
        self.PC = 15
        # Registrador de instrução (IR)
        self.ir = 0
        # FLAGS: 16 bits, mas só Z (bit 0) e C (bit 1) são usados
        self.FLAGS = 0
        # Registro de endereços da pilha alterados
        self.stack_accessed = set()

    def reset(self):
        """Zera todos os registradores, IR, FLAGS e inicializa SP."""
        self.regs = [0] * 16
        self.ir = 0
        self.FLAGS = 0
        self.sp = 0x8000  # Inicializa SP no topo da pilha
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
        """Flag Zero (bit 0 do FLAGS)"""
        return (self.FLAGS & 0x1) != 0

    @z.setter
    def z(self, value):
        if value:
            self.FLAGS |= 0x1
        else:
            self.FLAGS &= ~0x1

    @property
    def c(self):
        """Flag Carry (bit 1 do FLAGS)"""
        return (self.FLAGS & 0x2) != 0

    @c.setter
    def c(self, value):
        if value:
            self.FLAGS |= 0x2
        else:
            self.FLAGS &= ~0x2

    def update_flags(self, result, carry=False):
        """Atualiza as flags Z e C após operação da ULA."""
        self.z = (result & 0xFFFF) == 0
        self.c = carry

    def set_ir(self, value):
        """Define o valor do registrador de instrução (IR)."""
        self.ir = value & 0xFFFF

    def get_ir(self):
        """Obtém o valor do registrador de instrução (IR)."""
        return self.ir

    def push(self, memory, value):
        """
        Empilha um valor na pilha descendente.
        :param memory: Instância da memória
        :param value: Valor de 16 bits a ser empilhado
        """
        if self.sp == 0x0000:
            raise OverflowError("Stack overflow: SP atingiu o limite inferior da memória.")
        self.sp -= 1
        memory.write(self.sp, value)
        self.stack_accessed.add(self.sp)

    def pop(self, memory):
        """
        Desempilha um valor da pilha descendente.
        :param memory: Instância da memória
        :return: Valor de 16 bits desempilhado
        """
        if self.sp >= 0x8000:
            raise OverflowError("Stack underflow: SP atingiu o topo da pilha.")
        value = memory.read(self.sp)
        self.stack_accessed.add(self.sp)
        self.sp += 1
        return value

    def get_stack_accessed(self):
        """
        Retorna os endereços da pilha que foram alterados durante a execução.
        """
        return sorted(self.stack_accessed)

    def execute_instruction(self, instr, memory):
        """
        Decodifica e executa uma instrução de 16 bits conforme a tabela do edital.
        :param instr: instrução de 16 bits (int)
        :param memory: instância da memória
        """
        opcode = (instr >> 12) & 0xF
        op = OPCODES.get(opcode, 'NOP')

        # Campos comuns
        rd = (instr >> 8) & 0xF
        rm = (instr >> 4) & 0xF
        rn = instr & 0xF
        imm8 = instr & 0xFF
        imm4 = instr & 0xF
        addr12 = instr & 0x0FFF
        imm12 = sign_extend(instr & 0x0FFF, 12)
        imm10 = sign_extend(instr & 0x3FF, 10)

        # JMP e saltos
        if op == 'JMP':
            offset = sign_extend(instr & 0x0FFF, 12)
            if offset == 0:
                # NOP (JMP #0)
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
            return True
        elif op == 'OR':
            result = self.regs[rm] | self.regs[rn]
            self.regs[rd] = result
            self.update_flags(result)
            return True
        elif op == 'MISC':
            # Subopcodes para SHR, SHL, CMP, PUSH, POP
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
                z = self.regs[rm] == self.regs[rn]
                c = self.regs[rm] < self.regs[rn]
                self.z = z
                self.c = c
            elif subop == 0x3:  # PUSH Rn
                self.push(memory, self.regs[rn])
            elif subop == 0x4:  # POP Rd
                self.regs[rd] = self.pop(memory)
            return True
        elif op == 'HALT':
            return False  # Sinaliza parada
        else:
            pass  # Instrução desconhecida: NOP

        return True  # Continua execução

# Exemplo de ciclo principal (coloque no main.py):
def run(cpu, memory):
    cpu.reset()
    running = True
    while running:
        instr = memory.read(cpu.pc)
        cpu.set_ir(instr)
        cpu.pc = (cpu.pc + 1) & 0xFFFF
        running = cpu.execute_instruction(instr, memory)