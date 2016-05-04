# Ahmes

![Build Status](https://travis-ci.org/mafagafogigante/ahmes.svg?branch=master)

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

**N** - negative, set if the last operation produced a negative result
**Z** - zero, set if the last operation produced zero
**V** - overflow, set if the last operation resulted in an overflow
**C** - carry, set if the last operation resulted in a carry-out
**B** - borrow, set if the last operation resulted in a borrow

## Instruction List

### No-ops

    NOP - no operation

### Memory Manipulation Instructions

    STA ADDRESS - stores AC on ADDRESS
    LDA ADDRESS - loads ADDRESS on AC

### Logic Instructions

    AND
    OR
    NOT

### Mathematical Instructions

    ADD
    SUB

### Bitwise Instructions

    SHR - shifts the AC one bit to the right
    SHL - shifts the AC one bit to the left
    ROR - rotates the AC one bit to the right (the LSB becomes the MSB)
    ROL - rotates the AC one bit to the left (the MSB becomes the LSB)

### Jump Instructions

A jump is a modification of the program counter. Jumping to X and setting the
PC to X are practically the same thing here.

#### Unconditional Jump

    JMP ADDRESS - jumps to ADDRESS

#### Conditional Jumps

    JN  ADDRESS - if N, jumps to ADDRESS
    JP  ADDRESS - if not N, jumps to ADDRESS
    JV  ADDRESS - if V, jumps to ADDRESS
    JNV ADDRESS - if not V, jumps to ADDRESS
    JZ  ADDRESS - if Z, jumps to ADDRESS
    JNZ ADDRESS - if not Z, jumps to ADDRESS
    JC  ADDRESS - if C, jumps to ADDRESS
    JNC ADDRESS - if not C, jumps to ADDRESS
    JB  ADDRESS - if B, jumps to ADDRESS
    JNB ADDRESS - if not B, jumps to ADDRESS

### Halting Instructions

    HLT - halts the program execution

### Notation

    MSB - most significant bit
    LSB - least significant bit

## Regarding the memory files

`ones.mem` - A memory file whose bytes are all set to the value 1.
