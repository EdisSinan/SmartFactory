import serial
import csv
import time

# Adjust the COM port and baud rate based on your Arduino settings
arduino_port = 'COM10'  # Change to your Arduino's COM port
baud_rate = 9600

# Open the serial connection
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Allow time for the connection to establish

# Create and open a CSV file for writing
csv_file_path = 'arduino_data.csv'
csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write headers to CSV file
csv_writer.writerow(['Time', 'IR1', 'IR2', 'IR3', 'Ultrasonic', 'MotorR', 'MotorL', 'ServoMotor'])

try:
    start_time = time.time()  # Record the start time
    while True:
        # Calculate elapsed time in seconds with 0.5s resolution
        elapsed_time = round(time.time() - start_time, 1)
        
        # Read data from Arduino
        arduino_data = arduino.readline().decode('utf-8').strip().split(',')

        # Check if the received data is valid
        if len(arduino_data) == 8:
            # Write data to CSV file
            csv_writer.writerow([elapsed_time] + arduino_data)
            
            # Print data to console (optional)
            print(elapsed_time, arduino_data)

except KeyboardInterrupt:
    print("Logging stopped by the user.")

finally:
    # Close the serial connection and CSV file
    arduino.close()
    csv_file.close()
