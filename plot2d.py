import matplotlib.pyplot as plt
import numpy as np
a1=np.zeros((18,18))

plt.figure()
for i in range(40):
    plt.subplot(5,8,i+1)
    plt.imshow(a1)
    plt.colorbar()
    plt.grid()
