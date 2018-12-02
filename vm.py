from numpy import uint16 as i16

from parser import parse_asm_lines


MEM_SIZE = 0x5350
STACK_START = 0x4400


class State(object):
    class Flags(object):
        z  = False
        c  = False
        gt = False  # Used for jumps instead of z, n, v
        eq = False  # Used for jumps instead of z, n, v
    
    def __init__(self, **kwargs):
        registers = dict(('r{0}'.format(i), i16(0)) for i in range(4, 16))

        registers.update({
            'pc':     i16(0),
            'sp':     i16(STACK_START),
            'flags':  self.Flags(),
        })
        
        registers.update(kwargs)

        for k, v in registers.items():
            setattr(self, k, v)

    def __getitem__(self, item):
        """ Support both state.attr and state['attr'] lookup. """
        
        return getattr(self, item)

    def __setitem__(self, item, attr):
        """ Support both state.attr and state['attr'] assignment. """
        
        return setattr(self, item, attr)

    

class VM(object):
    def __init__(self, state=None, mem=None):
        self.state = state or State()
        self.mem = mem or tuple(0 for _ in range(MEM_SIZE))

    def runasm(self, *args):
        instructions = []
        
        for arg in args:
            if callable(arg):
                arg(self.state, self.mem)
            elif isinstance(arg, str):
                instructions += parse_asm_lines(arg)
            else:
                instructions.append(arg)

        for instruction in instructions:
            fn, params = instruction[0], instruction[1:]
            
            if fn.__name__.startswith('j'):
                pass
                # TODO: jmp?
            
            else:
                self.state.pc += 2
                fn(*(list(params) + [self.state, self.mem]))
        
