from numpy import uint16 as i16

from asm_parser import parse_asm_lines


MEM_SIZE = 0x5350
STACK_START = 0x4400


class State(object):
    class Flags(object):
        z  = False
        c  = False
        gt = False  # Used for jumps instead of z, n, v
        eq = False  # Used for jumps instead of z, n, v

        def __repr__(self):
            return 'z: {}\nc: {}\ngt: {}\neq: {}\n'.format(self.z, self.c, self.gt, self.eq)
    
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

    def __getitem__(self, key):
        """ Support both state.attr and state['attr'] lookup. """
        
        return getattr(self, key)

    def __setitem__(self, key, attr):
        """ Support both state.attr and state['attr'] assignment. """

        if not (isinstance(attr, i16) or isinstance(attr, int)):
            raise ValueError('Registers in State must be ints! {} supplied.'.format(type(attr)))
        
        setattr(self, key, i16(attr))

    def __repr__(self):
        to_ret = ''
        
        attrs = [(k, v) for k, v in self.__dict__.items() if isinstance(v, i16)]
        attrs.sort(key=lambda t: t[0])
        
        for (k, v) in attrs:
            to_ret += '{}:  {}\n'.format(k, hex(v))

        to_ret += repr(self.flags)

        return to_ret

    
class VM(object):
    def __init__(self, state=None, mem=None):
        self.state = state or State()
        self.mem = mem or [0 for _ in range(MEM_SIZE)]

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
        

