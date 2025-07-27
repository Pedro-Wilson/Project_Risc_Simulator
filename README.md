# Simulador de Processador RISC - UFC

Este repositório contém a implementação de um simulador de processador RISC de 16 bits, desenvolvido como trabalho final da disciplina de Arquitetura de Computadores da Universidade Federal do Ceará (UFC), Campus de Quixadá.

---

## Estrutura do Projeto

O projeto está modularizado nos seguintes arquivos:

- **`cpu.py`**: Implementação dos registradores, flags, lógica de execução das instruções, manipulação da pilha e ciclo de execução.
- **`memory.py`**: Implementação da memória de dados e instruções, incluindo métodos de leitura/escrita e mapeamento de E/S.
- **`io.py`**: Sistema de entrada e saída mapeado em memória (endereços especiais para CHAR/INT IN/OUT).
- **`assembler.py`**: Tradução de código Assembly para binário/hexadecimal, com suporte a labels e validação de sintaxe.
- **`main.py`**: Arquivo principal para inicialização, carregamento do programa, execução do simulador e exibição do estado final.
- **`utils.py`**: Funções auxiliares para manipulação de dados, conversão, etc.
- **`README.md`**: Este arquivo de documentação.

---

## Objetivos

- Simular a execução de programas em Assembly ou hexadecimal em um processador RISC de 16 bits.
- Implementar 16 registradores de uso geral (R0–R15), incluindo ponteiro de pilha (SP = R14) e contador de programa (PC = R15).
- Implementar registrador de instrução (IR) e registrador de flags (FLAGS), com bits Zero (Z) e Carry (C).
- Permitir leitura de programas a partir de arquivos texto, preenchendo a memória de instruções e dados.
- Executar corretamente o conjunto de instruções especificado no edital, incluindo operações aritméticas, lógicas, controle de fluxo, acesso à memória, manipulação de pilha e sistema de E/S mapeado em memória.
- Exibir, ao final da execução, o estado dos registradores, memória acessada, pilha (se alterada) e flags.

---

## Conjunto de Instruções

O processador simulado suporta 19 instruções de 16 bits, incluindo:

- **Saltos:** JMP, JEQ, JNE, JLT, JGE
- **Acesso à memória:** LDR, STR
- **Movimentação:** MOV
- **Aritméticas:** ADD, ADDI, SUB, SUBI
- **Lógicas:** AND, OR
- **Deslocamento:** SHR, SHL
- **Comparação:** CMP
- **Pilha:** PUSH, POP
- **Controle:** HALT, NOP (JMP #0)

Consulte o edital ou o código para detalhes de formato binário e campos de cada instrução.

---

## Sistema de Entrada/Saída (E/S)

Endereços especiais mapeados em memória:
- `0xF000`: CHAR IN (leitura de caractere)
- `0xF001`: INT IN (leitura de inteiro)
- `0xF002`: CHAR OUT (escrita de caractere)
- `0xF003`: INT OUT (escrita de inteiro)

A leitura/escrita nesses endereços é feita via instruções LDR/STR.

---

## Como Usar

1. Certifique-se de que todos os módulos estejam implementados conforme a especificação.
2. Prepare um arquivo de programa em Assembly (usando o `assembler.py`) ou hexadecimal, seguindo o formato `<endereço>:<conteúdo>`.
3. Para montar um programa Assembly, execute:
    ```bash
    python3 assembler.py <arquivo_assembly> <arquivo_hexadecimal>
    ```
4. Execute o simulador com:
    ```bash
    python3 main.py <arquivo_programa>
    ```
5. O simulador irá carregar o programa, executar as instruções e exibir o estado final dos componentes.

---

## Saída do Simulador

Ao final da execução (ou ao executar NOP), o simulador exibirá:
- Estado final dos registradores (R0–R15, SP, PC).
- Conteúdo da memória de dados acessada durante a execução.
- Conteúdo da pilha (se alterada).
- Flags Z e C.

Exemplo de saída:
```
Registradores:
R0 : 0x0003
R1 : 0x0000
...
SP : 0x8000
PC : 0x0004

Memória de Dados:
000A: 0x0005

Pilha:
[mostrada apenas se SP != 0x8000]

Flags:
Z = 0
C = 0
```

---

## Exemplos de Entrada

### Exemplo em hexadecimal:
```
0000:4003
0001:6202
0002:4A0A
0003:3002
0004:FFFF
```

### Exemplo em Assembly:
```
MOV R0, #3
ADDI R2, R0, #2
MOV R10, #10
STR R2, [R0]
HALT
```

---

## Requisitos Atendidos

- Estrutura modular e documentação.
- Registradores, flags, memória, pilha e E/S implementados.
- Conjunto de instruções completo.
- Ciclo fetch-decode-execute implementado.
- Saída conforme edital.
- Montador (assembler) funcional com suporte a labels e validação de sintaxe.

## Créditos

Projeto desenvolvido para fins acadêmicos na disciplina de Arquitetura de Computadores – UFC.

Desenvolvido por: Pedro Wilson C. Parreira  
Professor responsável: Pedro Botelho  
Campus de Quixadá – Universidade Federal do Ceará  
Data: 09/07 à 27/07/2025 -- ainda não fincalizado 


---
