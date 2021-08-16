from array import array
from div import divider_32bits
from mult import multiplier_32bits
import memory

MIR: int = 0
MPC: int = 0

MAR: int = 0
MDR: int = 0

PC: int = 0
MBR: int = 0

X: int = 0
Y: int = 0
H: int = 0

N: int = 0
Z: int = 1

BUS_A: int = 0
BUS_B: int = 0
BUS_C: int = 0

firmware = array('Q', [0]) * 512

# MAIN
firmware[0] =   0b000000000100000110101001000001001
# PC <- PC + 1; MBR <- read_byte(PC); GOTO MBR;

#X = X + mem[address]
firmware[2] =   0b000000011000000110101001000001001
# PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
firmware[3] =   0b000000100000000010100100000010010
# MAR <- MBR; read_word; GOTO 4
firmware[4] =   0b000000101000000010100000001000000
# H <- MDR; GOTO 5
firmware[5] =   0b000000000000000111100000100000011
# X <- X + H; GOTO MAIN;

#mem[address] = X
firmware[6] =   0b000000111000000110101001000001001
# PC <- PC + 1; fetch; GOTO 7
firmware[7] =   0b000001000000000010100100000000010
# MAR <- MBR; GOTO 8
firmware[8] =   0b000000000000000010100010000100011
# MDR <- X; write; GOTO MAIN

# goto address
firmware[9] =   0b000001010000000110101001000001001
# PC <- PC + 1; fetch; GOTO 10
firmware[10] =  0b000000000100000010100001000001010
# PC <- MBR; fetch; GOTO MBR;

# if X = 0 goto address
firmware[11] =  0b000001100001000010100000100000011
# X <- X; IF ALU = 0 GOTO 268 (100001100) ELSE GOTO 12 (000001100);
firmware[12] =  0b000000000000000110101001000000001
# PC <- PC + 1; GOTO MAIN;
firmware[268] = 0b100001101000000110101001000001001
# PC <- PC + 1; fetch; GOTO 269
firmware[269] = 0b000000000100000010100001000001010
# PC <- MBR; fetch; GOTO MBR;

#X = X - mem[address]
firmware[13] =  0b000001110000000110101001000001001
#PC <- PC + 1; fetch;
firmware[14] =  0b000001111000000010100100000010010
#MAR <- MBR; read;
firmware[15] =  0b000010000000000010100000001000000
#H <- MDR;
firmware[16] =  0b000000000000000111111000100000011
# X <- X - H; GOTO MAIN;

#Y = Y + mem[address]
firmware[17] =  0b000010010000000110101001000001001
# PC <- PC + 1; MBR <- read_byte(PC); GOTO 18
firmware[18] =  0b000010011000000010100100000010010
# MAR <- MBR; read_word; GOTO 19
firmware[19] =  0b000010100000000010100000001000000
# H <- MDR; GOTO 20
firmware[20] =  0b000000000000000111100000010000100
# Y <- Y + H; GOTO MAIN;

#mem[address] = Y
firmware[21] =  0b000010110000000110101001000001001
# PC <- PC + 1; fetch; GOTO 22
firmware[22] =  0b000010111000000010100100000000010
# MAR <- MBR; GOTO 23
firmware[23] =  0b000000000000000010100010000100100
# MDR <- Y; write; GOTO MAIN

#Y = Y - mem[address]
firmware[24] =  0b000011001000000110101001000001001
# PC <- PC + 1; fetch; GOTO 25
firmware[25] =  0b000011010000000010100100000010010
# MAR <- MBR; read; GOTO 26
firmware[26] =  0b000011011000000010100000001000000
# H <- MDR; GOTO 27
firmware[27] =  0b000000000000000111111000010000100
# Y <- Y - H; GOTO MAIN;

