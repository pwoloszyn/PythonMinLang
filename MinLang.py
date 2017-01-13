import sys
import io
import re

back_stack = []
front_stack = []
variable_definitions = {}
end_app = False

def eval(cmd):

	if cmd[0]=='def':
		if len(cmd) != 4:
			errorPrintOut(cmd, 1)
		if not re.match('([a-z]|[A-Z])[^ \n\t]*', cmd[1]):
			errorPrintOut(cmd, 2)
		tmp = cmd[3]
		if tmp in variable_definitions:
			variable_definitions[cmd[1]] = variable_definitions[tmp]
		else:
			variable_definitions[cmd[1]] = tmp


	elif cmd[0]=='step':
		if len(cmd) != 2:
			errorPrintOut(cmd, 1)
		num_of_steps = 0
		tmp = cmd[1]
		if tmp in variable_definitions:
			tmp = variable_definitions[tmp]
		if re.match('-?\d+\.?\d*', tmp):
			if re.match('-?\d+', tmp):
				num_of_steps = int(tmp)
			num_of_steps = int(tmp)
			if num_of_steps < 0:
				if abs(num_of_steps) > len(back_stack):
					errorPrintOut(cmd, 3)
				for i in range(-1, abs(num_of_steps)):
					front_stack.append(back_stack.pop())
			else:
				if num_of_steps > len(front_stack):
					errorPrintOut(cmd, 3)
				for i in range(1, num_of_steps):
					back_stack.append(front_stack.pop())
		else:
			errorPrintOut(cmd, 4)

	elif cmd[0]=='cmp':
		if len(cmd) != 4:
			errorPrintOut(cmd, 1)
		if len(front_stack) < 3:
			errorPrintOut(cmd, 6)
		lhs = ''
		rhs = ''
		if cmd[1] in variable_definitions:
			lhs = variable_definitions[cmd[1]]
		else:
			lhs = cmd[1]
		if cmd[3] in variable_definitions:
			rhs = variable_definitions[cmd[3]]
		else:
			rhs = cmd[3]
		if lhs != rhs:
			back_stack.append(front_stack.pop())

	elif cmd[0]=='out':
		if len(cmd) > 1:
			for i in range(1, len(cmd)):
				if cmd[i] == "\\n":
					print()
				elif cmd[i] == "\\t":
					print('\t', end='')
				elif cmd[i] in variable_definitions:
					print(variable_definitions[cmd[i]], end='')
				else:
					print(cmd[i], end='')
		else:
			print()

	elif cmd[0]=='inc':
		if len(cmd) != 2:
			errorPrintOut(cmd, 1)
		if cmd[1] in variable_definitions:
			tmp = variable_definitions[cmd[1]]
			if re.match('-?\d+', tmp):
				variable_definitions[cmd[1]] = str(int(tmp) + 1)
			elif re.match('-?\d+\.\d*', tmp):
				variable_definitions[cmd[1]] = str(float(tmp) + 1)
			else:
				errorPrintOut(cmd, 4)

	elif cmd[0]=='dec':
		if len(cmd) != 2:
			errorPrintOut(cmd, 1)
		if cmd[1] in variable_definitions:
			tmp = variable_definitions[cmd[1]]
			if re.match('-?\d+', tmp):
				variable_definitions[cmd[1]] = str(int(tmp) - 1)
			elif re.match('-?\d+\.\d*', tmp):
				variable_definitions[cmd[1]] = str(float(tmp) - 1)
			else:
				errorPrintOut(cmd, 4)

	elif cmd[0]=='end':
		if len(cmd) > 1:
			errorPrintOut(cmd, 1)
		end_app = True
		sys.exit()

	else:
		errorPrintOut(cmd,5)

#works!
def errorPrintOut(cmd, mod):
	if mod == 1:
		print('Syntax error (incorrect number of arguments): ')
	elif mod == 2:
		print('Syntax error (incorrect variable name): ')
	elif mod == 3:
		print('Error (to many steps): ')
	elif mod == 4:
		print('Error (incorrect variable type): ')
	elif mod == 5:
		print('Syntax error (unknown syntax): ')
	elif mod == 6:
		print('Error (insufficient room for the cmp instruction): ') 
	for s in cmd:
		print(s, end=' ')
	print()
	sys.exit()

#works!
def tokenize(inp):
	out_list = []
	str_bld = []
	is_quote = False
	for i in inp:
		c = i
		if c == '\"':
			if is_quote:
				is_quote = False
			else:
				is_quote = True
		elif c == ' ' and not is_quote:
			if len(str_bld) > 0:
				out_list.append(''.join(str_bld))
				str_bld = []
		else:
			str_bld.append(c)
	if len(str_bld) > 0:
		out_list.append(''.join(str_bld))
	return out_list

if len(sys.argv) > 1:
	file = open(sys.argv[1], 'r')
	print('Running file: ', end='')
	print(sys.argv[1])
else:
	print('No file specified.')
	sys.exit

for line in file:
	inp = line
	if inp[len(inp)-1] == '\n':
		inp = inp[:-1]
	back_stack.append(tokenize(inp))

while len(back_stack) > 0:
	front_stack.append(back_stack.pop())
cmd = []
while not end_app and len(front_stack) > 0:
	cmd = front_stack[-1]
	back_stack.append(front_stack.pop())
	eval(cmd)