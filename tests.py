import time
import unittest

from instructions import *
from parser import (parse_asm_line, parse_asm_lines)


# def provide_state_for_instructions(state, mem):
#     for k, v in globals().items():
#         if hasattr(v, 'is_instruction'):
#             def wrapped_fn(*args, **kwargs):
#                 return fn(*args, state=state, mem=mem, **kwargs)
        
#             __builtins__[k] = wrapped_fn

class TestParser(unittest.TestCase):
    def test_parse_asm_line_mov(self):
        result = parse_asm_line('        --->4ba2:  0f41            mov	sp, r15   # comment')

        self.assertEqual(result, (mov, ('sp', 'r15')))



class TestState(unittest.TestCase):
    def test_reset(self):
        state, mem = State.reset()

        self.assertEqual(mem[state.sp], 0)

        
class TestUtils(unittest.TestCase):    
    def setUp(self):
        self.state, self.mem = State.reset()

    @unittest.skip("Not now")
    def test_mov(self):
        provide_state_for_instructions(self.state, self.mem)
        
        mov(0x3, 'r8')

        self.assertEqual(mem[state.sp], 0x3)

    @unittest.skip("Not now")
    def test_setz(self):
        pass

    @unittest.skip("Not now")
    def test_add(self):
        pass

    @unittest.skip("Not now")
    def test_sub(self):
        pass

    @unittest.skip("Not now")
    def test_inc(self):
        pass

    @unittest.skip("Not now")
    def test_dec(self):
        pass

    @unittest.skip("Not now")
    def test_clr(self):
        pass

    @unittest.skip("Not now")
    def test_sxt(self):
        pass

    @unittest.skip("Not now")
    def test__and(self):
        pass

    @unittest.skip("Not now")
    def test_push(self):
        pass

    @unittest.skip("Not now")
    def test_pop(self):
        pass

    @unittest.skip("Not now")
    def test_call(self):
        pass

    @unittest.skip("Not now")
    def test_ret(self):
        pass

    @unittest.skip("Not now")
    def test_tst(self):
        pass

    @unittest.skip("Not now")
    def test_tstb(self):
        pass

    @unittest.skip("Not now")
    def test_from_addr(self):
        pass

    @unittest.skip("Not now")
    def test_jmp(self):
        pass

    @unittest.skip("Not now")
    def test_jz(self):
        pass

    @unittest.skip("Not now")
    def test_cmp(self):
        pass

    @unittest.skip("Not now")
    def test_cmpb(self):
        pass

    @unittest.skip("Not now")
    def test_jnz(self):
        pass
    
    @unittest.skip("Not now")
    def test_jeq(self):
        pass

    @unittest.skip("Not now")
    def test_jge(self):
        pass

    @unittest.skip("Not now")
    def test_jl(self):
        pass


unittest.main()
