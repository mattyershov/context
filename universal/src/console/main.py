import sys
import json
import hamlib
from PySide6.QtCore import QObject, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

class RadioBackend(QObject):
    freqChanged = Signal(float)

    def __init__(self):
        super().__init__()
        self._freq = 14200
    
    def getFrequency(self):
        return self._freq
    
    def setFrequency(self, newFreq):
        if newFreq != self._freq:
            self._freq = newFreq
            self.freqChanged.emit(self._freq)
        
    freq = Property(float, getFrequency, setFrequency, notify=freqChanged)



def main():
    with open('station.json', 'r') as file:
        station_list = json.load(file)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()