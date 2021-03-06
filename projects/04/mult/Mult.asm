// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Pseudocode
//-----------------------------------
// int a = firstNumber
// int b = secondNumber

// int i = 0
// int sum = 0

// LOOP:
//     if(b - i == 0) goto STOP
//
//     sum += a
//     i++
//     goto LOOP

// STOP:
//     goto STOP
//-----------------------------------

//initialize loop counter and sum register
@i
M=0
@R2
M=0

(LOOP)
    //if RAM[1] - i == 0 end loop
    @R1
    D=M
    @i
    D=D - M

    @STOP
    D;JEQ

    //increment sum
    @R0
    D=M
    @R2
    M=M + D

    //increment i
    @i
    M=M + 1

    @LOOP
    0;JMP

(STOP)
    @STOP
    0;JMP