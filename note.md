# Ressort le dernier terme, reserve r0 et r1
1,0,1
LOAD(i0,r0)
ADD(I@r0,0,r1)
**Ici on peut écrire**
JE(r0,0,**fin**)
ADD(r0,-1,r0)
JUMP(-3)

# Empile 1 et le char de fin de pile est 3, reserve r0
3
LOAD(i1,r0)
JE(r0,0,3)
MULT(r0,10,r0)
ADD(r0,1,r0)
JUMP(2)
LOAD(10,r0)

# Depile 1, reserve r0
311
LOAD(i1,r0)
JE(r0,0,3)
DIV(r0,10,r0)
JUMP(2)
LOAD(10,r0)
