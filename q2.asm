init:
     goto main
     wb 0 
!init    

vars:
    FIB     ww 0
    PREV    ww 0
    NEXT    ww 1
    SUM     ww 1
    COUNT   ww 0
!vars

prog:
    main  goto loop
    loop  add x, PREV
          add x, NEXT
          mov x, SUM
         
          add y, FIB
          jamz y, end_0
          reset y

          add y, NEXT
          mov y, PREV
        
          sub y, PREV
          add y, SUM
          mov y, NEXT

          sub x, SUM
          sub y, NEXT

          add x, FIB
          dec x
          mov x, FIB
          jamz x, end
          reset x

          goto loop

    end   add x, PREV
          mov x, FIB
          halt

    end_0 add y, PREV
          mov y, FIB
          halt




    end  halt

!prog
