'''
import subprocess
with open("output.txt", "w+") as output:
    subprocess.call(["python", "./WriteToFile.py"], stdout=output);
'''