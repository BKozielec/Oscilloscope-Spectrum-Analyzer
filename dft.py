import numpy as np

def calculate_dft_mgn(t,x):
    N=len(x)
    dt=t[1]-t[0]
    X_raw=np.fft.fft(x)
    f_raw=np.fft.fftfreq(N,d=dt)
    half=N//2
    f = f_raw[:half]
    X = np.abs(X_raw[:half]) * 2 / N

    return f, X


def calculate_dft_phase(t,x):
    N=len(x)
    dt=t[1]-t[0]
    X_raw=np.fft.fft(x)
    f_raw=np.fft.fftfreq(N,d=dt)
    half=N//2
    f = f_raw[:half]
    X = X_raw[:half]

    magnitude = np.abs(X) * 2 / N
    phase = np.angle(X)
    phase[magnitude < 0.05] = 0
    



    return f, phase