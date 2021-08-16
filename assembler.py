from io import TextIOWrapper
import sys
from pprint import pprint
from typing import Dict, List, Tuple

# comando: python assembler.py [arq1.asm] [arq1.bin] 

# Caso queira ver o valor em bytes de cada linha de cada bloco do programa, assim como sua saída e a númeração das linhas, mude DEBUG para True.
DEBUG = True

KEY_WORDS = ['wb', 'ww']

CODES = {
    'goto':     0x09,
    'add x,':   0x02,
    'mov x,':   0x06,
    'sub x,':   0x0D,
    'jamz x,':  0x0B,
    'halt':     0xFF,
    'add y,':   0x11,
    'mov y,':   0x15,
    'sub y,':   0x18,
    'jamz y,':  0x1C,
    'mult x,':  0x1E,
    'mult y,':  0x22,
    'div x,':   0x26,
    'div y,':   0x2A,
    'mod x,':   0x2E,
    'mod y,':   0x32,
    'dec x':    0x36,
    'dec y':    0x37,
    'inc x':    0x38,
    'inc y':    0x39,
    'reset x':  0x3A,
    'reset y':  0x3B,
}


prog_blocs: Dict[str, List[List[str]]] 
vars_codes: Dict[str, int] = {}
init_vars_codes: Dict[str, int] = {}
prog_vars_codes: Dict[str, int] = {}
prog_lines_with_bytes: Dict[int, Tuple] = {}


def get_blocs(file: TextIOWrapper) -> Dict[str, List[List[str]]]:
    """
        Retorna um dicionário em que cada chave representa um bloco de código
        contendo as linhas desse bloco.  
    """

    file_lines = []
    prog_blocs = {
        'init': [],
        'vars': [],
        'prog': [],
    }
    for line in file.readlines():
        if not line.isspace() or not line:
            file_lines.append(line.replace('\n', ''))

    for i in range(len(file_lines)):
        file_lines[i] = [word for word in file_lines[i].split(' ') if word]

    index_init, end_index_init = file_lines.index(
        ['init:']), file_lines.index(['!init'])
    index_vars, end_index_vars = file_lines.index(
        ['vars:']), file_lines.index(['!vars'])
    index_prog, end_index_prog = file_lines.index(
        ['prog:']), file_lines.index(['!prog'])

    prog_blocs['init'] = file_lines[index_init + 1:end_index_init]
    prog_blocs['init'].insert(0, ['0'])
    prog_blocs['vars'] = file_lines[index_vars + 1:end_index_vars]
    prog_blocs['prog'] = file_lines[index_prog + 1:end_index_prog]

    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            if 'add' in line:
                index_add = line.index('add')
                line[index_add] = line[index_add] + ' ' + line[index_add+1]
                line.pop(index_add+1)
            if 'sub' in line:
                index_sub = line.index('sub')
                line[index_sub] = line[index_sub] + ' ' + line[index_sub+1]
                line.pop(index_sub+1)
            if 'jamz' in line:
                index_jamz = line.index('jamz')
                line[index_jamz] = line[index_jamz] + ' ' + line[index_jamz+1]
                line.pop(index_jamz+1)
            if 'mov' in line:
                index_mov = line.index('mov')
                line[index_mov] = line[index_mov] + ' ' + line[index_mov+1]
                line.pop(index_mov+1)
            if 'mult' in line:
                index_mult = line.index('mult')
                line[index_mult] = line[index_mult] + ' ' + line[index_mult+1]
                line.pop(index_mult+1)
            if 'div' in line:
                index_div = line.index('div')
                line[index_div] = line[index_div] + ' ' + line[index_div+1]
                line.pop(index_div+1)
            if 'mod' in line:
                index_mod = line.index('mod')
                line[index_mod] = line[index_mod] + ' ' + line[index_mod+1]
                line.pop(index_mod+1)
            if 'dec' in line:
                index_dec = line.index('dec')
                line[index_dec] = line[index_dec] + ' ' + line[index_dec+1]
                line.pop(index_dec+1)
            if 'inc' in line:
                index_inc = line.index('inc')
                line[index_inc] = line[index_inc] + ' ' + line[index_inc+1]
                line.pop(index_inc+1)
            if 'reset' in line:
                index_reset = line.index('reset')
                line[index_reset] = line[index_reset] + ' ' + line[index_reset+1]
                line.pop(index_reset+1)
            

    return prog_blocs

