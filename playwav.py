#!/usr/bin/env python
import sys
import os

samplefile = sys.argv[1]
os.system('aplay ' + samplefile)
