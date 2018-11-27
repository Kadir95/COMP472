from mpi4py import MPI
import random
import math

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

def rand_a_dot():
    x = random.random() - .5
    y = random.random() - .5
    distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    if distance < .5:
        return True
    return False

try_count = 1000000
hit = 0
for i in range(try_count):
    if rand_a_dot():
        hit += 1

approx = hit / float(try_count) * 4
print("<rank:%d> approx:%f" %(rank, approx))

global_approx = MPI.COMM_WORLD.reduce(approx, op=MPI.SUM, root=0)

if rank == 0:
    global_approx = global_approx / size
    print("pi:", global_approx)