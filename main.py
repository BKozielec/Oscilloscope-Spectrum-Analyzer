import matplotlib.pyplot as plt
import numpy as np
from signals import sin, rectangle
from scipy import signal

#[t,y]=sin(1,2,np.pi,0,1,1000,5 )
#plt.plot(t,y)
#plt.show()

t,y=rectangle(1,2,np.pi,0.5,0,1,1000,5)
plt.plot(t,y)
plt.show()






