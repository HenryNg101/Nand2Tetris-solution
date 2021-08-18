// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Main loop to check if there's any key pressed or not
(LOOP)	
@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ

// When there's no key pressed
(WHITE)

@8192
D=A

@WHITELOOP
0;JMP

// Smaller loop to draw all white to the screen
(WHITELOOP)
@SCREEN
A=A+D
A=A-1
M=0			//Fill with white color (0 = 0000000000000000)
D=D-1

@LOOP
D;JLE

@WHITELOOP
D;JGT

//When there's any key pressed
(BLACK)
@SCREEN
D=M
@LOOP
D;JLT

@8192
D=A

@BLACKLOOP
0;JMP

//Smaller loop to draw black to the screen
(BLACKLOOP)
@SCREEN
A=A+D
A=A-1
M=-1		//Fill with black color (-1 = 1111111111111111)
D=D-1

@LOOP
D;JLE

@BLACKLOOP
D;JGT