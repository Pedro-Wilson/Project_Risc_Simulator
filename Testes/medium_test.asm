 MOV R0, #5
 MOV R1, #3
 ADD R2, R0, R1
 SUB R3, R0, R1
 AND R4, R0, R1
 OR R5, R0, R1
 PUSH R2
 POP R6
 HALT

        MOV R0, #5       ; R0 = 5
        MOV R1, #3       ; R1 = 3
        ADD R2, R0, R1   ; R2 = 8
        SUB R3, R0, R1   ; R3 = 2
        AND R4, R0, R1   ; R4 = 1
        OR R5, R0, R1    ; R5 = 7
        PUSH R2          ; empilha R2 (8)
        POP R6           ; desempilha para R6
        HALT             ; para execução
