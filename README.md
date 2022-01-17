# Nand2Tetris-solution
This is my own code solution for the [Nand2Tetris](https://www.nand2tetris.org/) course part 1 (Computer hardware), including the Hack assembler

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



### Computer architecture (Build a complete computer)
### Assembly language (Low-level instructions for computer)
