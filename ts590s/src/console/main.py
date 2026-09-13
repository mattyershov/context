import sys
import json
import serial
from evdev import InputDevice, list_devices, ecodes
import threading
from PySide6.QtCore import QObject, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class RadioWorker(QObject):

    vfo_a_freq = Signal(str)
    vfo_b_freq = Signal(str)

    rx_focus = Signal(str)  # {A, B}
    tx_focus = Signal(str)  # {A, B}

    key_speed = Signal(str)
    vfo_a_fil = Signal(str)  # {A, B}
    vfo_b_fil = Signal(str)  # {A, B}
    nr_status = Signal(int)  # {0, 1, 2} (NR is independent of VFO focus)

    def __init__(self, port, baud):
        super().__init__()
        self.port = port
        self.baud = baud
        self.ser = None
        self._lock = threading.Lock()

    def send_cmd(self, cmd):
        if self.ser and self.ser.is_open:
            if not cmd.endswith(";"):
                cmd += ";"
            with self._lock:
                ser.write(cmd.encode("ascii"))


    def parse(self, buffer):
        match buffer[:2]:
            case "FA":  # VFO A freq
                freq_a = float(buffer[2:])
                self.vfo_a_freq.emit(f"{freq_a / 1e3:.3f}")

            case "FB":  # VFO B freq
                freq_b = float(buffer[2:])
                self.vfo_b_freq.emit(f"{freq_b / 1e3:.3f}")

            case "FR":  # RX VFO
                if int(buffer[2:]) == 0:
                    self.rx_focus.emit("A")
                elif int(buffer[2:]) == 1:
                    self.rx_focus.emit("B")

            case "FT":  # TX VFO
                if int(buffer[2:]) == 0:
                    self.tx_focus.emit("A")
                elif int(buffer[2:]) == 1:
                    self.tx_focus.emit("B")

            case "KS":  # Key speed
                self.key_speed.emit(str(buffer[2:]).lstrip("0"))

            case "NR":  # Noise Reduction status
                if int(buffer[2:]) == 0:
                    self.nr_status.emit(0)
                elif int(buffer[2:]) == 1:
                    self.nr_status.emit(1)

            case _:
                pass

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            with self._lock:
                self.ser.write(b"AI2;")

            while True:
                with self._lock:
                    byte_cmd = self.ser.read_until(b";")
                    if byte_cmd.endswith(b";"):
                        cmd_ascii = byte_cmd[:-1].decode('ascii', errors="ignore")
                        if cmd_ascii:
                            self.parse(cmd_ascii)
        except Exception as e:
            print(f"Radio Serial Error: {e}")


class ShuttleProWorker(QObject):  # Fixed base class typo Qobject -> QObject

    jog_moved = Signal(int)         # {-1, +1} (relative)
    shuttle_moved = Signal(int)     # [-7, +7] (absolute)
    button_pressed = Signal(list)    # [Button ID (0 thru 14), status (1=pressed, 0=released)]

    def __init__(self, spv2_path="/dev/input/by-id/usb-Contour_Design_ShuttlePRO_v2-event-mouse"):
        super().__init__()
        self.spv2_path = spv2_path  # TODO: load from JSON or use list_devices()
        self._last_jog_pos = None

    @staticmethod
    def _to_signed_8bit(val):
        """Converts Linux evdev unsigned 8-bit byte (0..255) to signed int (-128..127)."""
        return val - 256 if val > 127 else val

    def run(self):
        if not self.spv2_path:
            return

        try:
            spv2 = InputDevice(self.spv2_path)
            spv2.grab()

            for event in spv2.read_loop():
                if event.type == ecodes.EV_REL and event.code == ecodes.REL_DIAL:
                    delta = self._to_signed_8bit(event.value)
                    if delta != 0:
                        self.jog_moved.emit(event.value)

                elif event.type == ecodes.EV_ABS and event.code in (ecodes.ABS_DIAL, ecodes.REL_DIAL):
                    current_pos = event.value

                    if self._last_jog_pos != None:

                        delta = self._to_signed_8bit((curr - self._last_jog_pos) & 0xFF)
                        if delta != 0:
                            self.jog_moved.emit(delta)

                    self._last_jog_pos = current_pos

                # Shuttle abs position
                elif event.type == ecodes.EV_ABS and event.code == ecodes.ABS_THROTTLE:
                    self.shuttle_moved.emit(event.value)

                elif event.type == ecodes.EV_KEY:
                    btn_idx = event.code - ecodes.BTN_TRIGGER_HAPPY1
                    if 0 <= btn_idx <= 14:
                        if event.value == 1:
                            self.button_pressed.emit([btn_idx, 1])
                        elif event.value == 0:
                            self.button_pressed.emit([btn_idx, 0])
        except Exception as e:
            print(f"ShuttlePro Error: {e}")


