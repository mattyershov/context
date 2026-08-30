import sys
import json
import serial
from PySide6.QtCore import QObject, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

class RadioWorker(QObject):
    vfoAFreq = Signal(str)
    vfoBFreq = Signal(str)

    rxFocus = Signal(str) # A or B
    txFocus = Signal(str)
    
    def __init__(self, port, baud):
        super().__init__()
        self.port = port
        self.baud = baud


    def run(self):
        
        def parse(cmd):   
            match cmd[:2]:
                case "FA":
                    freqA = int(buffer[2:])
                    self.vfoAFreq.emit(f"{freq / 1e3:.3f}")
                
                case "FB":
                    freqB = int(buffer[2:])
                    self.vfoBFreq.emit(f"{freq / 1e3:.3f}")

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

        ser = serial.Serial(self.port, self.baud, timeout=1)
        ser.write(b"AI1;") 

        buffer = ""
        while True:
            char = ser.read().decode('ascii', errors='ignore')
            if char == ";":
                self.parse(buffer)
            else:
                buffer += char

        



class RadioBackend(QObject):
    freqAChanged = Signal(str)
    freqBChanged = Signal(str)
    rxFocusChanged = Signal(str)
    txFocusChanged = Signal(str)

    def __init__(self, port="dev/ttyUSB0", baud=115200):
        super().__init__()
        self._freqA = "NaN"
        self._freqB = "NaN"
        self._rxFocus = "N"
        self._txFocus = "N"

        self.thread = QThread()
        self.worker = RadioWorker(port, baud)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.vfoAFreq.connect(self.setVfoA)
        self.worker.vfoBFreq.connect(self.setVfoB)
        self.worker.rxFocus.connect(self.setRxFocus)
        self.worker.txFocus.connect(self.setTxFocus)

        self.thread.start()

    def getVfoA(self):
        return self._freqA
    
    def getVfoB(self):
        return self._freqB

    def getRxFocus(self):
        return self._rxFocus

    def getTxFocus(self):
        return self._txFocus
    
    def setVfoA(self, newFreq):
        if self._freqA != newFreq:
            self._freqA = newFreq
            self.freqAChanged.emit(self._freqA)

    def setVfoB(self, newFreq):
        if self._freqB != newFreq:
            self._freqB = newFreq
            self.freqBChanged.emit(self._freqB)

    def setRxFocus(self, newRxFocus):
        if self._rxFocus != newRxFocus:
            self._rxFocus = newRxFocus
            self.rxFocusChanged.emit(_rxFocus)

    def setTxFocus(self, newTxFocus):
        if self._txFocus != newTxFocus:
            self._txFocus = newTxFocus
            self.txFocusChanged.emit(_txFocus)

    freqA = Property(str, getVfoA, setVfoA, notify=freqAChanged)
    freqB = Property(str, getVfoB, setVfoB, notify=freqBChanged)
    rxFocus = Property(str, getRxFocus, setRxFocus, notify=rxFocusChanged)
    txFocus = Property(str, getTxFocus, setTxFocus, notify=txFocusChanged)



app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

with open('station.json', 'r') as file:
    stnConfig = json.load(file)
    # port = stnConfig.get("port", "/dev/ttyUSB0") #TODO: make these fit the actual JSON structure
    # baud = stnConfig.get("baud", 115200)

    port = "/dev/ttyUSB0"
    baud = 115200

radio = RadioBackend(port=port, baud=baud)
engine.rootContext().setContextProperty("radio", radio)


engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())