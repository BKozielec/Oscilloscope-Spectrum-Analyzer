from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QDoubleSpinBox,QHBoxLayout
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signals import sin, rectangle, triangle, sawtooth, invsawtooth, pulse
from dft import calculate_dft_mgn,calculate_dft_phase
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import MultiCursor
from audio import AudioRecorder
import numpy as np
from PyQt6.QtCore import QTimer

class OscilloscopeGUI(QMainWindow):
    def __init__ (self):
        super().__init__()
        
        self.setWindowTitle("Osciloscope/Spectrum Analyzer")
        self.main_widget=QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.main_layout=QVBoxLayout(self.main_widget)

        self.layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.spectrum_layout = QVBoxLayout()
        
        #Time domain plot
        self.fig=Figure(figsize=(5, 4), dpi=100)
        self.canvas=FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.right_layout.addWidget(self.canvas)
        self.toolbar1 = NavigationToolbar(self.canvas, self)
        self.right_layout.addWidget(self.toolbar1)

        #Spectrum Plot
        self.fig2=Figure(figsize=(5, 4), dpi=100)
        self.canvas2=FigureCanvas(self.fig2)
        self.ax2 = self.fig2.add_subplot(111)
        self.spectrum_layout.addWidget(self.canvas2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        self.spectrum_layout.addWidget(self.toolbar2)

        #Spectrum Plot
        self.fig3=Figure(figsize=(5, 4), dpi=100)
        self.canvas3=FigureCanvas(self.fig3)
        self.ax3 = self.fig3.add_subplot(111)
        self.spectrum_layout.addWidget(self.canvas3)
        self.toolbar3 = NavigationToolbar(self.canvas3, self)
        self.spectrum_layout.addWidget(self.toolbar3)

        #Cursors 
        self.multi = MultiCursor(self.canvas, (self.ax, self.ax2, self.ax3), color='r', lw=1, useblit=True)

        self.signaltype=QComboBox()
        signals=["Sinusoid","Rectangle","Triangle","Sawtooth","Inverse Sawtooth", "Pulse"]
        self.signaltype.addItems(signals)
        self.left_layout.addWidget(self.signaltype)

        self.A=QDoubleSpinBox()
        self.A.setRange(0, 10)
        self.A.setValue(1.0)
        self.A.setPrefix("Magnitude [V]: ")
        self.left_layout.addWidget(self.A)
        
        self.B=QDoubleSpinBox()
        self.B.setRange(0, 10)
        self.B.setValue(0)
        self.B.setPrefix("Offset [V]: ")
        self.left_layout.addWidget(self.B)
        
        
        self.phi=QDoubleSpinBox()
        self.phi.setRange(0, 100)
        self.phi.setValue(0)
        self.phi.setPrefix("Phase [rad]: ")
        self.left_layout.addWidget(self.phi)
       
        self.start=QDoubleSpinBox()
        self.start.setRange(0, 100)
        self.start.setValue(0)
        self.start.setPrefix("Start [s]: ")
        self.left_layout.addWidget(self.start)
        
        self.stop=QDoubleSpinBox()
        self.stop.setRange(0, 100)
        self.stop.setValue(1)
        self.stop.setPrefix("Stop [s]: ")
        self.left_layout.addWidget(self.stop)
        
        self.f=QDoubleSpinBox()
        self.f.setRange(0, 1000)
        self.f.setValue(10.0)
        self.f.setPrefix("Frequency [V]: ")
        self.left_layout.addWidget(self.f)
        
        self.fs=QDoubleSpinBox()
        self.fs.setRange(0, 1000)
        self.fs.setValue(1000)
        self.fs.setPrefix("Sampling rate: ")
        self.left_layout.addWidget(self.fs)

        self.duty=QDoubleSpinBox()
        self.duty.setRange(0,1)
        self.duty.setValue(0.5)
        self.duty.setPrefix("Duty (rectangle): ")
        self.left_layout.addWidget(self.duty)

        self.start_pulse=QDoubleSpinBox()
        self.start_pulse.setRange(0,10)
        self.start_pulse.setValue(0.5)
        self.start_pulse.setPrefix("Start pulse (pulse): ")
        self.left_layout.addWidget(self.start_pulse)
        
        self.width=QDoubleSpinBox()
        self.width.setRange(0,10)
        self.width.setValue(0.25)
        self.width.setPrefix("Width (pulse): ")
        self.left_layout.addWidget(self.width)

        self.layout.addLayout(self.left_layout,1)
        self.layout.addLayout(self.right_layout,4)
        self.layout.addLayout(self.spectrum_layout,4)
        self.main_layout.addLayout(self.layout)
        
        self.btn = QPushButton("Generate signal")
        self.btn.clicked.connect(self.update_plot)
        self.main_layout.addWidget(self.btn)


        #Tool bars
        self.toolbar1 = NavigationToolbar(self.canvas, self)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        self.toolbar3 = NavigationToolbar(self.canvas3, self)



    def update_plot(self):
        self.ax.clear()
        self.ax2.clear()
        self.ax3.clear()
        type = self.signaltype.currentText()

        a = self.A.value()
        b= self.B.value()
        phi=self.phi.value()
        start=self.start.value()
        stop=self.stop.value()
        f=self.f.value()
        fs = self.fs.value()
        duty=self.duty.value()
        start_pulse=self.start_pulse.value()
        width=self.width.value()



        if(type=="Sinusoid"):
            t, x = sin(a, b, phi, start, stop, fs, f)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Rectangle"):
            t, x = rectangle(a,b,phi,duty,start,stop,fs,f)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Triangle"):
            t, x = triangle(a,b,phi,start,stop,fs,f)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Sawtooth"):
            t, x = sawtooth(a,b,phi,start,stop,fs,f)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Inverse Sawtooth"):
            t, x = invsawtooth(a,b,phi,start,stop,fs,f)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Pulse"):
            t, x = pulse(a,b,start_pulse,width,start,stop,fs)
            f, X = calculate_dft_mgn(t,x)
            f,pha = calculate_dft_phase(t,x)
        elif(type=="Real time audio"):
            print("Audio")
        
        self.ax.plot(t, x)
        self.ax.set_title(f"Time plot: {type}")
        self.ax.set_ylabel("Voltage [V]")
        self.ax.set_xlabel("Time [s]")
        self.ax.grid(True)
        self.canvas.draw()

        self.ax2.plot(f, X)
        self.ax2.set_title(f"Spectrum plot Magnitude: {type}")
        self.ax2.set_ylabel("Voltage [V]")
        self.ax2.set_xlabel("Frequnecy [Hz]")
        self.ax2.grid(True)
        self.canvas2.draw()

        self.ax3.plot(f, pha)
        self.ax3.set_title(f"Spectrum plot Phase: {type}")
        self.ax3.set_ylabel("Angle [rad]")
        self.ax3.set_xlabel("Frequnecy [Hz]")
        self.ax3.grid(True)
        self.canvas3.draw()


class Launcher (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select mode")
        self.layout = QVBoxLayout()

        self.btn_sim=QPushButton("Simulation mode")
        self.btn_sim.clicked.connect(self.open_simulation)
        self.layout.addWidget(self.btn_sim)

        self.btn_audio=QPushButton("Audio mode")
        self.btn_audio.clicked.connect(self.open_audio)
        self.layout.addWidget(self.btn_audio)

        self.setLayout(self.layout)
        self.sim_window=None
        self.audio_window=None

    def open_simulation(self):
        self.sim_window=OscilloscopeGUI()
        self.sim_window.show()
        self.close()

    def open_audio(self):
        print("Audio")
        self.audio_window=AudioWindow()
        self.audio_window.show()
        self.close()


        




class AudioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Audio")
        self.setMinimumSize(400, 300)

        self.main_widget=QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout=QVBoxLayout(self.main_widget)

        self.fig = Figure(figsize=(5, 8))
        self.canvas = FigureCanvas(self.fig)
        self.ax_time = self.fig.add_subplot(311)  
        self.ax_spec = self.fig.add_subplot(312)  
        self.ax_phase = self.fig.add_subplot(313) 
        self.layout.addWidget(self.canvas)

        
        self.recorder = AudioRecorder(rate=44100, chunk=1024)
        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  


    def update_frame(self):
        t, x = self.recorder.get_frame() 
        x = x - np.mean(x)
        
        
        f, X_mgn = calculate_dft_mgn(t, x)
        f_pha, X_pha = calculate_dft_phase(t, x) 

        self.ax_time.clear()
        self.ax_spec.clear()
        self.ax_phase.clear() 
        
       
        self.ax_time.plot(t, x, color='blue')
        self.ax_time.set_ylim(-0.5, 0.5) 
        
        
        self.ax_spec.plot(f, X_mgn, color='red')
        self.ax_spec.set_xlim(0, 5000) 
        
      
        self.ax_phase.plot(f_pha, X_pha, color='green') 
        self.ax_phase.set_xlim(0, 5000)
        self.ax_phase.set_ylim(-np.pi, np.pi)
        
        self.canvas.draw_idle()
    def closeEvent(self, event):
        self.timer.stop()
        self.recorder.close()
        event.accept()






        