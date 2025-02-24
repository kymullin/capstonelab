from pyvisa import VisaIOError
import matplotlib.pyplot as plt
from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset import (
    Measurement,
    initialise_database,
    new_experiment,
    plot_dataset,
)
from qcodes.instrument_drivers.Keithley import Keithley2450
import os
import datetime

# Replace with your instrument's IP
keithley_ip = "169.254.177.115"
resource_string = f"TCPIP::{keithley_ip}::INSTR"

keithley = Keithley2450("keithley", resource_string)
keithley.reset()

initialise_database()
experiment = new_experiment(name="Keithley_2450_example2", sample_name="no sample")

keithley.sense.function("current")
keithley.sense.range(1e-5)
keithley.sense.four_wire_measurement(True)

keithley.source.function("voltage")
keithley.source.range(0.2)
keithley.source.sweep_setup(0, 0.01, 10)

meas = Measurement(exp=experiment)

# Register source voltage parameter
meas.register_parameter(keithley.source.voltage)

# Register the measured current, using voltage as its setpoint
meas.register_parameter(keithley.sense.sweep, setpoints=[keithley.source.voltage])

with meas.run() as datasaver:
    for v in keithley.source.sweep_axis():  # Iterate over sweep values
        keithley.source.voltage(v)  # Set voltage
        current = keithley.sense.sweep()  # Measure current

        # Save both voltage and measured current
        datasaver.add_result(
            (keithley.source.voltage, v),  
            (keithley.sense.sweep, current)
        )

    dataid = datasaver.run_id
    print(f"Data saved with ID: {dataid}")

# Retrieve dataset
ds = datasaver.dataset
data = ds.get_parameter_data()

# Extract measured current
y_data = data["keithley_sense_sweep"]["keithley_sense_sweep"]

# Generate a simple x-axis (just index values)
x_data = range(len(y_data))
    
# Generate timestamp and create directory
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
directory_name = f"tests/{timestamp}"
os.makedirs(directory_name, exist_ok=True)
file_path = os.path.join(directory_name, "plot.png")

# Plot data
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, marker='o', linestyle='-')
plt.xlabel("Measurement Index")
plt.ylabel("Current (A)")
plt.title("Measured Current from Keithley 2450")
plt.grid(True)
plt.show()

# Close connection
keithley.close()

# Save plot as PNG
plt.savefig(file_path)
plt.close()
