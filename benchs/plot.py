import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

filename = sys.argv[1]
reader = csv.reader(open(filename, 'r'), delimiter=' ')
x, y = map(np.array, zip(*reader))
plt.plot(x, y)
clean_filename = os.path.basename(os.path.splitext(filename)[0])
plt.savefig('images/%s.png' % clean_filename)
