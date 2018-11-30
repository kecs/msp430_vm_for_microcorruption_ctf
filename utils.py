import pdb
from collections import OrderedDict
from numpy import uint16 as i16

from parser import parse_asm_lines


MEM_SIZE = 0x5350
STACK_START = 0x4400


class State(object):
    class Flags(object):
        z  = False
        c  = False
        gt = False  # Used for jl, jge, jne; instead of z, n, v
        eq = False # Used for jl, jge, jne; instead of z, n, v
    
    def __init__(self, **kwargs):
        registers = dict(('r{0}'.format(i), i16(0)) for i in range(4, 16))

        registers.update({
            'pc':      i16(0),
            'sp':      i16(STACK_START),
            'flags':  self.Flags(),
        })
        
        registers.update(kwargs)

        for k, v in registers.items():
            setattr(self, k, v)

    def __getitem__(self, item):
        """ Support both state.attr and state['attr'] lookup. """
        
        return getattr(self, item)
    

class VM(object):
    def __init__(self, state=None, mem=None):
        
        self.state = state or State()
        self.mem = mem or tuple(0 for _ in range(MEM_SIZE))):

    def runasm(self, *args):
        instructions = []
        
        for arg in args:
            if callable(arg):
                return arg(self.state, self.mem)
            elif isinstance(arg, str):
                instructions += parse_asm_lines(arg)
            else:
                instructions.append(arg)

        for instruction in instructions:
            instruction[0](*list(instruction)[1:], self.state, self.mem)
        
        
def inject_state(fn):
    """
    Decorator for assembly instructions.
    Falling back to global state if no explicit state / memory is provided. 
    If arg 0 is an address or register, fetches uint16 value.
    """
    
    global state
    global mem

    def inner(*args, **kwargs):
        if len(args) == 2:
            arg0 = args[0]
            if isinstance(arg0, str):
                if arg0.startswith('@'):
                    arg0 = from_addr(arg0[1:])
                else:
                    arg0 = state[arg0]

            return fn(arg0, args[1], state=state, mem=mem, **kwargs)
    
        return fn(*args, state=state, mem=mem, **kwargs)
    
    return  inner


def from_addr(locator, state, mem):
    """
    Fetches address stored in a register.
    e.g. `mov 0x8(r8), 0x2400` -> mov("r8+8", 0x2400)
    """
    
    splitted = locator.split('+')
    locator = splitted[0]
    
    if len(splitted) == 2:
        offset = int(splitted[1])
    else:
        offset = 0
        
    return mem[state[locator] + offset]


def print_state(state, mem):
    for k, v in state.items():
        print('k' + ':  ', v)

    print('\n')


def memset(s, addr, state, mem):
    # TODO: make it work for non printables
    
    for i, c in enumerate(s):
        mem[addr + i] = ord(c)