def get_var_names() -> None:
    """
        Filtra os nomes das variáveis em cada bloco do programa e 
        guarda como uma chave de um dicionário com seus valores em bytes zerados.
        Ex:
            init_vars_codes -> {
                "A": 0,
                "B": 0,
                "C": 0,
            }
    """
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            for word in line:
                if not word.isnumeric() and word not in KEY_WORDS and word not in CODES and 'x' not in word:
                    if bloc == 'vars':
                        vars_codes[word] = 0
                    elif bloc == 'init' and word not in vars_codes.keys():
                        init_vars_codes[word] = 0
                    elif bloc == 'prog' and word not in vars_codes.keys() and word not in init_vars_codes.keys():
                        prog_vars_codes[word] = 0


def calculate_bytes() -> None:
    """
        Calcula os bytes de cada linha, atribuindo um intervalo de bytes para cada linha.
        Cada linha é uma chave do dicionário, onde o primeiro valor da tupla são as palavras
        da sua respectiva linha e o segundo valor da tupla é o intevalo em bytes dessa linha.
        Ex:
            prog_lines_with_bytes -> {
                1: (['0'], (0, 0)),
                2: (['goto', 'main'], (1, 2)),
                3: (['wb', '0'], (3, 3)),
                4: (['A', 'ww', '0'], (4, 7)),
                5: (['B', 'ww', '250'], (8, 11)),
            }
    """

    byte_counter = 0
    line_number = 1

    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            last_byte_counter = byte_counter
            if 'goto' in line:
                byte_counter += 2
            if 'add x,' in line:
                byte_counter += 2
            if 'sub x,' in line:
                byte_counter += 2
            if 'mov x,' in line:
                byte_counter += 2
            if 'jamz x,' in line:
                byte_counter += 2
            if 'mult x,' in line:
                byte_counter += 2
            if 'div x,' in line:
                byte_counter += 2
            if 'mod x,' in line:
                byte_counter += 2
            if 'add y,' in line:
                byte_counter += 2
            if 'sub y,' in line:
                byte_counter += 2
            if 'mov y,' in line:
                byte_counter += 2
            if 'jamz y,' in line:
                byte_counter += 2
            if 'mult y,' in line:
                byte_counter += 2
            if 'div y,' in line:
                byte_counter += 2
            if 'mod y,' in line:
                byte_counter += 2
            if 'halt' in line:
                byte_counter += 1
            if 'ww' in line:
                byte_counter += 4
            if 'wb' in line:
                byte_counter += 1
            if 'dec x' in line:
                byte_counter += 1
            if 'dec y' in line:
                byte_counter += 1
            if 'inc x' in line:
                byte_counter += 1
            if 'inc y' in line:
                byte_counter += 1
            if 'reset x' in line:
                byte_counter += 1
            if 'reset y' in line:
                byte_counter += 1

            if byte_counter == 0:
                prog_lines_with_bytes[line_number] = (
                    line, (last_byte_counter, byte_counter))
            else:
                prog_lines_with_bytes[line_number] = (
                    line, (last_byte_counter + 1, byte_counter))
            line_number += 1

def assign_bytes_to_init() -> None:
    """
        Coloca os bytes nas variáveis do bloco init.
        Ex: init_vars_codes -> {
            "main": 20,
        }
    """
    for var in init_vars_codes:
        var_count = 0
        for line in prog_lines_with_bytes:
            if var in prog_lines_with_bytes[line][0]:
                var_count += 1
            if var_count == 2 and var in prog_lines_with_bytes[line][0]:
                init_vars_codes[var] = prog_lines_with_bytes[line][1][0]


