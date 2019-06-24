from CyClient import *
import time
import numpy as np
from matchUtil import *
from Cut import *
import matplotlib.pyplot as plt
cli = Client()
cli.sayHello()

cli.takAction(4,0,0)
time.sleep(0.5)
cli.takAction(3,0,0)