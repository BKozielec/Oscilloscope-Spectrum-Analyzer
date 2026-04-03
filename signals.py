import numpy as np
from scipy import signal


def sin(A,B,phi,tstart,tstop,fs,f): #Asin(2pift + phi) + B;
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples)
    y= A*np.sin(2*np.pi*f*t+phi) + B   
    return [t,y]

def rectangle(A,B,phi,duty,tstart,tstop,fs,f):
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples)
    y=A * signal.square(2 * np.pi * f * t + phi, duty=duty) + B 
    return [t,y]





