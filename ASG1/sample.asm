        START   100

A       DC      01              ; sample program

        LOAD    A
        LOAD    C               ; c variable
        ADD     ='5'
        ADD     D

        ORIGIN  A+4
        MULT    ='10'
        ADD     L

        LTORG
        ='5'
        ='10'

L       ADD     ='5'
        ADD     B

B       DS      1
C       EQU     B
A       DS      1

        END