# if Y = 0 goto address
firmware[28] =  0b000011101001000010100000010000100
# Y <- Y; IF ALU = 0 GOTO 285 (100011101) ELSE GOTO 29 (000011101);
firmware[29] =  0b000000000000000110101001000000001
# PC <- PC + 1; GOTO MAIN;
firmware[285] = 0b100011110000000110101001000001001
# PC <- PC + 1; fetch; GOTO 286
firmware[286] = 0b000000000100000010100001000001010
# PC <- MBR; fetch; GOTO MBR;

#X = X * mem[address]
firmware[30] =  0b000011111000000110101001000001001
# PC <- PC + 1; fetch; GOTO 31
firmware[31] =  0b000100000000000010100100000010010
# MAR <- MBR; read_word; GOTO 32
firmware[32] =  0b000100001000000010100000001000000
# H <- MDR; GOTO 33
firmware[33] =  0b000000000000001001100000100000011
# X <- X * H; GOTO MAIN;

#Y = Y * mem[address]
firmware[34] =  0b000100011000000110101001000001001
# PC <- PC + 1; fetch; GOTO 35
firmware[35] =  0b000100100000000010100100000010010
# MAR <- MBR; read_word; GOTO 36
firmware[36] =  0b000100101000000010100000001000000
# H <- MDR; GOTO 37
firmware[37] =  0b000000000000001001100000010000100
# Y <- Y * H; GOTO MAIN;

#X = X / mem[address]
firmware[38] =  0b000100111000000110101001000001001
# PC <- PC + 1; fetch; GOTO 39
firmware[39] =  0b000101000000000010100100000010010
# MAR <- MBR; read_word; GOTO 40
firmware[40] =  0b000101001000000010100000001000000
# H <- MDR; GOTO 41
firmware[41] =  0b000000000000001011100000100000011
# X <- X / H; GOTO MAIN;

#Y = Y / mem[address]
firmware[42] =  0b000101011000000110101001000001001
# PC <- PC + 1; fetch; GOTO 43
firmware[43] =  0b000101100000000010100100000010010
# MAR <- MBR; read_word; GOTO 44
firmware[44] =  0b000101101000000010100000001000000
# H <- MDR; GOTO 45
firmware[45] =  0b000000000000001011100000010000100
# Y <- Y / H; GOTO MAIN;

#X = X % mem[address]
firmware[46] =  0b000101111000000110101001000001001
# PC <- PC + 1; fetch; GOTO 47
firmware[47] =  0b000110000000000010100100000010010
# MAR <- MBR; read_word; GOTO 48
firmware[48] =  0b000110001000000010100000001000000
# H <- MDR; GOTO 49
firmware[49] =  0b000000000000001101100000100000011
# X <- X % H; GOTO MAIN;

#Y = Y % mem[address]
firmware[50] =  0b000110011000000110101001000001001
# PC <- PC + 1; fetch; GOTO 51
firmware[51] =  0b000110100000000010100100000010010
# MAR <- MBR; read_word; GOTO 52
firmware[52] =  0b000110101000000010100000001000000
# H <- MDR; GOTO 53
firmware[53] =  0b000000000000001101100000010000100 
# Y <- Y % H; GOTO MAIN;

# X = X - 1
firmware[54] =  0b000000000000000110110000100000011
# X <- X - 1; GOTO MAIN;

# Y = Y - 1
firmware[55] =  0b000000000000000110110000010000100
# Y <- Y + 1; GOTO MAIN;

# X = X + 1
firmware[56] =  0b000000000000000110101000100000011
# X <- X + 1; GOTO MAIN;

# Y = Y + 1
firmware[57] =  0b000000000000000110101000010000100
# Y <- Y + 1; GOTO MAIN;

# X = 0
firmware[58] =  0b000000000000000010000000100000011
# X <- X - 1; GOTO MAIN;

# Y = 0
firmware[59] =  0b000000000000000010000000010000100
# Y <- 0; GOTO MAIN;



def read_regs(reg_num: int) -> None:
    global BUS_A, BUS_B, H, MDR, PC, MBR, X, Y

    BUS_A = H

    if reg_num == 0:
        BUS_B = MDR
    elif reg_num == 1:
        BUS_B = PC
    elif reg_num == 2:
        BUS_B = MBR
    elif reg_num == 3:
        BUS_B = X
    elif reg_num == 4:
        BUS_B = Y
    else:
        BUS_B = 0


