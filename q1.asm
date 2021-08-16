init:
     goto main
     wb 0 
!init    

vars:
     FAT       ww 0
     AUX_FAT   ww 0
     AUX_MLT   ww 0
!vars

prog:

    main add x, FAT
         mov x, AUX_FAT
         jamz x, end_0
         add y, AUX_FAT

    loop dec y
         jamz y, end
         mov y, AUX_MLT
         mult x, AUX_MLT
         mov x, AUX_FAT
         goto loop

    end mov x, FAT
        halt
    
    end_0 inc x
          mov x, FAT
          halt
          
!prog
