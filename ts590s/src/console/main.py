import sys
import json
import serial
from evdev import InputDevice, list_devices, ecodes
import threading
import time
from PySide6.QtCore import QObject, Signal, Property, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

class RadioWorker(QObject):

    vfo_a_freq = Signal(str)
    vfo_b_freq = Signal(str)

    rx_focus = Signal(str)  # {A, B}
    tx_focus = Signal(str)  # {A, B}

    vfo_a_fil = Signal(str)  # {A, B}
    vfo_b_fil = Signal(str)  # {A, B}
    nr_status = Signal(int)  # {0, 1, 2} (NR is independent of VFO focus)
    mode = Signal(str)

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
                self.ser.write(cmd.encode("ascii"))


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

            case "NR":  # Noise Reduction status
                self.nr_status.emit(int(buffer[2:]))
            
            case "MD": # Mode (differentiation of VFO A vs. B happens later, in RadioBackend)
                mode = ""
                match int(buffer[2:]):
                    case 1:
                        mode = "LSB"
                    case 2:
                        mode = "USB"
                    case 3:
                        mode = "CW"
                    case 7:
                        mode = "CW-R"
                    case _:
                        mode = "N"
                self.mode.emit(mode)
            case _:
                pass

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            with self._lock:
                self.ser.write(b"AI2;")

            while True:
                if self.ser.in_waiting > 0:
                    with self._lock:
                        byte_cmd = self.ser.read_until(b";")
                    if byte_cmd.endswith(b";"):
                        cmd_ascii = byte_cmd[:-1].decode('ascii', errors="ignore")
                        if cmd_ascii:
                            self.parse(cmd_ascii)
                else:
                    time.sleep(0.05)
        except Exception as e:
            print(f"Radio Serial Error: {e}")


class ShuttleProWorker(QObject):

    jog_moved = Signal(int)         # {-1, +1} (relative)
    # shuttle_moved = Signal(int)     # [-7, +7] (absolute)
    button_pressed = Signal(list)    # [Button ID (0 thru 14), status (1=pressed, 0=released)]

    def __init__(self):
        super().__init__()

        self.spv2_path = config.get("shuttleprov2", {}).get("port", "/dev/input/by-id/usb-Contour_Design_ShuttlePRO_v2-event-mouse")
        self._last_jog_pos = None
        self.delta = None

    @staticmethod
    def _to_signed_8bit(val):
        """Converts evdev unsigned 8-bit byte (0..255) to signed int (-128..127)."""
        return val - 256 if val > 127 else val

    def run(self):
        if not self.spv2_path:
            return
        try:
            spv2 = InputDevice(self.spv2_path)
            spv2.grab()

            for event in spv2.read_loop():
                
                # Jog
                if event.type == ecodes.EV_REL and event.code == ecodes.REL_DIAL:
                    current_pos = event.value

                    if self._last_jog_pos != None:
                        self.delta = self._to_signed_8bit((current_pos - self._last_jog_pos) & 0xFF)
                        if self.delta != 0:
                            self.jog_moved.emit(self.delta)
                            print(self.delta)

                    self._last_jog_pos = current_pos

                # Shuttle
                # elif event.type == ecodes.EV_REL and event.code == ecodes.REL_WHEEL:
                #     self.shuttle_moved.emit(event.value)

                elif event.type == ecodes.EV_KEY:
                    btn_idx = event.code
                    if 256 <= btn_idx <= 270:
                        if event.value == 1:
                            self.button_pressed.emit([btn_idx, 1])
                            print([btn_idx, 1])
                        elif event.value == 0:
                            self.button_pressed.emit([btn_idx, 0])
                            print([btn_idx, 0])
        except Exception as e:
            print(f"ShuttlePro Error: {e}")


