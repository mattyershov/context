import sys
import json
import hamlib
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

def main():
    with open('station.json', 'r') as file:
        station_list = json.load(file)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)


    sys.exit(app.exec())

if __name__ == "__main__":
    main()