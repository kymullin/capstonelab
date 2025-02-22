import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
from qcodes.dataset import (
    Measurement,
    initialise_database,
    new_experiment,
)
from qcodes.instrument_drivers.Keithley import Keithley2450

# Replace with your instrument's IP
keithley_ip = "169.254.142.72"
resource_string = f"TCPIP::{keithley_ip}::INSTR"

keithley = Keithley2450("keithley", resource_string)
keithley.reset()

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
keithley.source.voltage(0)  # Start at 0V before sweeping

# **Enable Output**
keithley.write(":OUTP ON")
time.sleep(0.5)  # Wait for stability

# Verify Output is On
if keithley.ask(":OUTP?").strip() != "1":
    print("⚠ Warning: Output is OFF! Measurement may fail.")

# Setup Measurement
meas = Measurement(exp=experiment)
# Register parameters before measurement
meas.register_parameter(keithley.source.voltage)  # Register voltage
meas.register_parameter(keithley.sense.current, setpoints=[keithley.source.voltage])  # Register current with voltage as setpoint

voltages = []
currents = []

with meas.run() as datasaver:
    for v in np.arange(-10, 10.01, 0.1):  # Sweep from -10V to 10V
        keithley.source.voltage(v)  # Set voltage
        current = keithley.sense.current()  # Measure current

        # Save to lists for plotting
        voltages.append(v)
        currents.append(current)

        datasaver.add_result(
            (keithley.source.voltage, v),
            (keithley.sense.current, current)
        )

    dataid = datasaver.run_id

# ✅ Plot the results using Matplotlib
plt.figure(figsize=(8, 6))
plt.plot(voltages, currents, marker="o", linestyle="-", markersize=2)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("IV Curve")
plt.grid(True)
plt.show()