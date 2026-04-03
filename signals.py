import numpy as np
from scipy import signal


def sin(A,B,phi,tstart,tstop,fs,f): #Asin(2pift + phi) + B;
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples,endpoint=False)
    y= A*np.sin(2*np.pi*f*t+phi) + B   
    return [t,y]

def rectangle(A,B,phi,duty,tstart,tstop,fs,f):
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples,endpoint=False)
    y=A * signal.square(2 * np.pi * f * t + phi, duty=duty) + B 
    return [t,y]

def triangle(A,B,phi,tstart,tstop,fs,f,width=0.5,):
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples,endpoint=False)
    y=A * signal.sawtooth(2 * np.pi * f * t + phi,width=width) + B 
    return [t,y]

def sawtooth(A,B,phi,tstart,tstop,fs,f,width=1,):
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples,endpoint=False)
    y=A * signal.sawtooth(2 * np.pi * f * t + phi,width=width) + B 
    return [t,y]

def invsawtooth(A,B,phi,tstart,tstop,fs,f,width=0,):
    duration = tstop - tstart
    num_samples=int(duration*fs)
    t=np.linspace(tstart,tstop,num_samples,endpoint=False)
    y=A * signal.sawtooth(2 * np.pi * f * t + phi,width=width) + B 
    return [t,y]

def pulse(A, B, t_start_pulse, width, tstart, tstop, fs):
    duration = tstop - tstart
    num_samples = int(duration * fs)
    t = np.linspace(tstart, tstop, num_samples, endpoint=False)
    y = A * ((t >= t_start_pulse) & (t < t_start_pulse + width)) + B
    
    return t, y