def write_regs(reg_bits: int) -> None:
    global MAR, MDR, PC, X, Y, H, BUS_C

    if reg_bits & 0b100000:
        MAR = BUS_C
    if reg_bits & 0b010000:
        MDR = BUS_C
    if reg_bits & 0b001000:
        PC = BUS_C
    if reg_bits & 0b000100:
        X = BUS_C
    if reg_bits & 0b000010:
        Y = BUS_C
    if reg_bits & 0b000001:
        H = BUS_C


def alu(control_bits: int) -> None:
    global N, Z, BUS_A, BUS_B, BUS_C

    a = BUS_A
    b = BUS_B
    o = 0

    shift_bits = (0b110000000 & control_bits) >> 7
    control_bits = 0b001111111 & control_bits

    if control_bits   == 0b0011000:
        o = a
    elif control_bits == 0b0010100:
        o = b
    elif control_bits == 0b0011010:
        o = ~a
    elif control_bits == 0b0101100:
        o = ~b
    elif control_bits == 0b0111100:
        o = a+b
    elif control_bits == 0b0111101:
        o = a+b+1
    elif control_bits == 0b0111001:
        o = a+1
    elif control_bits == 0b0110101:
        o = b+1
    elif control_bits == 0b0111111:
        o = b-a
    elif control_bits == 0b0110110:
        o = b-1
    elif control_bits == 0b0111011:
        o = -a
    elif control_bits == 0b0001100:
        o = a & b
    elif control_bits == 0b0011100:
        o = a | b
    elif control_bits == 0b0010000:
        o = 0
    elif control_bits == 0b0110001:
        o = 1
    elif control_bits == 0b0110010:
        o = -1
    elif control_bits == 0b1001100:
        o = multiplier_32bits(a, b)
    elif control_bits == 0b1011100:
        o, _ = divider_32bits(b, a)  # recebe o resultado da divisão
    elif control_bits == 0b1101100:
        _, o = divider_32bits(b, a)  # recebe o resto da divisão

    # código mult -> 1001100 -> 100 mult 1100 ativa a e b
    # código div  -> 1011100 -> 101 div  1100 ativa a e b
    # código mod  -> 1101100 -> 110 mod  1100 ativa a e b

    if o == 0:
        N = 0
        Z = 1
    else:
        N = 1
        Z = 0

    if shift_bits == 0b01:
        o = o << 1
    elif shift_bits == 0b10:
        o = o >> 1
    elif shift_bits == 0b11:
        o = o << 8

    BUS_C = o


def next_instruction(next: int, jam: int) -> None:
    global MPC, MBR, Z, N

    if jam == 0:
        MPC = next
        return

    if jam & 0b001:
        next = next | (Z << 8)

    if jam & 0b010:
        next = next | (N << 8)

    if jam & 0b100:
        next = next | MBR

    MPC = next


def memory_io(mem_bits: int) -> None:
    global PC, MBR, MDR, MAR

    if mem_bits & 0b001:
        MBR = memory.read_byte(PC)

    if mem_bits & 0b010:
        MDR = memory.read_word(MAR)

    if mem_bits & 0b100:
        memory.write_word(MAR, MDR)


def step() -> bool:
    global MIR, MPC

    MIR = firmware[MPC]

    if MIR == 0:
        return False

    read_regs(MIR & 0b000000000000000000000000000000111)
    alu((MIR & 0b000000000000111111111000000000000) >> 12)
    write_regs((MIR & 0b000000000000000000000111111000000) >> 6)
    memory_io((MIR & 0b000000000000000000000000000111000) >> 3)
    next_instruction(
        (MIR & 0b111111111000000000000000000000000) >> 24,
        (MIR & 0b000000000111000000000000000000000) >> 21
    )

    return True