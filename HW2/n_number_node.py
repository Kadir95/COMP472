#!/usr/bin/python

import random
import math
from functools import reduce

def main():
    nodes = [random.randint(1, 100) for i in range(10)]

    mul = reduce(lambda x, y: x * y, nodes)

    print("Node number:", len(nodes))
    print("Root degree:", 1. / len(nodes))
    print("Mul        :", mul)
    print("Calculation:", math.pow(mul, (1. / len(nodes))))
    print("Ass NodeNum:", math.pow(math.pow(mul, (1. / len(nodes))), 1/2))

if __name__ == "__main__":
    main()