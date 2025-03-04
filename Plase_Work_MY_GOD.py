import numpy as np
import matplotlib.pyplot as plt
import time
from qcodes.dataset import (
    Measurement,
    initialise_database,
    new_experiment,
)
from qcodes.instrument_drivers.Keithley import Keithley2450

# Replace with your instrument's IP
keithley_ip = "192.168.2.2"
resource_string = f"TCPIP::{keithley_ip}::INSTR"

keithley = Keithley2450("keithley", resource_string)
keithley.reset()

# **Set Front Terminals**
keithley.write(":ROUT:TERM FRON")

# Initialize QCoDeS database
initialise_database()
experiment = new_experiment(name="Keithley_2450_example", sample_name="no sample")

# Configure Keithley for Current Measurement
keithley.sense.function("current")
keithley.sense.range(1e-5)
keithley.sense.four_wire_measurement(True)

# Configure Voltage Source
keithley.source.function("voltage")
keithley.source.range(10)

# **Enable Output**
keithley.write(":OUTP ON")
time.sleep(0.5)  # Wait for stability

# Verify Output is On
if keithley.ask(":OUTP?").strip() != "1":
    print("⚠ Warning: Output is OFF! Measurement may fail.")

# **Linear Sweep Parameters**
start_v = -10  # Start voltage
stop_v = 10    # Stop voltage
step = 0.5     # Voltage step size
delay = 0.1    # Delay between steps (seconds)

voltages = np.arange(start_v, stop_v + step, step)  # Generate voltage steps
currents = []

# **Perform the Linear Sweep**
for v in voltages:
    keithley.source.voltage(v)  # Set voltage
    time.sleep(delay)  # Allow system to settle
    current = keithley.sense.current()  # Measure current

    currents.append(current)

# **Turn Off Output After Measurement**
keithley.write(":OUTP OFF")

# **Plot the results**
plt.figure(figsize=(8, 6))
plt.plot(voltages, currents, marker="o", linestyle="-", markersize=2)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("IV Curve - Linear Sweep")
plt.grid(True)
plt.show()