class RadioBackend(QObject):
    freq_a_changed = Signal(str)
    freq_b_changed = Signal(str)
    rx_focus_changed = Signal(str)
    tx_focus_changed = Signal(str)
    nr_status_changed = Signal(int)
    mode_a_changed = Signal(str)
    mode_b_changed = Signal(str)
    send_cat_cmd = Signal(str)

    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        super().__init__()
        self._freq_a = "00000.000"
        self._freq_b = "00000.000"
        self._rx_focus = "N"
        self._tx_focus = "N"
        self._nr_status = 0
        self._mode_a = "CW"
        self._mode_b = "CW"

        self._split_count = 1

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
        self.radio_worker.nr_status.connect(self.set_nr_status)
        self.radio_worker.mode.connect(self.set_mode)

        self.shuttlepro_worker.jog_moved.connect(self.handle_jog)
        # self.shuttlepro_worker.shuttle_moved.connect(self.handle_shuttle)
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

    def get_nr_status(self):
        return self._nr_status

    def get_mode_a(self):
        return self._mode_a

    def get_mode_b(self):
        return self._mode_b

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

    def set_nr_status(self, new_nr_status):
        if self._nr_status != new_nr_status:
            self._nr_status = new_nr_status
            self.nr_status_changed.emit(self._nr_status)
    
    def set_mode(self, new_mode):
        if self._rx_focus == "A":
            if self._mode_a != new_mode:
                self._mode_a = new_mode
                self.mode_a_changed.emit(self.mode_a)

        elif self._rx_focus == "B":
            if self._mode_b != new_mode:
                self._mode_b = new_mode
                self.mode_b_changed.emit(self.mode_b)
        

    def send_cmd(self, cmd):
        self.radio_worker.send_cmd(cmd)

    def handle_jog(self, jog_step):
        tuning_step = 0.01 # 10 Hz
        target_vfo = None
        new_freq = None
        
        if self._rx_focus == "A":
            new_freq = round((float(self._freq_a)) + float(tuning_step * jog_step), 3)

            self.set_vfo_a(f"{new_freq:.3f}")
            self.send_cmd(f"FA{int(new_freq * 1000):011d}")
            print(f"{int(new_freq * 1000):011d}")

        elif self._rx_focus == "B":
            new_freq = round((float(self._freq_b)) + float(tuning_step * jog_step), 3)

            self.set_vfo_b(f"{new_freq:.3f}")
            self.send_cmd(f"FB{int(new_freq * 1000):011d}")
            print(f"{int(new_freq * 1000):011d}")

    def split_macro(self, status):
        if status == 1:
            # Assuming running on B and S&Ping on A
            self.send_cmd("FR0;FT1") # Turn on split to listen to unidentified signal while maintaining run freq
        elif status == 2:
            self.send_cmd("FR0") # Then, set TX and RX to A to work mult
        elif status == 3:
            self.send_cmd("FR1") # Cancel split if someone responds to your CQ call


    # Shuttle (currently not in use; may not be practical):

    # def handle_shuttle(self, pos):
    #     new_freq = None

    #     if pos == 0:
    #         return
    #     elif pos > 0:
    #         accel_rate = pos ** 2
    #     elif pos < 0:
    #         accel_rate = -(pos ** 2)

    #     if self.get_rx_focus() == "A":
    #         new_freq = round((float(self._freq_a)) + float(accel_rate), 3)
    #         self.set_vfo_a(f"{new_freq:.3f}")
    #         self.send_cmd(f"FA{int(new_freq * 1000):011d}")
    #         print(f"{int(new_freq * 1000):011d}")

    #     elif self.get_rx_focus() == "B":
    #         new_freq = round((float(self._freq_b)) + float(accel_rate), 3)
    #         self.set_vfo_b(f"{new_freq:.3f}")
    #         self.send_cmd(f"FA{int(new_freq * 1000):011d}")
    #         print(f"{int(new_freq * 1000):011d}")


    def handle_button(self, button):
        id, status = button[0], button[1]

        match id:

            case 260:
                # Swap A and B
                if status == 1:
                    temp_freq_b = float(self._freq_b)
                    self.send_cmd(f"FB{int(float(self._freq_a) * 1000):011d}")
                    self.send_cmd(f"FA{int(temp_freq_b * 1000):011d}")
                    print("swap")

            case 261:
                # Throw A
                if status == 1:
                    self.send_cmd("FR0")
                    self._split_count = 0
            
            case 263:
                # Throw B
                if status == 1:
                    self.send_cmd("FR1")
                    self._split_count = 0

            case 262:
                # Noise reduction mode TODO: fix toggle logic
                if status == 1:
                    self.send_cmd(f"NR{(self.nr_status + 1) % 3}")
                    
            case 268:
                # TF-SET
                self.send_cmd(f"TS{status}")

            case 266:
                # Split Macro stages
                if status == 1:
                    if self._split_count > 3:
                        self._split_count = 1
                    self.split_macro(self._split_count)
                    print(self._split_count)
                    self._split_count += 1

            case 264:
                # Cancel Split Macro
                if status == 1:
                    self.split_macro(3)
                    self._split_count = 1
                    
            case 270:
                # CW/CW-R
                if status == 1:

                    if self.get_rx_focus() == "A":
                        if self._mode_a == "CW":
                            self.send_cmd("MD7")
                            print("MD7")
                        elif self._mode_a == "CW-R":
                            self.send_cmd("MD3")

                    elif self.get_rx_focus() == "B":
                        if self._mode_b == "CW":
                            self.send_cmd("MD7")
                            print("MD7")
                        elif self._mode_b == "CW-R":
                            self.send_cmd("MD3")

            case _:
                return

    freq_a = Property(str, get_vfo_a, set_vfo_a, notify=freq_a_changed)
    freq_b = Property(str, get_vfo_b, set_vfo_b, notify=freq_b_changed)
    rx_focus = Property(str, get_rx_focus, set_rx_focus, notify=rx_focus_changed)
    tx_focus = Property(str, get_tx_focus, set_tx_focus, notify=tx_focus_changed)
    nr_status = Property(int, get_nr_status, set_nr_status, notify=nr_status_changed)
    mode_a = Property(str, get_mode_a, set_mode, notify=mode_a_changed)
    mode_b = Property(str, get_mode_b, set_mode, notify=mode_b_changed)


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

port = config.get("port", "/dev/ttyUSB0")
baud = config.get("baud", 115200)


radio = RadioBackend(port=port, baud=baud)
engine.rootContext().setContextProperty("radio", radio)

engine.load("main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())