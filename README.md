# Nand2Tetris-solution
This is my own code solution for the [Nand2Tetris](https://www.nand2tetris.org/) course.

Hack Translator usage: (Will added later)

So, what is Nand2Tetris project about. It's basically just, learning how to build a basic computer system. Through the entire course, you will learn how to build a hardware architecture and write necessary software that's needed for a basic computer. Alright, so, let's get into it.

## Part 1: Hardware
### Boolean logics and arithmetics (Mathematical & Logical operations)
So, to build a computer system, what do you need to have ? To start with it, you just need some computer chips. Basic chips combine tog
ether form more complex chips, then more complex chips combine together, to create a computer system.

But, the first chip to start with, is the Nand chips (That's why this course is called "Nand2Tetris"). It's the most basic chip unit, from that you can build many other chips with it. You will need to build logical chips first. They are chips that receive inputs as 0(s)and 1(s), and the final output from these chips are also be 0 or 1 (true or false state, that's the reason they are called "logic gates").

After you have all of the logical chips, it's time to create boolean arithmetic chips. These chips are responsible for doing basic nume
rical arithmetics like addition and subtraction (Multiplication and division will be built later). Your final goal is to build a basic
ALU (Arithmetic Logic Unit), to do some bitwise and numerical arithmetic operations.
### Sequential Logic (Persistence storage)
In computer, it uses a clockto represent the time, it often cycles between 0 and 1, ot "tick" and "tock". To start with sequential logic, you need a special chip to start with, which is Data Flip-Flop chip. This chip contains will output the inputted data of previous clock's cycle (which means that, out(t) = in(t-1), t is the clock's time). Since the DFF can't contain the same data over time, you need a register to do that. A register is similar to DFF, except that it has the other option to store same data over time. From there you build 16-bit registers, and small RAM (consists of registers), and bigger RAMs contains smaller RAMs.

However, there's a special case, which is program counter. It's a chip that can increase it's value over time, when clock ticks. It's very important to be used to count and find current assembly instruction of a program, when you can reset (go back to beginning of the program), load with specific value (branching and jumps).

### Assembly language (Low-level instructions for computer)
Is a language used to provide instructions for CPU. Assembly language can access some different things: Memory (RAM Access), Registers (Fast memory access, but limited), CPU (Different operations). There are different types of memory access operations, direct addressng to access a very specific memory location, immediate addressing to load values in instruction code to memory, and indirect addressing, used to handle pointers and array access. Control flow helps the program counter to jump from one location to an arbitrary location, which helps with branching and looping. 

For Hack language, there are only 2 types of instructions, A and C instructions. The A instructions are used to access a specific memory address. It changes the A register's value, which points to memory location, we can access data in any location with M register. And then there is C instructions, used to do computations, save result to a register (A, M or D (D is register where you can store whateber temporary data)). There's still more details in the book, you can check it out.

### Computer architecture (Build a complete computer, and for Hack computer)
Based on Von Neumman architecture, a computer consists of memory and a CPU. The memory stores data (memory, variables, objects) and program instructions. 

The memory consists of read-only memory (ROM), which contains instructions, and dynamic memory (RAM), to store and access data. In RAM, there are 3 data segments (memory map (Store just data), screen data(Store screen color, which is black and white), and keyboard data (store information on what key has been pressed)). 

CPU process instructions by performing arithmetic operations with ALU, store immediate results in registers (D and A registers), and updates program counter know what is the next instruction to execute.

### Assembler (Hack assembler)
Just a tool to translate Hack Assembly instructions to binary code, which can be processed by Hack CPU. Check out the different way to process A, C instructions, and how to process different fields (destionation, computation, jumps) in the book.

## Part 2: Software (How it can be connected with hardware)

### Virtual Machine (Jack VM)
A tool to translate VM code (bytecode) into assembly (Hack assembly) language. Virtual Machine code are the code that are used as intermediate code between assembly and high-level code (like Java, C#). This allows different devices with different Assembly specifications and architectures can still compile the same code, that makes Java is the "Write once, run everywhere" code. 

There are 4 different types of operations in VM language: Arithmetic/Logical commands (For calculations), Memory access (push/pop in memory stack) commands, branching commands (for creating labels and jump to label) and function commands (function creation, function calls and return). Read more in the book and watch videos for more information.

For the tool usage, go to the "VM Translator" directory and check README.md

### Compiler (Jack Compiler)
A tool to compile high-level language code (Jack) into VM code (or bytecode). Jack language is kinda like Java. 

For a compiler, there are several steps to compile from high-level code to intermediate code (VM code). They includes tokenization (breaks down the code base into different lexical elements (keywords, values, etc)), parsing (from simple lexoical elements that we got by breaking down the code base, we try to build more complex structure (statements, expression, etc) from that code, which results in parsing tree, often stored as XML), and code generation (Generate VM code from the parsing tree). For more details on how to do each step for Jack language, with different algorithms, read more in the book and videos.

For the tool usage, go to the "Jack Compiler" directory and check README.md

### OS (Haven't complete yet)
