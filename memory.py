# memory.py
# Módulo responsável pela implementação e manipulação da memória de dados e instruções do simulador.

import io


class Memory:
    def __init__(self, size=0x10000):
        """
        Inicializa a memória zerada.
        :param size: Tamanho total da memória (default: 65536 palavras de 16 bits)
        """
        self.size = size
        self.mem = [0] * size  # Cada posição armazena 16 bits
        self.accessed = set()  # Endereços acessados (leitura ou escrita)

    def read(self, address):
        """
        Lê o valor de um endereço de memória ou realiza operação de E/S se for endereço especial.
        :param address: Endereço a ser lido (int)
        :return: Valor de 16 bits armazenado no endereço ou valor lido da E/S
        """

        #if 0x0000 <= address < 0x8000:
        if not (0 <= address < self.size):
            self.accessed.add(address)
            return self.mem[address] & 0xFFFF
        elif address == 0xF000:
            return ord(io.read_char())
        elif address == 0xF001:
            return io.read_int()
        else:
            raise ValueError(f"Endereço de leitura inválido: {hex(address)}")

    def write(self, address, value):
        """
        Escreve um valor em um endereço de memória ou realiza operação de E/S se for endereço especial.
        :param address: Endereço a ser escrito (int)
        :param value: Valor a ser armazenado (int, 16 bits)
        """
        if 0x0000 <= address < 0x8000:
            self.mem[address] = value & 0xFFFF
            self.accessed.add(address)
        elif address == 0xF002:
            io.write_char(chr(value & 0xFF))
        elif address == 0xF003:
            io.write_int(value)
        else:
            raise ValueError(f"Endereço de escrita inválido: {hex(address)}")

    def get_accessed(self):
        """
        Retorna uma lista dos endereços acessados durante a execução.
        """
        return sorted(self.accessed)

    def reset(self):
        """
        Zera toda a memória e limpa o registro de acessos.
        """
        self.mem = [0] * self.size
        self.accessed.clear()