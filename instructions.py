from utils import (State,
                   from_addr,
                   print_state,)

def setz(r, state, mem):
    if state[r] == 0:
        state.flags.z = True
        
def add(n, rb, state, mem):
    if rb.startswith('@'):
        mem[state[rb[1:]]] += n
    else:
        state[rb] += n

    setz(rb)

def sub(n, rb, state, mem):
    if rb.startswith('@'):
        mem[state[rb[1:]]] -= n
    else:
        state[rb] -= n

    setz(rb)
    

def inc(r, state, mem):
    state[r] += 1

    setz(r)


def dec(r, state, mem):
    state[r] -= 1
    
    setz(r)


def clr(r, state, mem):
    state[r] = 0


def sxt(r, state, mem):
    state[r] &= 0x00ff

    if 0x80 <=  state[r] <= 0xff:
        state[r] += 0xff00


def _and(ra, rb, state, mem):
    if rb.startswith('@'):
        mem[state[rb[1:]]] &= ra
    else:
        state[rb] &= n

    setz(rb)
        

def push(r, state, mem):
    high_byte = state[r] >> 8
    low_byte  = state[r] & 0x00ff
    
    mem[state.sp + 1] = high_byte
    mem[state.sp]       = low_byte
        
    state.sp -= 2
    

def pop(r, state, mem):
    high_byte = mem[state.sp + 1]
    low_byte  = mem[state.sp]

    state[r] = (high_byte << 8) | low_byte
    state.sp += 2

    return state[r]


def call(fn, state, mem):
    """ Args: fn is a pyhton callable """
    
    push('pc')
    return fn()


def ret(state, mem):
    return pop('pc')
    

def tst(r, state, mem):
    if isinstance(r, str) and r.startswith('@'):
        r = from_addr(r[1:])
    
    if r == 0:
        state.flags.z = True
    else:
        state.flags.z = False
        

def tstb(r, state, mem):
    if isinstance(r, str) and r.startswith('@'):
        r = from_addr(r[1:])

    tst(r & 0x00ff, **kwargs)


def jmp(addr, state, mem):
    return addr


def jz(addr, state, mem):
    if state.flags.z:
        return addr


def cmp(ra, rb, state, mem):
    if isinstance(rb, str) and rb.startswith('@'):
        rb = from_addr(rb[1:])

    # TODO: refactor
    if ra <= rb:
        state['flags']['ge'] = True
    else:
        state['flags']['ge'] = False

    if ra >= rb:
        state['flags']['jl'] = True
    else:
        state['flags']['jl'] = False
        
    if ra != rb:
        state['flags']['z'] = True
        state['flags']['eq'] = False
    else:
        state['flags']['z'] = False
        state['flags']['eq'] = True


def cmpb(ra, rb, state, mem):
    if isinstance(rb, str) and rb.startswith('@'):
        rb = from_addr(rb[1:])

    return cmp(ra & 0x00ff, rb & 0x00ff, **kwargs)
        

def jnz(addr, state, mem):
    if not state.flags.z:
        return addr


def jeq(addr, state, mem):
    if state.flags.eq:
        return addr


def jge(addr, state, mem):
    # TODO: implement, adjust cmp
    if state['flags']['ge']:
        return addr


def jl(addr, state, mem):
    # TODO: implement, adjust cmp
    if not state['flags']['z']:
        return addr


def b(state, mem):
    """ Debug instruction """
    
    print_state()
    pdb.set_trace()

jne = jnz