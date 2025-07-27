main:   MOV R10, #0xF0      
        SHL R11, R10, #8    
        ADDI R12, R11, #1   
        LDR R1, [R12]       
        PUSH R1             
        MOV R13, #0         

read:   CMP R1, R13         
        JEQ call            
        LDR R5, [R12]       
        STR R5, [R10]       
        ADDI R10, R10, #1   
        SUBI R1, R1, #1     
        JMP read            

call:   POP R1              
        SUB R0, R10, R1     
        ADDI R10, PC, #2    
        PUSH R10            
        JMP arrsum          

print:  ADDI R12, R11, #3   
        STR R0, [R12]       
        HALT                

arrsum: PUSH R4             
        PUSH R5             
        ADDI R4, R1, #0     
        JEQ exit            
        MOV R4, #0x00       
loop:   LDR R5, [R0]        
        ADD R4, R4, R5      
        ADDI R0, R0, #1     
        SUBI R1, R1, #1     
        JNE loop            
        ADDI R0, R4, #0     
exit:   POP R5              
        POP R4              
        POP PC              