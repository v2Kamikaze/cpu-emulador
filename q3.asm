init:
     goto main
     wb 0 
!init    

vars:
    PRIME    ww 0
    CUR_NUM  ww 2
    COUNT    ww 2
    LAST_DIV ww 0
    MOD      ww 0
    TWO      ww 2
    THREE    ww 3

!vars

prog:

    main add x, PRIME
         jamz x, end_0
         dec x
         jamz x, end
         inc x
         sub x, TWO
         jamz x, end
         add x, TWO

    loop mod x, CUR_NUM
         mov x, MOD
         jamz x, incr

    back sub x, MOD
         add x, CUR_NUM
         inc x
         mov x, CUR_NUM
         reset x
         
         add x, PRIME
         sub x, CUR_NUM
         jamz x, end
         reset x

         add x, PRIME

         goto loop

    incr add y, COUNT
         inc y
         mov y, COUNT
         reset y
         
         add y, COUNT
         sub y, THREE
         jamz y, end
         reset y

         goto back

    end  add y, THREE
         sub y, COUNT
         mov y, PRIME
         halt

    end_0 mov x, PRIME
          halt
!prog
