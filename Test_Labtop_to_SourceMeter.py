import pyvisa

# Replace with your instrument's IP
keithley_ip = "192.168.2.2"
resource_string = f"TCPIP::{keithley_ip}::INSTR"

# Open a connection
rm = pyvisa.ResourceManager()
keithley = rm.open_resource(resource_string)

# Identify the instrument
print(keithley.query("*IDN?"))

# Close connection
keithley.close()
