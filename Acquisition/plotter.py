% Load CSV file
data = readtable('C:\Users\edis-\Desktop\my_super_bank_app-development\arduino_data.csv');
 
% Extract data columns
Time = data.Time;
IR1 = data.IR1;
IR2 = data.IR2;
IR3 = data.IR3;
Ultrasonic = data.Ultrasonic;
MotorR = data.MotorR;
MotorL = data.MotorL;
ServoMotor = data.ServoMotor;
 
% Plot data
figure;
 
subplot(3, 1, 1);
plot(Time, IR1, 'r-', 'LineWidth', 1.5);
hold on;
plot(Time, IR2, 'g-.', 'LineWidth', 1.5);
plot(Time, IR3, 'b--', 'LineWidth', 1.5);
title('IR Sensors');
xlabel('Time (s)');
ylabel('State');
legend('IRcentar', 'IRleft', 'IRright');
grid on;
 
subplot(3, 1, 2);
plot(Time, Ultrasonic, 'k-', 'LineWidth', 1.5);
title('Ultrasonic Sensor');
xlabel('Time (s)');
ylabel('State');
grid on;
 
subplot(3, 1, 3);
plot(Time, MotorR, 'b:', 'LineWidth', 2);
hold on;
plot(Time, MotorL, 'c-.', 'LineWidth', 1);
plot(Time, ServoMotor, 'k-', 'LineWidth', 1);
title('Motor and Servo');
xlabel('Time (s)');
ylabel('State');
legend('MotorR', 'MotorL', 'ServoMotor');
grid on;
 
% Adjust plot appearance
sgtitle('Arduino Sensor Data');


