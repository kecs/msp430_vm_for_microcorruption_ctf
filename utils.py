import pdb
from collections import OrderedDict

        
def fetch_1st_arg(fn):
    """
    Decorator for assembly instructions.
    If 1st arg is address or register, fetches uint16 value.
    Marks fn with `is_instruction`
    """

    fn.is_instruction = True
    
    def inner(*args, **kwargs):
        if len(args) == 2:
            arg0 = args[0]
            if isinstance(arg0, str):
                if arg0.startswith('@'):
                    arg0 = from_addr(arg0[1:])
                else:
                    arg0 = state[arg0]

            return fn(arg0, args[1], **kwargs)
    
        return fn(*args, **kwargs)
    
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


def setz(r, state):
    if state[r] == 0:
        state.flags.z = True


def print_state(state, mem):
    for k, v in state.items():
        print('k' + ':  ', v)

    print('\n')


def memset(s, addr, state, mem):
    # TODO: make it work for non printables
    
    for i, c in enumerate(s):
        mem[addr + i] = ord(c)
