#!/usr/bin/python3

from z3 import (
    And,
    Const,
    Datatype,
    Exists,
    ForAll,
    Function,
    Implies,
    Int,
    IntSort,
    IntVal,
    Or,
    SolverFor,
    z3,
)
import sys

solver = SolverFor('LIA')
z3.set_option(model=True)
z3.set_option(stats=True)
z3.set_option(verbose=2)

Command = Datatype('Command')
Command.declare('Forward', ('amount', IntSort()))
Command.declare('Down', ('amount', IntSort()))
Command.declare('Up', ('amount', IntSort()))
Command = Command.create()

input = Function('input', IntSort(), Command)
n_inputs = 0
for (i, line) in enumerate(sys.stdin.readlines()):
    [direction, _, amount] = line.partition(' ')
    amount = int(amount)
    if direction == 'forward':
        command = Command.Forward(amount)
    elif direction == 'down':
        command = Command.Down(amount)
    elif direction == 'up':
        command = Command.Up(amount)
    else:
        raise Exception('bad direction "' + direction + '"')
    solver.add(input(i) == command)

    n_inputs += 1

aim = Function('aim', IntSort(), IntSort())
solver.add(aim(-1) == 0)
distance = Function('distance', IntSort(), IntSort())
solver.add(distance(-1) == 0)
depth = Function('depth', IntSort(), IntSort())
solver.add(depth(-1) == 0)
index = Int('index')
command = Const('command', Command)
amount = Int('amount')
solver.add(ForAll(
    index,
    Implies(
        And(index >= 0, index < n_inputs),
        Exists(
            amount,
            Or(
                And(
                    input(index) == Command.Forward(amount),
                    aim(index) == aim(index - 1),
                    distance(index) == distance(index - 1) + amount,
                    depth(index) == depth(index - 1) + aim(index - 1) * amount,
                ),
                And(
                    input(index) == Command.Up(amount),
                    aim(index) == aim(index - 1) - amount,
                    distance(index) == distance(index - 1),
                    depth(index) == depth(index - 1),
                ),
                And(
                    input(index) == Command.Down(amount),
                    aim(index) == aim(index - 1) + amount,
                    distance(index) == distance(index - 1),
                    depth(index) == depth(index - 1),
                ),
            ),
        ),
    ),
))

output = Int('output')
solver.add(output == distance(n_inputs - 1) * depth(n_inputs - 1))

print('Solving:')
print(solver.to_smt2())
if solver.check() == z3.sat:
    model = solver.model()
    print('\nSolution found:', model[output])
else:
    print('\nNo valid solutions')
print()
print(solver.statistics())
