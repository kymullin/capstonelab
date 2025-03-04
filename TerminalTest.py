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
import os
import datetime
from PIL import Image


# Replace with your instrument's IP
keithley_ip = "192.168.2.2"
resource_string = f"TCPIP::{keithley_ip}::INSTR"

keithley = Keithley2450("keithley", resource_string)
keithley.reset()

# Send query command manually
print(f"Current terminal: {keithley.terminals.get()}")
print(f"4-wire sensing enabled: {keithley.sense.four_wire_measurement.get()}")
print(f"Measurement function: {keithley.sense.function.get()}")
print(keithley.parameters)


keithley.close()
