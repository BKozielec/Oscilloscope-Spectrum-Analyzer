import pyaudio
import numpy as np

class AudioRecorder:
    def __init__(self, rate=44100, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def get_frame(self):
        raw_data = self.stream.read(self.chunk, exception_on_overflow=False)
        
        samples = np.frombuffer(raw_data, dtype=np.int16)
        
        x = samples / 32768.0
        
        t = np.linspace(0, self.chunk / self.rate, self.chunk)
        
        return t, x

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()