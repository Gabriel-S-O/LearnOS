import os
import curses
import pycfg
from pyarch import fake_syscall_handler, load_binary_into_memory
from pyarch import cpu_t

STOP_EXECUTION = 'exit'
OPEN_CALCULATOR = 'calc'
CLEAR_CONSOLE = 'clear'

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		
	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()
		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			strchar = chr(key)
			self.terminal.console_print(strchar)
			self.console_str += strchar
		elif key == curses.KEY_BACKSPACE:
			#self.console_str = self.console_str.rstrip(self.console_str[-1])
			self.console_str = ''
			self.terminal.console_print('\r')
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.verify_input()
			self.clear()	

	def handle_interrupt (self, interrupt):
		if pycfg.INTERRUPT_KEYBOARD == interrupt:
			self.keyboard_interrupt_detected()

	def clear (self):
		self.terminal.console_print('\r')
		self.console_str = ''

	def keyboard_interrupt_detected(self):
		self.interrupt_keyboard()

	def verify_input(self):
		if(self.console_str == STOP_EXECUTION):
			self.cpu.set_reg(0, 0)
		elif(self.console_str == CLEAR_CONSOLE):
			self.terminal.app_print('\r')
		else:
			self.terminal.app_print('\n' + self.console_str)
		self.syscall()

	def syscall (self):
		return
	
