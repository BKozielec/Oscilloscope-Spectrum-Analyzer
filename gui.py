from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QDoubleSpinBox
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
        self.layout = QVBoxLayout(self.main_widget)
        
        self.fig=Figure(figsize=(5, 4), dpi=100)
        self.canvas=FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.layout.addWidget(self.canvas)

        self.btn = QPushButton("Generate signal")
        self.btn.clicked.connect(self.update_plot)
        self.layout.addWidget(self.btn)

        self.signaltype=QComboBox()
        signals=["Sinusoid","Rectangle","Triangle","Sawtooth","Inverse Sawtooth", "Pulse"]
        self.signaltype.addItems(signals)
        self.layout.addWidget(self.signaltype)


        self.A=QDoubleSpinBox()
        self.A.setRange(0, 10)
        self.A.setValue(1.0)
        self.A.setPrefix("Magnitude [V]: ")
        self.layout.addWidget(self.A)
        
        self.B=QDoubleSpinBox()
        self.B.setRange(0, 10)
        self.B.setValue(0)
        self.B.setPrefix("Offset [V]: ")
        self.layout.addWidget(self.B)
        
        
        self.phi=QDoubleSpinBox()
        self.phi.setRange(0, 100)
        self.phi.setValue(0)
        self.phi.setPrefix("Phase [rad]: ")
        self.layout.addWidget(self.phi)
       
        self.start=QDoubleSpinBox()
        self.start.setRange(0, 100)
        self.start.setValue(0)
        self.start.setPrefix("Start [s]: ")
        self.layout.addWidget(self.start)
        
        self.stop=QDoubleSpinBox()
        self.stop.setRange(0, 100)
        self.stop.setValue(1)
        self.stop.setPrefix("Stop [s]: ")
        self.layout.addWidget(self.stop)
        
        self.f=QDoubleSpinBox()
        self.f.setRange(0, 1000)
        self.f.setValue(10.0)
        self.f.setPrefix("Frequency [V]: ")
        self.layout.addWidget(self.f)
        
        self.fs=QDoubleSpinBox()
        self.fs.setRange(0, 1000)
        self.fs.setValue(100)
        self.fs.setPrefix("Sampling rate: ")
        self.layout.addWidget(self.fs)

        self.duty=QDoubleSpinBox()
        self.duty.setRange(0,1)
        self.duty.setValue(0.5)
        self.duty.setPrefix("Duty (rectangle): ")
        self.layout.addWidget(self.duty)

        self.start_pulse=QDoubleSpinBox()
        self.start_pulse.setRange(0,10)
        self.start_pulse.setValue(0.5)
        self.start_pulse.setPrefix("Start pulse (pulse): ")
        self.layout.addWidget(self.start_pulse)
        
        self.width=QDoubleSpinBox()
        self.width.setRange(0,10)
        self.width.setValue(0.25)
        self.width.setPrefix("Width (pulse): ")
        self.layout.addWidget(self.width)
            




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




