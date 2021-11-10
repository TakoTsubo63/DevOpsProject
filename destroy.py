#!/bin/python3
import os
path = (os.path.expanduser('~'))
os.chdir(path+"/projectTerra")
os.system("terraform apply -destroy")
