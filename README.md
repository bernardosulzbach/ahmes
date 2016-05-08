# Ahmes

![Build Status](https://travis-ci.org/mafagafogigante/ahmes.svg?branch=master)
[![codecov](https://codecov.io/gh/mafagafogigante/ahmes/branch/master/graph/badge.svg)](https://codecov.io/gh/mafagafogigante/ahmes)

Ahmes is a computer used in some computer architecture classes. There is an
executable file in the repository. It can be ran natively on Windows or using
Wine under Linux.

You will need Git LFS in order to get the executable from the command line.

Everything here is licensed under the BSD 2-Clause license, except for the
simulator itself.

The maintainer of this repository is working on a fully-compatible simulator
for Ahmes using Python. This is a step in the direction of making software
usable by everyone.

## Regarding the computer

The computer has 256 bytes of memory.

There are also two registers: the accumulator (AC) and the program counter (PC).

The computer also has five indicators:

    N - negative, set if the last operation produced a negative result
    Z - zero,     set if the last operation produced zero
    V - overflow, set if the last operation resulted in an overflow
    C - carry,    set if the last operation resulted in a carry-out
    B - borrow,   set if the last operation resulted in a borrow

## Notation

    MSB - most  significant bit
    LSB - least significant bit

## Instruction List

### No-ops

    NOP - no operation

### Memory Manipulation Instructions

    STA ADDRESS - stores AC on ADDRESS
    LDA ADDRESS - loads ADDRESS on AC

### Logic Instructions

    AND ADDRESS - bitwise AND with the byte at ADDRESS
    OR  ADDRESS - bitwise OR  with the byte at ADDRESS
    NOT         - bitwise NOT

### Mathematical Instructions

    ADD ADDRESS - two's complement addition    with the byte at ADDRESS
    SUB ADDRESS - two's complement subtraction with the byte at ADDRESS

### Bitwise Instructions

    SHR - shifts  the AC one bit to the right
    SHL - shifts  the AC one bit to the left
    ROR - rotates the AC one bit to the right (the LSB becomes the MSB)
    ROL - rotates the AC one bit to the left  (the MSB becomes the LSB)

### Jump Instructions

A jump is a modification of the program counter. Jumping to X and setting the
PC to X are practically the same thing here.

#### Unconditional Jump

    JMP ADDRESS - jumps to ADDRESS

#### Conditional Jumps

    JN  ADDRESS - if N,     jumps to ADDRESS
    JP  ADDRESS - if not N, jumps to ADDRESS
    JV  ADDRESS - if V,     jumps to ADDRESS
    JNV ADDRESS - if not V, jumps to ADDRESS
    JZ  ADDRESS - if Z,     jumps to ADDRESS
    JNZ ADDRESS - if not Z, jumps to ADDRESS
    JC  ADDRESS - if C,     jumps to ADDRESS
    JNC ADDRESS - if not C, jumps to ADDRESS
    JB  ADDRESS - if B,     jumps to ADDRESS
    JNB ADDRESS - if not B, jumps to ADDRESS

### Halting Instructions

    HLT - halts the program execution

## Instruction Table

When the program counter points to a byte with a code, the instruction to be
executed is selected according to the following table.

Each instruction is indicated by a byte value in the range [Code, Maximum Code].
However, if you run the program with the `--pedantic` flag only Code is
considered a valid identification code for the instruction and all other codes
are mapped into NOPs.

|Code|Maximum Code|Mnemonic|
|----|------------|--------|
|0   |15          |NOP     |
|16  |31          |STA     |
|32  |47          |LDA     |
|48  |63          |ADD     |
|64  |79          |OR      |
|80  |95          |AND     |
|96  |111         |NOT     |
|112 |127         |SUB     |
|128 |143         |JMP     |
|144 |147         |JN      |
|148 |151         |JP      |
|152 |155         |JV      |
|156 |159         |JNV     |
|160 |163         |JZ      |
|164 |175         |JNZ     |
|176 |179         |JC      |
|180 |183         |JNC     |
|184 |187         |JB      |
|188 |223         |JNB     |
|224 |224         |SHR     |
|225 |225         |SHL     |
|226 |226         |ROR     |
|227 |239         |ROL     |
|240 |255         |HLT     |

## Flags

### `--pedantic`

Only the first code value is mapped to the instruction, all other instruction
codes that would map to the instruction will then map to NOP.

## Regarding the memory files

`ones.mem` - A memory file whose bytes are all set to the value 1.
