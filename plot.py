import matplotlib.pyplot as plt
import csv

def plot_all_tests(csv_path: str):
    label_map = {
        "1": "Fully Reacted",
        "2": "Semi-Reacted",
        "3": "Not Reacted",
        "4": "Semi-Reacted"
    }

    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header

        plt.figure(figsize=(10, 10))

        for row in reader:
            test_number = row[0]
            label = label_map.get(test_number, f"Test {test_number}")
            data = list(map(float, row[1:]))
            voltages = data[0::2]
            currents = data[1::2]

            # Determine style
            linestyle = '-' if label == "Semi-Reacted" else '-'
            if test_number == "3":
                color = '#222222'
            elif test_number == "2":
                color = '#FF0000'
            elif test_number == "1":
                color = '#0000FF'
            elif test_number == "4":
                color = '#008800'
            else:
                color = None  # Let matplotlib auto-assign

            plt.plot(voltages, currents, marker='o', linestyle=linestyle, markersize=2, label=label, color=color)

        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.title("I-V Curves Comparison")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    plot_all_tests("tests.csv")
