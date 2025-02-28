import os
import numpy as np
import matplotlib.pyplot as plt
import time
from qcodes.dataset import (
    Measurement,
    initialise_database,
    new_experiment,
)
from qcodes.instrument_drivers.Keithley import Keithley2450

def perform_iv_sweep(save_dir, test_num, keithley_ip="169.254.144.15"):
    resource_string = f"TCPIP::{keithley_ip}::INSTR"
    keithley = Keithley2450("keithley", resource_string)
    keithley.reset()
    
    initialise_database()
    experiment = new_experiment(name="Keithley_2450_example", sample_name="no sample")
    
    keithley.sense.function("current")
    keithley.sense.range(1e-5)
    keithley.sense.four_wire_measurement(True)
    
    keithley.source.function("voltage")
    keithley.source.range(10)
    keithley.source.voltage(-10)
    
    keithley.write(":OUTP ON")
    time.sleep(0.5)
    
    if keithley.ask(":OUTP?").strip() != "1":
        print("⚠ Warning: Output is OFF! Measurement may fail.")
    
    meas = Measurement(exp=experiment)
    meas.register_parameter(keithley.source.voltage)
    meas.register_parameter(keithley.sense.current, setpoints=[keithley.source.voltage])
    
    voltages, currents = [], []
    with meas.run() as datasaver:
        for v in np.arange(-10, 10.01, 0.5):  
            keithley.source.voltage(v)  
            current = keithley.sense.current()  
            voltages.append(v)
            currents.append(current)
            datasaver.add_result((keithley.source.voltage, v), (keithley.sense.current, current))
        
        for v in np.arange(10, -10.01, -0.5):  
            keithley.source.voltage(v)  
            current = keithley.sense.current()  
            voltages.append(v)
            currents.append(current)
            datasaver.add_result((keithley.source.voltage, v), (keithley.sense.current, current))
    
    keithley.close()

    plt.figure(figsize=(8, 6))
    plt.plot(voltages, currents, marker="o", linestyle="-", markersize=2)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.title("IV Curve - Forward and Reverse Sweep")
    plt.grid(True)
    
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"Test_Result_{test_num}.png")
    plt.savefig(save_path)
    plt.close()
    
    print(f"Plot saved to {save_path}")
    return save_path
