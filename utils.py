def fetch_1st_arg(fn):
    """
    Decorator for 2 operand assembly instructions.
    If arg 0 is address or register, fetches uint16 value.
    """

    def inner(arg0, arg1, state, mem):
        if isinstance(arg0, str):
            if arg0.startswith('@'):
                arg0 = from_addr(arg0[1:], state, mem)
            else:
                arg0 = state[arg0]

        return fn(arg0, arg1, state, mem)

    return inner
    

def get_offset(locator):
    splitted = locator.split('+')

    if len(splitted) == 2:
        offset = int(splitted[1])
    else:
        offset = 0

    return (locator, offset)


def from_addr(locator, state, mem):
    """ Fetches address stored in a register from memory. """

    r, offset = get_offset(locator)

    return mem[state[r] + offset]


def setz(r, state):
    if state[r] == 0:
        state.flags.z = True


def memset(s, addr, state, mem):
    # TODO: make it work for non printables
    
    for i, c in enumerate(s):
        mem[addr + i] = ord(c)
