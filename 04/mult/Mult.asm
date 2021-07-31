// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@R2		//Reset RAM[2] value to 0 before calculating
M=0

(LOOP)	//Main loop to do the calculation R0 * R1
@R1
D=M
@END	//Check if R1 is equal to 0, if yes, break the loop, if not, R2 = R2 + R0 until R1 is equal to 0
D;JEQ
@R0
D=M
@R2
M=M+D
@R1
M=M-1
@LOOP
D;JMP

(END)	//Terminate the program safely, prevent NOP slide attack
@END
0;JMP