def assign_bytes_to_vars() -> None:
    """
        Coloca o número da word de cada variável do bloco vars.
        Ex: vars_codes -> {
            'A': 2, <- word 2
            'B': 3, <- word 3
            'C': 4, <- word 4
        }
    """
    word_counter = 1
    for line in prog_blocs['vars']:
        for var in vars_codes:
            if var in line:
                vars_codes[var] = word_counter
                word_counter += 1
                break


def assign_bytes_to_prog() -> None:
    """
        Coloca os bytes respectivos de cada variável do bloco prog.
        Ex: prog_vars_codes -> {
            'jmp': 30,
            'hlt': 22,
        }
    """
    for var in prog_vars_codes:
        var_count = 1
        for line in prog_lines_with_bytes:
            if var in prog_lines_with_bytes[line][0] and var_count == 1 and var == prog_lines_with_bytes[line][0][0]:
                byte_var = prog_lines_with_bytes[line][1][0]
                prog_vars_codes[var] = byte_var
                var_count += 1

def replace_keywords_and_mnemonics() -> None:
    """
        Substitui cada mnemônico pelo seu respectivo byte e remove as palavras-chaves, 
        deixando apenas seus valores.
    """
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            if 'goto' in line:
                line[line.index('goto')] = CODES['goto']
            if 'add x,' in line:
                line[line.index('add x,')] = CODES['add x,']
            if 'sub x,' in line:
                line[line.index('sub x,')] = CODES['sub x,']
            if 'mov x,' in line:
                line[line.index('mov x,')] = CODES['mov x,']
            if 'jamz x,' in line:
                line[line.index('jamz x,')] = CODES['jamz x,']
            if 'mult x,' in line:
                line[line.index('mult x,')] = CODES['mult x,']
            if 'div x,' in line:
                line[line.index('div x,')] = CODES['div x,']
            if 'mod x,' in line:
                line[line.index('mod x,')] = CODES['mod x,']
            if 'add y,' in line:
                line[line.index('add y,')] = CODES['add y,']
            if 'sub y,' in line:
                line[line.index('sub y,')] = CODES['sub y,']
            if 'mov y,' in line:
                line[line.index('mov y,')] = CODES['mov y,']
            if 'jamz y,' in line:
                line[line.index('jamz y,')] = CODES['jamz y,']
            if 'mult y,' in line:
                line[line.index('mult y,')] = CODES['mult y,']
            if 'div y,' in line:
                line[line.index('div y,')] = CODES['div y,']
            if 'mod y,' in line:
                line[line.index('mod y,')] = CODES['mod y,']
            if 'halt' in line:
                line[line.index('halt')] = CODES['halt']
            if 'wb' in line:
                line.pop(0)  # deletando o mnemônico wb
            if 'ww' in line:
                line.pop(0)  # deletando o nome da variável
                line.pop(0)  # deletando o mnemônico ww
                line[0] = int(line[0])
            if 'dec x' in line:
                line[line.index('dec x')] = CODES['dec x']
            if 'dec y' in line:
                line[line.index('dec y')] = CODES['dec y']
            if 'inc x' in line:
                line[line.index('inc x')] = CODES['inc x']
            if 'inc y' in line:
                line[line.index('inc y')] = CODES['inc y']
            if 'reset x' in line:
                line[line.index('reset x')] = CODES['reset x']
            if 'reset y' in line:
                line[line.index('reset y')] = CODES['reset y']


def replace_vars_of_vars_bloc_in_program() -> None:
    """
        Substitui cada ocorrência das variáveis do bloco vars no programa pelo seu número de word.
    """
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            for var in vars_codes:
                if var in line:
                    line[line.index(var)] = vars_codes[var]


