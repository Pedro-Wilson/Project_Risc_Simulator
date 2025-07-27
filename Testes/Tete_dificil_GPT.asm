        MOV R0, #0xFF
        MOV R1, #0x0A
        ADD R2, R0, R1
        SUB R3, R2, R1
        AND R4, R2, R3
        OR  R5, R4, R1
        ADDI R6, R5, #0xF
        SUBI R7, R6, #0x1
        CMP R7, R5
        SHL R8, R7, #3
        SHR R9, R8, #2
        PUSH R9
        POP R10
        STR R10, [R1]
        LDR R11, [R1]
        JEQ LABEL1
        JNE LABEL2
        JLT LABEL3
        JGE LABEL4
        JMP END

LABEL1: ADD R12, R11, R0
LABEL2: SUB R13, R12, R1
LABEL3: OR  R14, R13, R2
LABEL4: AND R15, R14, R3
        NOP
END:    HALT
