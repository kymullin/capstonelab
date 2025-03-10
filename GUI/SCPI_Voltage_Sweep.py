import numpy as np
import matplotlib.pyplot as plt
import time
import os
import datetime
from qcodes.instrument_drivers.Keithley import Keithley2450

def perform_iv_sweep(save_directory: str, test_number: int):
    # Replace with your instrument's IP
    keithley_ip = "192.168.2.2"
    resource_string = f"TCPIP::{keithley_ip}::INSTR"
    
    keithley = Keithley2450("keithley", resource_string)
    keithley.reset()
    
    # Enable output
    keithley.write("OUTP ON")  
    time.sleep(0.5)  # Allow stabilization
    
    # Verify Output is On
    if keithley.ask_raw("OUTP?").strip() != "1":
        print("⚠ Warning: Output is OFF! Measurement may fail.")
    
    # Define voltage range
    voltages = np.linspace(-10, 10, 41)  # 41 steps from -10V to 10V
    voltages_reverse = voltages[::-1]  # Reverse sweep
    currents = []
    
    # Forward Sweep: -10V to 10V
    for v in voltages:
        keithley.write(f"SOUR:VOLT {v}")  # Set voltage
        time.sleep(0.1)  # Allow settling
        current = float(keithley.ask_raw("MEAS:CURR?"))  # Measure current
        currents.append(current)
        print(f"V: {v:.2f}V, I: {current:.6f}A")  # Live output
    
    # Reverse Sweep: 10V back to -10V
    for v in voltages_reverse:
        keithley.write(f"SOUR:VOLT {v}")  # Set voltage
        time.sleep(0.1)  # Allow settling
        current = float(keithley.ask_raw("MEAS:CURR?"))  # Measure current
        currents.append(current)
        print(f"V: {v:.2f}V, I: {current:.6f}A")  # Live output
    
    # Turn off output after sweep
    keithley.write("OUTP OFF")
    
    # Ensure save directory exists
    os.makedirs(save_directory, exist_ok=True)
    file_path = os.path.join(save_directory, f"Test_Result_{test_number}.png")
    
    # Plot results
    plt.figure(figsize=(8, 6))
    plt.plot(np.concatenate([voltages, voltages_reverse]), currents, marker="o", linestyle="-", markersize=2)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.title("I-V Curve - Forward and Reverse Sweep")
    plt.grid(True)
    
    # Save plot as PNG
    plt.savefig(file_path)
    plt.close()
    
    # Close connection
    keithley.close()
    
    print(f"Test result saved to {file_path}")