def replace_vars_of_init_bloc_in_program() -> None:
    """
        Substitui a variável do bloco init pelo sua representação em byte..
    """
    for line in prog_blocs['init']:
        for var in init_vars_codes:
            if var in line:
                line[line.index(var)] = init_vars_codes[var]

def replace_vars_of_prog_bloc_in_program() -> None:
    """
        Substitui cada ocorrência das variáveis do bloco init no programa pelo seu byte.
    """
    for var in prog_vars_codes:
        for line in prog_blocs['prog']:
            if var in line and var != line[0]:
                line[line.index(var)] = prog_vars_codes[var]


def format_prog_blocs() -> List[int]:
    """
        Formata os bytes do programa e coloca em ordem em uma lista.
    """
    # convertendo todos os valores numéricos contidos em cada chave de prog_blocs em inteiros.
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            for i in range(len(line)):
                if str(line[i]).isnumeric():
                    line[i] = int(line[i])

    # removendo os elementos não numéricos que sobraram em prog_blocs.
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            for word in line:
                if not str(word).isnumeric():
                    line.pop(line.index(word))

    array_bytes: List[int] = []

    # colocando em array_bytes os valores de cada bloco em prog_blocs.
    # como as words tem um tamanho de até 32 bits, separa-se cada word em 4 bytes
    # e escreve-se sequencialmente em array_bytes.
    for bloc in prog_blocs:
        for line in prog_blocs[bloc]:
            for word in line:
                if bloc == 'vars':
                    array_bytes.append(word & 0xFF)
                    array_bytes.append((word & 0xFF00) >> 8)
                    array_bytes.append((word & 0xFF0000) >> 16)
                    array_bytes.append((word & 0xFF000000) >> 24)
                else:
                    array_bytes.append(word)
    return array_bytes


with open(sys.argv[1]) as file:
    prog_blocs = get_blocs(file)

    # filtrando os nomes das variáveis de cada bloco e salvando nas variáveis:
    # init_vars_codes, prog_vars_codes, prog_lines_with_bytes.
    get_var_names()
    # atribuindo o intervalo em bytes de cada linha e salvando em:
    # prog_lines_with_bytes.
    calculate_bytes()

    if DEBUG:
        print("Debug 1: ")
        pprint(prog_lines_with_bytes)

    # colocando os bytes nas variáveis do bloco de inicialização.
    assign_bytes_to_init()

    # colocando as words nas variáveis do bloco de variáveis.
    assign_bytes_to_vars()

    # colocando os bytes nas variáveis do bloco do programa.
    assign_bytes_to_prog()

    # substituindo os mnemônicos e keywords presentes em prog_blocs.
    replace_keywords_and_mnemonics()

    # como as variáveis do bloco de variáveis já estão com seus respectivos bytes,
    # substituindo os seus nomes pelos seus valores, agora podemos substituir cada
    # ocorrência dessa variável no programa pelo seu respectivo byte.
    replace_vars_of_vars_bloc_in_program()

    # agora é hora de substituir as variáveis do bloco init, que nada mais é do que substituir a variável após o goto pelo byte da
    # primeira ocorrência dela.
    replace_vars_of_init_bloc_in_program()

    # agora falta só substituir as variáveis definidades dentro do bloco do programa, por enquanto, somente sua primeira ocorrência.
    replace_vars_of_prog_bloc_in_program()

    # formatando prog_blocs e retornando uma lista com os bytes do programa. 
    array_bytes = format_prog_blocs()
    
    if DEBUG:
        print("Debug 2: ")
        pprint(prog_blocs)
        print("Debug 3: ")
        for byte in bytearray(array_bytes): print(hex(byte), end=" ")
        print("\nDebug 4: ")
        print("Bloco init -> ", init_vars_codes)
        print("Bloco vars -> ", vars_codes)
        print("Bloco prog -> ", prog_vars_codes)


    with open(sys.argv[2], 'wb') as out:
        out.write(bytearray(array_bytes))



