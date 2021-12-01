#!/usr/bin/python3

from z3 import (
    And,
    If,
    Int,
    IntVal,
    Solver,
    Sum,
    z3
)
import sys

solver = Solver()
z3.set_option(model=True)
z3.set_option(stats=True)
z3.set_option(verbose=2)

input = [
    (Int('input' + str(i)), IntVal(int(x)))
    for (i, x) in enumerate(sys.stdin.readlines())
]
increases = [
    If(input[i - 1][0] < input[i][0], 1, 0)
    for i in range(1, len(input))
]
output = Int('output')
solver.add(And(
    output == Sum(increases),
    *(symbol == value for (symbol, value) in input),
))

print('Solving:')
print(solver.to_smt2())
if solver.check() == z3.sat:
    model = solver.model()
    print('\nSolution found:', model[output])
else:
    print('\nNo valid solutions')
print()
print(solver.statistics())
