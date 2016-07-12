# HummusLite

The Goal is to build a functional CPU in minecraft that interprets an assembly code that I wrote called HummusLite. I chose to do this in minecraft cause why not. The name Hummus stuck because me and my friends watched [this video.](https://www.youtube.com/watch?v=_QdPW8JrYzQ) Since then, the name kinda stuck.

#### TODO List
- [ ] Add pictures to the README
- [ ] Implement a system clock
- [ ] Figure out how to implement user input

# System Registers
ID | Name | Description
---|------|----------------
PC | Program Counter | Location of Current Instruction
B1 | Register B1 | One of the two main registers
B2 | Register B2 | One of the two main registers
RS | Result Register | Stores the Current Result

# Instruction Set

_[4-bit OPCODE] [4-bit Argument]_

OPCODE | ARGS | Instruction | Psuedo-Code | Description
-------|------|-------------|-------------|------------
0000 | ---- | HALT | end() | Ends the Program.
0001 | xxxx | SHFF | PC = PC + 0b0000_xxxx | Moves the Program Counter Forward.
0010 | xxxx | SHFB | PC = PC - 0b0000_xxxx | Moves the Program Counter Backward.
0011 | zxxx | BNR |  if(RS): PC = PC + 0bzzzz_zxxx | If result is not zero, add a two's compliment number to the Program Counter, else do nothing.
0100 | yyyy | INP | B(2/1) = userInput() | If the ARGS are non-zero, get user input and store it in register B2, else store it in register B1.
0101 | yyyy | STR | B(2/1) = RS | If the ARGS are non-zero, store the value of register RS into B2, else store it in B1.
0110 | mmmm | LDB1 | B1 = Memory[0bmmmm] | Take byte from location 0bmmmm in memory and store it into register B1.
0111 | mmmm | LDB2 | B2 = Memory[0bmmmm] | Take byte from location 0bmmmm in memory and store it into register B2.
1000 | xxxx | ADDB1 | RS = B1 + 0bxxxx | Add 0bxxxx to the value in B1 and store it in RS.
1001 | xxxx | ADDB2 | RS = B2 + 0bxxxx | Add 0bxxxx to the value in B2 and store it in RS.
1010 | cccc | BOOL | RS = Bool(0bcccc) | The behaviour of Bool is described below.
1011 | --cc | ADD | RS = Add(0b00cc) | The behaviour of Add is described below.
1100 | xxxx | SUBB1 | RS = B1 - 0bxxxx | Subtract 0bxxxx from the value in register B1 and store it in RS.
1101 | xxxx | SUBB2 | RS = B2 - 0bxxxx | Subtract 0bxxxx from the value in register B2 and store it in RS.
1110 | mmmm | STM | Memory[0bmmmm] = RS | Store result into location 0bmmmm in memory.
1111 | ---- | MEMC | memoryClear() | Clear the Main Memory.

#### Behaviour of BOOL
The instruction BOOL performs a boolean or a logical operation based on the current value of ARGS. Hence it can do 16 different boolean operations. Here is the list.

ARGS | Psuedo-Code | Description
----------|-------------|------------
0000 | RS = B1 & B2 | Bitwise AND
0001 | RS = B1 && B2 | Logical AND
0010 | RS = B1 \| B2 | Bitwise OR
0011 | RS = B1 \|\| B2 | Logical OR
0100 | RS = B1 ^ B2 | Bitwise XOR
0101 | RS = B1 ~^ B2 | Bitwise XNOR
0110 | RS = B1 << 1 | Left Shift on B1
0111 | RS = B2 << 1 | Left Shift on B2
1000 | RS = ~(B1 & B2) | Bitwise NAND
1001 | RS = !(B1 && B2) | Logical NAND
1010 | RS = ~(B1 \| B2) | Bitwise NOR
1011 | RS = !(B1 \|\| B2) | Logical NOR
1100 | RS = ~B1 | Bitwise NOT on B1
1101 | RS = ~B2 | Bitwise NOT on B2
1110 | RS = B1 >> 1 | Right Shift on B1
1111 | RS = B2 >> 1 | Right Shift on B2

#### Behaviour of ADD
The instruction ADD simply adds register B1 and B2 in four different ways. Based on the ARGS value, it decides whether it should negate a register or two. Here is the list.

ARGS | Psuedo-Code | Description
-----|-------------|------------
00 | RS = B1 + B2 | Add B1 and B2
01 | RS = B1 + (-B2) | Add B1 and -B2
10 | RS = (-B1) + B2 | Add -B1 and B2
11 | RS = (-B1) + (-B2) | Add -B1 and -B2
