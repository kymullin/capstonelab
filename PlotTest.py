import os
import datetime
import matplotlib.pyplot as plt
    
# Generate timestamp and create directory
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
directory_name = f"tests/{timestamp}"
os.makedirs(directory_name, exist_ok=True)
file_path = os.path.join(directory_name, "plot.png")

plt.plot([1, 2, 3], [1, 4, 9])
plt.title("Test Plot")

# Save plot as PNG
plt.savefig(file_path)
plt.close()
