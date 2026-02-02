START   100
A       DC      01          ; sample program

        LOAD    A
        LOAD    C           ; c variable

        ORIGIN  500
        ADD     ='5'
        AD      D

        ORIGIN  A+4
        MULT    ='10'
        ADD     L

        ORIGIN  900
        LTORG
        ='5'
        ='10'

L       ADD     ='7'
        MOVER   ='2'

        ORIGIN  A+10
        STORE   ='4'
        LTORG

        ADD     B
        LOAD    ='3'
        LOAD    ='5'

B       DS      4
C       EQU     B
A       DS      7

        END
