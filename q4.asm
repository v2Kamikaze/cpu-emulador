init:
     goto main
     wb 0 
!init    

vars:
    N       ww 0
    COUNT   ww 0
    TWO     ww 2
!vars

prog:
    main add x, N
         jamz x, end

    loop div x, TWO

         add y, COUNT
         inc y
         mov y, COUNT
         reset y

         dec x
         jamz x, end
         inc x

         goto loop

    end add y, COUNT
        mov y, N
        halt
!prog

skopaskaopskopaksopaksopakspoaksop