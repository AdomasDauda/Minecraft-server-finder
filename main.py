from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

step = 16

for i in range(0, 256, step):
    p = f'python finder.py -o out.txt -s {i} -e {i+step}'
    output = Popen(p, stdout=PIPE)