class RadioBackend(QObject):
    freq_a_changed = Signal(str)
    freq_b_changed = Signal(str)
    rx_focus_changed = Signal(str)
    tx_focus_changed = Signal(str)
    key_speed_changed = Signal(str)
    nr_status_changed = Signal(int)
    send_cat_cmd = Signal(str)

    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        super().__init__()
        self._freq_a = "00000.000"
        self._freq_b = "00000.000"
        self._rx_focus = "N"
        self._tx_focus = "N"
        self._key_speed = "N"
        self._nr_status = 0

        self.radio_thread = QThread()
        self.shuttlepro_thread = QThread()

        self.radio_worker = RadioWorker(port, baud)
        self.shuttlepro_worker = ShuttleProWorker()

        self.radio_worker.moveToThread(self.radio_thread)
        self.shuttlepro_worker.moveToThread(self.shuttlepro_thread)


        self.radio_thread.started.connect(self.radio_worker.run)
        self.shuttlepro_thread.started.connect(self.shuttlepro_worker.run)


        self.radio_worker.vfo_a_freq.connect(self.set_vfo_a)
        self.radio_worker.vfo_b_freq.connect(self.set_vfo_b)
        self.radio_worker.rx_focus.connect(self.set_rx_focus)
        self.radio_worker.tx_focus.connect(self.set_tx_focus)
        self.radio_worker.key_speed.connect(self.set_key_speed)
        self.radio_worker.nr_status.connect(self.set_nr_status)

        self.shuttlepro_worker.jog_moved.connect(self.handle_jog)
        self.shuttlepro_worker.shuttle_moved.connect(self.handle_shuttle)
        self.shuttlepro_worker.button_pressed.connect(self.handle_button)

        self.send_cat_cmd.connect(self.radio_worker.send_cmd)

        self.radio_thread.start()
        self.shuttlepro_thread.start() 

    def get_vfo_a(self):
        return self._freq_a

    def get_vfo_b(self):
        return self._freq_b

    def get_rx_focus(self):
        return self._rx_focus

    def get_tx_focus(self):
        return self._tx_focus

    def get_key_speed(self):
        return self._key_speed

    def get_nr_status(self):
        return self._nr_status

    def set_vfo_a(self, new_freq):
        if self._freq_a != new_freq:
            self._freq_a = new_freq
            self.freq_a_changed.emit(self._freq_a)

    def set_vfo_b(self, new_freq):
        if self._freq_b != new_freq:
            self._freq_b = new_freq
            self.freq_b_changed.emit(self._freq_b)


    def set_rx_focus(self, new_rx_focus):
        if self._rx_focus != new_rx_focus:
            self._rx_focus = new_rx_focus
            self.rx_focus_changed.emit(self._rx_focus)

    def set_tx_focus(self, new_tx_focus):
        if self._tx_focus != new_tx_focus:
            self._tx_focus = new_tx_focus
            self.tx_focus_changed.emit(self._tx_focus)

    def set_key_speed(self, new_key_speed):
        if self._key_speed != new_key_speed:
            self._key_speed = new_key_speed
            self.key_speed_changed.emit(self._key_speed)

    def set_nr_status(self, new_nr_status):
        if self._nr_status != new_nr_status:
            self._nr_status = new_nr_status
            self.nr_status_changed.emit(self._nr_status)

    def send_cmd(self, cmd):
        self.send_cmd.emit(cmd)

    def handle_jog(self, step):
        tuning_step = 50 # 50 Hz
        
        #TODO: Add a setting to set the mode of the shuttle and jog (main or opposite VFO)
        if self.get_rx_focus() == "A":
            print(step)
            self.set_vfo_b(str(float(self._freq_b) + float(step * tuning_step)))
        elif self.get_rx_focus() == "B":
            self.set_vfo_a(str(float(self._freq_a) + float(step * tuning_step)))

    def handle_shuttle(self, pos):
        if pos == 0:
            return
        elif pos > 0:
            accel_rate = pos ** 2 * 500
        elif pos < 0:
            accel_rate = -(pos ** 2) * 500

        if self.get_rx_focus() == "A":
            self.set_vfo_b(str(float(self._freq_b) + float(accel_rate)))
        elif self.get_rx_focus() == "B":
            self.set_vfo_a(str(float(self._freq_a) + float(accel_rate)))

    def handle_button(self, button):
        id, status = button[0], button[1]
        match id:
            case 4:
                # Swap A and B
                if status == 1:
                    self.send_cmd("SW")
                    print("swap")

            case _:
                return

    freq_a = Property(str, get_vfo_a, set_vfo_a, notify=freq_a_changed)
    freq_b = Property(str, get_vfo_b, set_vfo_b, notify=freq_b_changed)
    rx_focus = Property(str, get_rx_focus, set_rx_focus, notify=rx_focus_changed)
    tx_focus = Property(str, get_tx_focus, set_tx_focus, notify=tx_focus_changed)
    key_speed = Property(str, get_key_speed, set_key_speed, notify=key_speed_changed)
    nr_status = Property(int, get_nr_status, set_nr_status, notify=nr_status_changed)


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

try:
    with open('station.json', 'r') as file:
        stn_config = json.load(file)
        port = stn_config.get("port", "/dev/ttyUSB0")
        baud = stn_config.get("baud", 115200)
except (FileNotFoundError, json.JSONDecodeError):
    port, baud = "/dev/ttyUSB0", 115200

radio = RadioBackend(port=port, baud=baud)
engine.rootContext().setContextProperty("radio", radio)

engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())