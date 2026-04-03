from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QDoubleSpinBox,QHBoxLayout
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signals import sin, rectangle, triangle, sawtooth, invsawtooth, pulse

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

        #Spectrum Plot
        self.fig2=Figure(figsize=(5, 4), dpi=100)
        self.canvas2=FigureCanvas(self.fig2)
        self.ax2 = self.fig2.add_subplot(111)
        self.spectrum_layout.addWidget(self.canvas2)

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
        self.fs.setValue(100)
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



    def update_plot(self):
        self.ax.clear()
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
            t, y = sin(a, b, phi, start, stop, fs, f)
        elif(type=="Rectangle"):
            t, y = rectangle(a,b,phi,duty,start,stop,fs,f)
        elif(type=="Triangle"):
            t, y = triangle(a,b,phi,start,stop,fs,f)
        elif(type=="Sawtooth"):
            t, y = sawtooth(a,b,phi,start,stop,fs,f)
        elif(type=="Inverse Sawtooth"):
            t, y = invsawtooth(a,b,phi,start,stop,fs,f)
        elif(type=="Pulse"):
            t, y = pulse(a,b,start_pulse,width,start,stop,fs)
       
        
        self.ax.plot(t, y)
        self.ax.set_title(f"Time plot: {type}")
        self.ax.set_ylabel("Voltage [V]")
        self.ax.set_xlabel("Time [s]")
        self.ax.grid(True)
        self.canvas.draw()




