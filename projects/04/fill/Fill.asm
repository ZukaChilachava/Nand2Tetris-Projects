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

// Pseudocode
//---------------------------------------------------
// screensize = 8192

// OUTERLOOP:
//     color = 0
//     currentPos = SCREEN
//     if(!keyPressed) goto PAINTLOOP
//     else color = 1

//     PAINTLOOP:
//         RAM[currentPos] = color
//         currentPos++
//         int k = SCREEN + screenSize - currentPos
//         if(k == 0) goto OUTERLOOP
//         else goto PAINTLOOP

// goto OUTERLOOP
//---------------------------------------------------

@8192
D=A

@screensize
M=D

(OUTERLOOP)
    //current screen color
    @color
    M=0

    //starting position of screen pixels
    @SCREEN
    D=A
    @currpos
    M=D

    //if keyPressed! don't change screen color to black
    @KBD
    D=M
    @PAINTLOOP
    D;JEQ

    //change screen color to black
    @color
    M=-1

        (PAINTLOOP)
            @color
            D=M

            //set color of 16 pixels
            @currpos
            A=M
            M=D

            //go to next 16 pixels for the next iteration
            @currpos
            M=M + 1

            @SCREEN
            D=A

            //D = last index of screen
            @screensize
            D=D + M

            //if RAM[currpos] == 0 screen ended
            @currpos
            D=D - M

            //if screen ended get out of the loop
            @OUTERLOOP
            D;JEQ

            //keep painting
            @PAINTLOOP
            0;JMP
    

    @OUTERLOOP
    0;JMP
