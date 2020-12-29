# https://adventofcode.com/2020/day/8
import sys


input = [line.strip() for line in sys.stdin]


# part 1
program = [[opcode, int(arg)] for opcode, arg in [l.split() for l in input]]


def run(program, termination_fn):
    pc, acc, cycle = 0, 0, 0
    while not termination_fn(pc, cycle):
        instr, arg = program[pc]
        if instr == 'acc': acc += arg
        if instr == 'jmp': pc += arg - 1
        pc += 1
        cycle += 1
    return (halted := pc == len(program)), acc

line_executions = [0] * len(program)
def has_entered_inf_loop(pc, cycle):
    line_executions[pc] += 1
    return line_executions[pc] > 1

print(run(program, has_entered_inf_loop)[1])

# part 2
swap = {'nop': 'jmp', 'jmp': 'nop', 'acc': 'acc'}
for i in range(len(program)):
    program[i][0] = swap[program[i][0]]
    has_halted, acc = run(program, lambda pc, cycle: pc >= len(program) or cycle >= len(program))
    if has_halted:
        print(acc)
    program[i][0] = swap[program[i][0]]
