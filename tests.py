import time
import unittest
from numpy import uint16 as i16

from instructions import *
from vm import VM
from asm_parser import (parse_asm_line,
                    parse_asm_lines,)


class TestParser(unittest.TestCase):    
    def test_parse_asm_line_2operand_reg_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov     sp, r15   # comment'),
                         (mov, 'sp', 'r15'))

    def test_parse_asm_line_2operand_reg_addr_plus_offset_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov 0x2(r4), r11  # comment'),
                         (mov, '@r4+2', 'r11'))

    def test_parse_asm_line_2operand_reg_addr_to_reg_plus_offset(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov r13, 0x13(r13)  # comment'),
                         (mov, 'r13', '@r13+19'))

    def test_parse_asm_line_2operand_reg_addr_plus_offset_to_reg_plus_offset(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov 0x3(r4), 0x2(r11)  # comment'),
                         (mov, '@r4+3', '@r11+2'))
        
    def test_parse_asm_line_2operand_const_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  #0xff, r11   # comment'),
                         (mov, 0xff, 'r11'))

    def test_parse_asm_line_2operand_addr_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  @r10, r10   # comment'),
                         (mov, '@r10', 'r10'))

    def test_parse_asm_line_2operand_0x0_reg_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  0x0(r10), r10   # comment'),
                         (mov, '@r10', 'r10'))

    def test_parse_asm_line_2operand_reg_to_0x0_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  r10, 0x0(r10)   # comment'),
                         (mov, 'r10', '@r10'))

    def test_parse_asm_line_2operand_0x0_reg_to_0x0_reg_1(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  0x0(r10), 0x0(r11)   # comment'),
                         (mov, '@r10', '@r11'))

    def test_parse_asm_line_2operand_0x0_reg_to_0x0_reg_2(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     and  0x0(r10), 0x0(r11)   # comment'),
                         (and_, '@r10', '@r11'))

    def test_parse_asm_line_1operand_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     sxt  r10   # comment'),
                         (sxt, 'r10'))


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.vm = VM() 
        self.state, self.mem = self.vm.state, self.vm.mem

    def test_mov_const_to_reg(self):
        mov(i16(0x3), 'r8', self.state, self.mem)
        self.assertEqual(self.state.r8, i16(0x3))

    def test_mov_reg_to_reg(self):
        self.state.r4 = i16(0x3)
        mov('r4', 'r8', self.state, self.mem)
        self.assertEqual(3, self.state.r8)

    def test_mov_addr_to_reg(self):
        self.mem[0x666] = (0x1234)
        self.state.r4 = i16(0x666)
        mov('@r4', 'r4', self.state, self.mem)
        self.assertEqual(0x1234, self.state.r4)

    def test_mov_addr_plus_offset_to_reg(self):
        self.mem[0x66a] = i16(0x1234)
        self.state.r4 = i16(0x666)
        mov('@r4+4', 'r4', self.state, self.mem)
        self.assertEqual(0x1234, self.state.r4)

    def test_mov_addr_to_reg_2(self):
        self.mem[0x666] = i16(0x1234)
        self.state.r4 = i16(0x666)
        self.state.r5 = i16(0x555)
        mov('@r4', '@r5', self.state, self.mem)
        self.assertEqual(0x1234, self.mem[i16(0x555)])

    def test_mov_addr_plus_offset_to_reg_plus_offset(self):
        place_1 = 0x333
        place_2 = 0x4231
        val_1   = 0x1234
        
        self.mem[place_1 + 4] = i16(val_1)
        self.state.r4 = i16(place_1)
        self.state.r6 = i16(place_2)
        mov('@r4+4', '@r6+3', self.state, self.mem)
        self.assertEqual(0x1234, self.mem[self.state.r4 + 4])
        self.assertEqual(0x1234, self.mem[self.state.r6 + 3])

    def test_movb_addr_to_reg(self):
        self.mem[0x666] = i16(0x1234)
        self.state.r4 = i16(0x666)
        self.state.r5 = i16(0x555)
        movb('@r4', '@r5', self.state, self.mem)
        self.assertEqual(0x34, self.mem[i16(0x555)])

    def test_add_reg_to_reg(self):
        self.state.r4 = i16(0x666)
        self.state.r5 = i16(0x555)
        add('r4', 'r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x555) + i16(0x666))

    def test_addb_reg_to_reg(self):
        self.state.r4 = i16(0x666)
        self.state.r5 = i16(0x555)
        addb('r4', 'r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x555) + i16(0x66))

    def test_sub_reg_to_reg(self):
        self.state.r4 = i16(0x5)
        self.state.r5 = i16(0x1234)
        sub('r4', 'r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x1234) - i16(0x5))

    def test_inc_reg(self):
        self.state.r5 = i16(0x1234)
        inc('r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x1235))

    def test_dec_reg(self):
        self.state.r5 = i16(0x1234)
        dec('r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x1233))


    def test_clr_reg(self):
        self.state.r5 = i16(0x1234)
        clr('r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0))

    def test_sxt_reg(self):
        self.state.r5 = i16(0x80)
        sxt('r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0xff80))

    def test_and_reg_reg(self):
        self.state.r5 = i16(0x80)
        self.state.r6 = i16(0x80)
        and_('r5', 'r6', self.state, self.mem)
        self.assertEqual(self.state.r6, i16(0x80))
        
    def test_push_const(self):
        self.state.sp = i16(0x33)
        push(i16(0x1234), self.state, self.mem)
        self.assertEqual(self.mem[i16(0x32)], i16(0x1234))

    def test_push_reg(self):
        self.state.sp = i16(0x13)
        self.state.r5 = i16(0x80)
        push('r5', self.state, self.mem)
        self.assertEqual(self.mem[i16(0x12)], i16(0x80))

    def test_pop(self):
        self.state.sp = i16(0x13)
        self.state.r5 = i16(0x80)
        push('r5', self.state, self.mem)
        self.state.r5 = i16(0x3)
        pop('r5', self.state, self.mem)
        self.assertEqual(self.state.r5, i16(0x80))
        
    def test_tstb_false(self):
        self.state.r5 = i16(0xdead)
        tstb('r5', self.state, self.mem)
        self.assertEqual(self.state.flags.z, False)

    def test_tstb_true(self):
        self.state.r5 = i16(0x100)
        tstb('r5', self.state, self.mem)
        self.assertEqual(self.state.flags.z, True)

    def test_jnz(self):
        self.state.flags.z = False
        ret = jnz(i16(0x4321), self.state, self.mem)
        self.assertEqual(ret, i16(0x4321))
        

class TestSnippetParseAndExecuteWithJmp(unittest.TestCase):
    def setUp(self):
        self.vm = VM() 
        self.state, self.mem = self.vm.state, self.vm.mem

    def test_cycle(self):
        self.vm.runasm("""
        mov #0x0, sp
        mov #0x10, r8
        mov r8, 0x0(sp)
        inc sp
        dec r8
        jnz #-0x3
        """)

        self.assertEqual(self.mem[1], i16(0xf))
        
unittest.main()
