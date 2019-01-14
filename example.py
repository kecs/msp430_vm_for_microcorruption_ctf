import sys
from numpy import uint16 as i16

from vm import VM
from utils import memset
from instructions import *


def readstr(addr):
    ret = ''
    while mem[addr] != 0:
        ret += mem[addr]
        addr += 1

    return ret


def strcmp(vm, dbg=True):
    "Sets z if strings at r15 and r14 are equal"
    
    vm.runasm('''
    jmp	     4
    tst.b	     r13
    jz           11
    inc	     r15
    mov.b     @r15, r13
    mov.b     @r14, r12
    inc	     r14
    cmp.b     r12, r13
    jeq	     -7
    mov.b     r13, r15
    mov.b     -0x1(r14), r14
    sub	     r14, r15
    ret
    clr          r15
    ret''',
    dbg=dbg)
    
        
def _hash(vm, dbg=True):
    vm.runasm('''
    mov	  r15, r14
    clr	  r15
    jmp	  12
    mov.b  @r14, r13
    sxt	  r13                      
    add	  r15, r13               
    mov	  r13, r15
    add	  r15, r15
    add	  r15, r15
    add	  r15, r15
    add	  r15, r15
    add	  r15, r15
    sub	  r13, r15
    inc	  r14
    tst.b	  0x0(r14)
    jnz	  -12
    ret''',
    dbg=dbg)


def get_from_table(vm, dbg=False):
    vm.runasm('''
    push	r11
    push	r10
    push	r9
    push	r8
    push	r7
    push	r6
    mov	r15, r10
    mov	r14, r6
    mov	r14, r15
    call    hash

    mov	#0x1, r11
    mov	0x2(r10), r13
    tst	r13
    jz	4
    add	r11, r11
    dec	r13
    jnz     -2
    add	#-0x1, r11
    and	r15, r11
    add	r11, r11
    mov	0x6(r10), r13
    add	r11, r13
    mov	@r13, r9
    clr	r8
    jmp	11
    mov	r9, r7
    mov	r9, r14
    mov	r6, r15
    call  strcmp
    add	#0x12, r9
    tst	r15
    jnz	3
    mov	0x10(r7), r15
    jmp	7
    inc	r8
    mov	0x8(r10), r15
    add	r11, r15
    cmp	@r15, r8
    jl	-13
    mov	#-0x1, r15
    pop	r6
    pop	r7
    pop	r8
    pop	r9
    pop	r10
    pop	r11
    ret''',
    dbg=dbg)

        
def fuzz_get_from_table(pw_chr_list):
    """
    r15 is the heap? or tree structure start?
    r15 @5006 0000 0300 0500 1650
    r14 is the key str
    """
    vm = VM(subroutines={'strcmp': strcmp, 'hash': _hash})
    vm.state.r14 = i16(0x3df3)
    vm.state.r15 = i16(0x5006)
    memset([i16(0x0), i16(0x0300), i16(0x0500), i16(0x1650)], 0x3df3, vm)
    memset(pw_chr_list, 0x5006, vm)
    get_from_table(vm, dbg=False)

    if vm.state.r15 != i16(-1):
        print('[*]', vm.state.r15, pw_chr_list)
    elif pw_chr_list[0] % 10 == 0:
        sys.stdout.flush()
        sys.stdout.write('.')
    

for i in range(1, 255):
    for j in range(1, 333):
        fuzz_get_from_table([i for _ in range(j)])


# There is an int underflow in hash!
