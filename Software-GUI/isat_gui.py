import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
import threading
import time
from matplotlib.dates import datestr2num

# Set the host and port to connect to the ESP32
ESP32_IP = "192.168.4.1"
ESP32_PORT = 80

# Create a socket object to connect to ESP32
esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create the main application window with a fixed size
root = tk.Tk()
root.title("iSat-Ground Station v1.0.0.")
root.geometry("1000x800")  # Set the window size to 1000x800 pixels
root.configure(bg="black")  # Set the background color to black

# Create a notebook with tabs for different sensor data
notebook = ttk.Notebook(root)

notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Create a frame for all graphs
all_graphs_frame = ttk.Frame(notebook)
notebook.add(all_graphs_frame, text="All Data")


# Create Matplotlib figures and axes for all graphs
fig = Figure(figsize=(12, 8))

accel_ax = fig.add_subplot(231)
accel_ax.set_title("Acceleration")
accel_ax.set_xlabel("Time")
accel_ax.set_ylabel("Value")

gyro_ax = fig.add_subplot(232)
gyro_ax.set_title("Rotation")
gyro_ax.set_xlabel("Time")
gyro_ax.set_ylabel("Value")

pressure_ax = fig.add_subplot(233)
pressure_ax.set_title("Pressure")
pressure_ax.set_xlabel("Time")
pressure_ax.set_ylabel("Value")

altitude_ax = fig.add_subplot(234)
altitude_ax.set_title("Altitude")
altitude_ax.set_xlabel("Time")
altitude_ax.set_ylabel("Value")

# Create a label for temperature
temp_label = tk.Label(all_graphs_frame, text="Temperature: N/A",
                      font=("Helvetica", 12), bg="black", fg="white")
temp_label.pack()

# Create a label for timestamp
timestamp_label = tk.Label(all_graphs_frame, text="", font=(
    "Helvetica", 10), bg="black", fg="white")
timestamp_label.pack()

# Create a canvas to display the Matplotlib figure
accel_canvas = FigureCanvasTkAgg(fig, master=all_graphs_frame)
accel_canvas.get_tk_widget().pack()

# Lists to store data for the graphs
accel_data_x = []
accel_data_y = []
accel_data_z = []
gyro_data_x = []
gyro_data_y = []
gyro_data_z = []
pressure_data = []
altitude_data = []
timestamps = []
temperature_data = []

# Function to connect to ESP32 and receive sensor data


def connect_to_esp32():
    try:
        esp32_socket.connect((ESP32_IP, ESP32_PORT))
        while True:
            data = esp32_socket.recv(1024).decode("utf-8")
            if data:
                update_gui(data)
            else:
                break
    except Exception as e:
        print("Error:", e)
    finally:
        esp32_socket.close()

# Function to update the GUI with sensor data


def update_gui(data):
    parts = data.split(',')
    if len(parts) == 9:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        timestamps.append(timestamp)
        accel_x = float(parts[0])
        accel_y = float(parts[1])
        accel_z = float(parts[2])
        gyro_x = float(parts[3])
        gyro_y = float(parts[4])
        gyro_z = float(parts[5])
        pressure = float(parts[6])
        altitude = float(parts[7])
        temperature = float(parts[8])

        # Append data to lists for the graphs
        accel_data_x.append(datestr2num(timestamp))
        accel_data_y.append(accel_x)
        accel_data_z.append(accel_y)
        gyro_data_x.append(datestr2num(timestamp))
        gyro_data_y.append(gyro_x)
        gyro_data_z.append(gyro_y)
        pressure_data.append(datestr2num(timestamp))
        pressure_data.append(pressure)
        altitude_data.append(datestr2num(timestamp))
        altitude_data.append(altitude)
        temperature_data.append(temperature)

        # Limit the number of data points displayed on the graphs
        max_data_points = 50
        if len(accel_data_x) > max_data_points:
            accel_data_x.pop(0)
            accel_data_y.pop(0)
            accel_data_z.pop(0)
            gyro_data_x.pop(0)
            gyro_data_y.pop(0)
            gyro_data_z.pop(0)
            pressure_data.pop(0)
            pressure_data.pop(0)
            altitude_data.pop(0)
            altitude_data.pop(0)
            timestamps.pop(0)
            temperature_data.pop(0)

        # Update acceleration plot
        accel_ax.clear()
        accel_ax.plot(accel_data_x, accel_data_y, label="X")
        accel_ax.plot(accel_data_x, accel_data_z, label="Y")
        accel_ax.plot(accel_data_x, accel_data_z, label="Z")

        # Update rotation plot
        gyro_ax.clear()
        gyro_ax.plot(accel_data_x, gyro_data_x, label="X")
        gyro_ax.plot(accel_data_x, gyro_data_y, label="Y")
        gyro_ax.plot(accel_data_x, gyro_data_z, label="Z")

        # Update pressure plot
        pressure_ax.clear()
        pressure_ax.plot(pressure_data[::2],
                         pressure_data[1::2], label="Pressure")

        # Update altitude plot
        altitude_ax.clear()
        altitude_ax.plot(altitude_data[::2],
                         altitude_data[1::2], label="Altitude")

        # Update temperature label
        temp_label.config(text=f"Temperature: {temperature} °C")

        # Update timestamp label
        timestamp_label.config(text=f"Last Update: {timestamp}")

        # Draw all the plots
        accel_ax.legend()
        gyro_ax.legend()
        pressure_ax.legend()
        altitude_ax.legend()
        accel_canvas.draw()


# Start a thread to connect to ESP32 and receive data
esp32_thread = threading.Thread(target=connect_to_esp32)
esp32_thread.daemon = True
esp32_thread.start()

root.mainloop()
