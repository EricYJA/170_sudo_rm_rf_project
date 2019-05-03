import os
import subprocess
import time

cmd = "python client.py --solver solver"
total_score = 0
num_iter = 30

for i in range(num_iter):
    time.sleep(2)
    p = os.popen(cmd)
    x=p.read()

    last_line = x.split("\n")[-2]
    print(last_line)
    score = last_line.split(" ")[-1]

    total_score += float(score)

    print("tmp average:", total_score / (i + 1))
    

print("Average score:", total_score / num_iter)