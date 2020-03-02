#!/home/ntonasa/miniconda3/envs/TL/bin/python

#https://stackoverflow.com/questions/6086047/get-output-of-python-script-from-within-python-script
import subprocess
proc = subprocess.Popen(['python', 'client.py',  'arg1', 'arg2', 'arg3', 'arg4'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(proc.communicate()[0])