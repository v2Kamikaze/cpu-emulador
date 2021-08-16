# Python 3.9.5
# Carlos Victor Torres Rufino - 473741

from logo import *
import memory as mem
import clock as clk
import amdog as cpu
import disk
import sys

Colors.show_logo()

disk.read(sys.argv[1])

mem.write_word(1, 0) # só mudar os valores.

clk.start([cpu])

print(f"Resultado do programa {sys.argv[1]}: ", mem.read_word(1))

# Mudanças no microcódigo:
#   Com a inserção da multiplicação, divisão e resto da divisão, a ALU agora possui um bit extra no decodificador, 
#   assim 100, 101 e 110, são os códigos do decodificador para mult, div e mod.
#   Microinstruções de 33 bits: 
#       9 bits de endereçamento, 
#       3 bits de jump, 
#       2 bits do deslocador e 7 bits operações da alu, 
#       6 bits para escrita de registradores,
#       3 de acesso para memória,
#       3 de lida de registradores.
# 
# Circuitos extras na ALU:
#   A ALU agora possui 3bits no decodificador, assim podemos selecionar a multiplicação, divisão e resto da divisão.
#
#   Circuito de divisão:
#       Divide o valor vindo do barramento B pelo valor vindo do barramento A e guarda em um registrador (X ou Y).
#       É usado assim, pois, queremos dividir um valor que está em um registrador (X ou Y), por um valor que foi jogado no registrador H.
#
#   Circuito de multiplicação:
#       Multiplica o valor vindo do barramento A pelo valor vindo do barramento B e guarda em um registrador (X ou Y).
#       É usado assim, pois, queremos multiplicar um valor que está em um registrador (X ou Y), por um valor que foi jogado no registrador H.
#
#   Circuito de módulo, que nada mais é do que um circuito de divisão que só retorna o resto da divisão.
#       Divide o valor vindo do barramento B pelo valor vindo do barramento A e guarda o resto da divisão em um registrador (X ou Y).
#       É usado assim, pois, queremos dividir um valor que está em um registrador (X ou Y), por um valor que foi jogado no registrador H.
#       Como o circuito é o mesmo de divisão, ignora-se os bits da divisão e só se usa os bits de resto.
#   Obs.: A explicação do escalonamento dos circuitos está explicada no arquivo circuitos.txt.
# 
# Registradores: 
#   Uso do resgistrador Y.
#
# Assembler:
#   Só rodar python assembler.py [file.asm] [file.bin]
#   Possui 3 blocos definidos:
#       init: O bloco da primeira word na memória, onde é definido em qual linha começa o programa.
#            Ex: init:
#                    goto main
#                    ww 0
#                !init
#       vars: O bloco onde são definidas as variáveis (words) que serão usados no programa.
#             Ex: vars:      
#                     VAR_1 ww 256  
#                 !vars  
#       prog: O bloco onde está o programa em si, tudo dentro desse bloco é a lógica do programa.
#             Ex: prog:  
#                     main add x, VAR_1
#                          dec x                
#                          mov x, VAR_1
#                          halt 
#                 !prog  
#   
#   Os registradores X e Y podem ser acessados e manipulados usando os seguintes comandos:
#       reg: resgistrador
#       end: endereço       
#
#       add   [reg], [valor]  = reg <- reg + valor
#       sub   [reg], [valor]  = reg <- reg - valor 
#       mult  [reg], [valor]  = reg <- reg * valor
#       div   [reg], [valor]  = reg <- reg // valor
#       mod   [reg], [valor]  = reg <- reg % valor
#       mov   [reg], [end]    = end <- reg
#       dec   [reg]           = reg <- reg - 1
#       inc   [reg]           = reg <- reg + 1
#       reset [reg]           = reg <- 0
#       jamz  [reg], [linha]  = pule se reg == 0 para essa linha.