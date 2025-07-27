START:
    MOV R0, #10        ; Inicializa R0 com 10
    MOV R1, #20        ; Inicializa R1 com 20
    ADD R2, R0, R1     ; R2 = R0 + R1 (30)
    SUB R3, R1, R0     ; R3 = R1 - R0 (10)
    AND R4, R2, R3     ; R4 = R2 & R3 (30 & 10 = 10)
    OR R5, R0, R1      ; R5 = R0 | R1 (10 | 20 = 30)
    PUSH R2            ; Empilha R2 (30)
    PUSH R3            ; Empilha R3 (10)
    POP R6             ; Desempilha para R6 (10)
    POP R7             ; Desempilha para R7 (30)
    CMP R6, R7         ; Compara R6 e R7 (Z=0, C=1)
    JEQ EQUAL          ; Se iguais, salta para EQUAL
    JNE NOTEQUAL       ; Se diferentes, salta para NOTEQUAL

EQUAL:
    MOV R8, #1         ; R8 = 1 (indicando igualdade)
    JMP END

NOTEQUAL:
    MOV R8, #0         ; R8 = 0 (indicando diferença)

END:
    HALT               ; Finaliza execução
