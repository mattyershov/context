import sys
import json
import serial
from PySide6.QtCore import QObject, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

class RadioWorker(QObject):
    vfoAChanged = Signal(str)
    vfoBChanged = Signal(str)

    rxFocus = Signal(str) # A or B
    txFocus = Signal(str)
    
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud


    def run(self):
        ser = serial.Serial(self.port, self.baud, timeout=1)
        ser.write(b"AI1;") 

        buffer = ""
        while True:
            char = ser.read().decode('ascii', errors='ignore')
            if char == ";":
                self.parse(buffer)
            else:
                buffer += char

            match cmd.startswith():
                case "FA":
                    freqA = int(buffer[2:])
                    self.vfoAChanged.emit(f"{freq / 1e3:.3f}")
                
                case "FB":
                    freqB = int(buffer[2:])
                    self.vfoBChanged.emit(f"{freq / 1e3:.3f}")

                case "FR":
                    if int(buffer[2:]) == 0:
                        self.rxFocus.emit("A")
                    elif int(buffer[2:]) == 1:
                        self.rxFocus.emit("B")
                
                case "FT":
                    if int(buffer[2:]) == 0:
                        self.txFocus.emit("A")
                    elif int(buffer[2:]) == 1:
                        self.txFocus.emit("B")
                

                case _:
                    pass



class RadioBackend(QObject):
    freqAChanged = Signal(str)
    freqBChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._freqA = "NaN"
        self._freqB = "NaN"

        self.thread = QThread()
        self.worker = RadioWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.vfoAChanged.connect(self.setVfoA)
        self.worker.vfoBChanged.connect(self.setVfoB)

        self.thread.start()

    def getVfoA(self):
        return self._freqA
    
    def getVfoB(self):
        return self._freqB
    
    def setVfoA(self, newFreq):
        if self._freqA != newFreq:
            self._freqA = newFreq
            self.freqAChanged.emit(self._freqA)

    def setVfoB(self, newFreq):
        if self._freqB != newFreq:
            self._freqB = newFreq
            self.freqBChanged.emit(self._freqB)

    freqA = Property(str, getVfoA, setVfoA, notify=freqAChanged)
    freqB = Property(str, getVfoB, setVfoB, notify=freqBChanged)


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

with open('station.json', 'r') as file:
    stnConfig = json.load(file)
    port = stnConfig.get("port", "/dev/ttyUSB0") #TODO: make these fit the actual JSON structure
    baud = stnConfig.get("baud", 115200)

radio = RadioBackend(port=port, baud=baud)
engine.rootContext().setContextProperty("radio", radio)


engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())