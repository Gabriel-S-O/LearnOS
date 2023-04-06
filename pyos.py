from operator import iadd
import curses
import pycfg
from pyarch import fake_syscall_handler, load_binary_into_memory
from pyarch import cpu_t

DEFAULT_PROCCESS = 'load default'
CLEAR_CONSOLE = 'clear'
EXIT_COMMAND = 'exit'

SYS_EXIT = DEFAULT_PROCCESS = 'load default'
CLEAR_CONSOLE = 'clear'
EXIT_COMMAND = 'exit'

SYS_EXIT = 1

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
			if len(self.console_str) > 0:
				self.terminal.console_print("\r")
				self.console_str = self.console_str[:-1]
				self.terminal.console_print(self.console_str)
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.verify_input()
			self.clear()	

	def handle_interrupt (self, interrupt):
		if pycfg.INTERRUPT_MEMORY_PROTECTION_FAULT == interrupt:
			self.printk("Memory Protection Fault Interruption not Implemented yet")
		elif pycfg.INTERRUPT_KEYBOARD == interrupt:
			self.keyboard_interrupt_detected()
		elif pycfg.INTERRUPT_TIMER == interrupt:
			self.printk("Timer Interruption not Implemented yet")

	def clear (self):
		self.terminal.console_print('\r')
		self.console_str = ''

	def keyboard_interrupt_detected(self):
		self.interrupt_keyboard()

	def verify_input(self):
		if(self.console_str == CLEAR_CONSOLE):
			self.terminal.app_print('\r')
		elif (self.console_str == EXIT_COMMAND):
			self.stop_execution()
		elif self.console_str == DEFAULT_PROCCESS:
			self.load_process()
		else:
			self.terminal.app_print('\n' + self.console_str)

	def stop_execution(self):
		self.panic("System interrupted by user")

	def load_process(self):
		self.terminal.app_print("\nLoading default proccess...")

	def syscall_exit(self):
		self.terminal.end()
		self.cpu.cpu_alive = False
		self.terminal.dprint("pysim halted")

	def syscall(self):
		syscall_code = self.cpu.get_reg(0)
		if syscall_code == SYS_EXIT:
			self.syscall_exit()
			
