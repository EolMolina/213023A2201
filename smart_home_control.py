import tkinter as tk

# Clase base
class Device:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"

    def turn_on(self):
        self.state = "ON"

    def turn_off(self):
        self.state = "OFF"

    def status(self):
        return f"{self.name}: {self.state}"


# Clases hijas
class SmartLight(Device):
    def turn_on(self):
        self.state = "ON - Bright Light"

    def turn_off(self):
        self.state = "OFF - Light Off"

    def configure(self, mode=None, intensity=None, time=None):
        return f"Light configured: mode={mode}, intensity={intensity}, time={time}"


class SmartCurtain(Device):
    def turn_on(self):
        self.state = "OPEN"

    def turn_off(self):
        self.state = "CLOSED"

    def configure(self, mode=None, intensity=None, time=None):
        return f"Curtain configured: mode={mode}, time={time}"


class SmartThermostat(Device):
    def turn_on(self):
        self.state = "ON - Heating"

    def turn_off(self):
        self.state = "OFF"

    def configure(self, mode=None, intensity=None, time=None):
        return f"Temperature set to {intensity}°C"


# Control central
class ControlCenter:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def turn_on_all(self):
        for d in self.devices:
            d.turn_on()

    def turn_off_all(self):
        for d in self.devices:
            d.turn_off()

    def show_status(self):
        return "\n".join([d.status() for d in self.devices])


# Crear objetos
control = ControlCenter()
light = SmartLight("Living Room Light")
curtain = SmartCurtain("Main Curtain")
thermostat = SmartThermostat("Home Thermostat")

control.add_device(light)
control.add_device(curtain)
control.add_device(thermostat)


# Interfaz gráfica
window = tk.Tk()
window.title("Smart Home Control")

text = tk.StringVar()

def update_status():
    text.set(control.show_status())

def turn_on():
    control.turn_on_all()
    update_status()

def turn_off():
    control.turn_off_all()
    update_status()

label = tk.Label(window, textvariable=text, font=("Arial", 12))
label.pack()

btn_on = tk.Button(window, text="Turn ON all devices", command=turn_on)
btn_on.pack()

btn_off = tk.Button(window, text="Turn OFF all devices", command=turn_off)
btn_off.pack()

update_status()

window.mainloop()
