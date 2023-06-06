"""
Herramienta que permite liberar un puerto matado el proceso que lo utiliza.

Author: Alejandro Priego Izquierdo
"""
import subprocess
import os
from sys import argv, stderr

STATUS = ["LISTENING", "ESTABLISHED", "CLOSE_WAIT", "TIME_WAIT"]

if len(argv) == 1:
    print("Debes introducir un puerto", file=stderr)
    exit(1)

if len(argv) == 3 and len(argv[2]) not in STATUS:
    print("Debes introducir un estado válido", file=stderr)
    exit(1)

if len(argv) < 0 or len(argv) > 3:
    print("Faltan argumentos o hay más de los necesarios", file=stderr)
    exit(1)

try:
    if 65535 < int(argv[1]) or int(argv[1]) < 0:
        raise ValueError()
except ValueError:
    print("Debes introducir un puerto válido", file=stderr)
    exit(1)

PORT = argv[1]


proc = subprocess.Popen('netstat -nao', stdout=subprocess.PIPE)
output = str(proc.stdout.read()).replace("\\r\\n", "").replace("b'", "").split()
for n in range(9):
    output.remove(output[0])

clean_output = []
for _ in range(len(output)//5):
    temp = []
    if output[3] in STATUS:
        for _ in range(5):
            temp.append(output.pop(0))
    else:
        for _ in range(4):
            temp.append(output.pop(0))
    clean_output.append(temp.copy())

for n in clean_output:
    n.pop(2)


pid_to_kill = ""
for n in clean_output:
    stripped_port = n[1][-5:].strip(":")[-len(PORT):]
    if len(argv) == 2:
        if stripped_port == PORT:
            pid_to_kill = n[3]
            break
    else:
        if stripped_port == PORT and n[3] == argv[2]:
            pid_to_kill = n[3]

if os.name == "nt":
    subprocess.run(f'taskkill /PID {pid_to_kill} /F')
else:
    subprocess.run(f'kill -9 {pid_to_kill}')

print(pid_to_kill)
