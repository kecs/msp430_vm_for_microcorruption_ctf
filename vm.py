import pdb
import sys


class Num(object):
    @staticmethod
    def get_val(n):
        if isinstance(n, Num):
            return n.val
        elif isinstance(n, int):
            return n
    
    def __init__(self, n):
        self.val = self.get_val(n)
        
    def __iadd__(self, n):
        n = self.get_val(n)

        if self.val + n > 0xffff:
            self.val = self.val + n - 0xffff - 1
        else:
            self.val += n

        return self

    def __isub__(self, n):
        n = self.get_val(n)
        
        if self.val - n < 0:
            self.val = 0xffff - (self.val - n)
        else:
            self.val = self.val - n

        return self
            
    def __gt__(self, n):
        n = self.get_val(n)
        
        return self.val > n
    
    def __lt__(self, n):
        n = self.get_val(n)
        
        return self.val < n

    def __repr__(self):
        return hex(self.val)
        

r7  = Num(0)
r8  = Num(0)
r9  = Num(0)
r10 = Num(0)
r11 = Num(0)
r12 = Num(0)
r13 = Num(0)
r14 = Num(0)
r15 = Num(0)
sp  = Num(0)
flags = {'z': 0}

mem = [0 for i in range(0x4daf)]


def ctx(fn):
    global r7
    global r8
    global r9
    global r10
    global r11
    global r12
    global r13
    global r14
    global r15    

    def inner(*args, **kwargs):
        return fn(*args, r8=r8, r9=r9, r10=r10, r11=r11, r12=r12, r13=r13, r14=r14, r15=r15, flags=flags, **kwargs)
    
    return  inner

@ctx
def mov(n, rb, **kwargs):
    if isinstance(n, str) and n[0] == '@':
        n = from_stack(n[1:])
    
    rb.val = Num.get_val(n)
    
@ctx
def add(n, rb, **kwargs): rb += n

@ctx
def inc(r, **kwargs): r += 1

@ctx
def dec(r, **kwargs):
    r -= 1

    if r.val == 0:
        flags.z = True


@ctx
def clr(r, **kwargs): r.val = 0

@ctx
def sxt(r, **kwargs): pass

@ctx
def from_stack(locator, **kwargs):
    splitted = locator.split('+')
    locator = splitted[0]
    
    if len(splitted) == 2:
        offset = int(splitted[1])
    else:
        offset = 0
        
    return mem[kwargs[locator].val + offset]
        
@ctx
def printr(**kwargs):
    print('r7: ', r7)
    print('r8: ', r8)
    print('r9: ', r9)
    print('r10:', r10)
    print('r11:', r11)
    print('r12:', r12)
    print('r13:', r13)
    print('r14:', r14)
    print('r15:', r15)
    print('\n')


@ctx
def _and(r1, r2, **kwargs):
    r2.val = r1.val & r2.val

    
@ctx
def tst(r, **kwargs):
    if isinstance(r, str) and n[0] == '@':
        r = Num(from_stack(r[1:]))
    
    if r.val == 0:
        flags['z'] = True
    else:
        flags['z'] = False

        
@ctx
def tstb(r, **kwargs):
    if isinstance(r, str) and n[0] == '@':
        r = Num(from_stack(r[1:]))
    
    if repr(r)[-2:] == '00' or r.val == 0:
        flags['z'] = True
    else:
        flags['z'] = False


        
def before_get_from_table():
    mov('@r11', r15)
    tstb(r15)
    if flags.z return False
    mov(r10, r13)
    add(r13, r13)
    add(r13, r13)
    add(r10, r13)
    add(r13, r13)
    mov('@r11', r10)
    sxt(r10)
    add(0xffd0, r10)
    add(r13, r10)
    inc(r11)

    return True
    

def hash():
    mov(r15, r14)           # 0e4f
    clr(r15)                    # 4810
    # instead of jmp, inlined
    tstb('@r14')              # 482a   
    if flags.z: return
    # endinstead
    movb('@r14', r13)    # 4814
    sxt(r13)                   # 4816
    add(r15, r13)          # 4818
    mov(r13, r15)          # 481a
    add(r15, r15)          # 481c
    add(r15, r15)          # 481e
    add(r15, r15)          # 4820
    add(r15, r15)          # 4822
    add(r15, r15)          # 4824
    sub(r13, r15)          # 4826
    inc(r14)                  # 4828

    
def get_from_table():
#           push	r11         # 49cc
#           push	r10         # 49ce
#           push	r9          # 49d0
#           push	r8          # 49d2
#           push	r7          # 49d4
#           push	r6          # 49d6
    mov(r15, r10)             # 49d8
    mov(r14, r6 )              # 49da
    mov(r14, r15)             # 49dc
    hash()                        # 49de
    mov(0x1, r11)             # 49e2
    mov	0x2(r10), r13      # 49e4
    tst(r13)                      # 49e8

    while flags.z is False:
        add(r11, r11)         # 49ec
        dec(r13)                # 49ee
    
    add(-0x1, r11)            # 49f2
    _and(r15, r11)            # 49f4
    add(r11, r11)             # 49f6
    mov(from_stack('r10+6'), r13)          # 49f8
    add(r11, r13)             # 49fc
    mov('@r13', r9)          # 49fe
    clr(r8)                        # 4a00
    jmp	#0x4a1e <get_from_table+0x52>          # 4a02
    
    mov	r9, r7          # 4a04
    mov	r9, r14          # 4a06
    mov	r6, r15          # 4a08
    call	#0x4d7c <strcmp>          # 4a0a
    add	#0x12, r9          # 4a0e
    tst	r15          # 4a12
    jnz	#0x4a1c <get_from_table+0x50>          # 4a14
    mov	0x10(r7), r15          # 4a16
    jmp	#0x4a2a <get_from_table+0x5e>          # 4a1a
    inc	r8          # 4a1c
    
    mov	0x8(r10), r15          # 4a1e
    add	r11, r15          # 4a22
    cmp	@r15, r8          # 4a24
    jl	#0x4a04 <get_from_table+0x38>          # 4a26
    mov	#-0x1, r15          # 4a28
#           pop	r6          # 4a2a
#           pop	r7          # 4a2c
#           pop	r8          # 4a2e
#           pop	r9          # 4a30
#           pop	r10          # 4a32
#           pop	r11          # 4a34


    
pin_place = 0x3df7
mov(r8, 0x5006)

mov(pin_place, r11)
clr(r10)

pin = 'abc'
for i, c in enumerate(pin): 
    mem[pin_place + i] = ord(c)

#pdb.set_trace()
while before_get_from_table():
    pass
    #printr()
    
mov(r8, r15)
get_from_table()

if r15 != 0xffff:
    print('[*] Goooood: ' + r15 + ' ' + pin)

