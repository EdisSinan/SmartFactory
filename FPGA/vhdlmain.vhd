module line_follower (
  input clk,
  input [3:0] qti_sensors,
  output reg arduino1,
  output reg arduino2,
  output reg arduino3,
  output reg ulzvarduino0,
  output reg left_motor,
  output reg right_motor,
  output reg kipper,
  input wire echo,
  output wire trig
);
reg [31:0] counter;
//Echo sensor 
reg trig_value = 1'b0;

//Echo counter
reg [25:0] count;
reg n_trigger;
reg old_pulse;
reg [32:0] count_out;
reg [32:0] pulse_count;
reg [32:0] status;
initial begin
count = 25'b0;
n_trigger = 1'b0;
old_pulse = 1'b0;
count_out = 33'b0;
pulse_count = 33'b0;
status = 33'b0;
end
reg [5:0]object_counter = 5'b0;
reg [4:0] state=0;
reg [24:0] yet_another_delay =0;
// Define the internal signals
reg [2:0] line_position;
reg [16:0] left_motor_speed_reg;
reg [16:0] right_motor_speed_reg;
reg [16:0] kipper_reg;
//always block to start counting object fallen inside the truck
always @(posedge clk) begin
    //Always add one to count, this is the overall counter for the script
    count = count + 1;
    //This is used to pick a very specific time out for trigger control
    //This count is mased on a 50 MHz clock
    n_trigger = ~&(count[24:9]);    //Pulse of us every ms
    if (~&(count[24:10])) begin
        //If ~&(count[24:10]) is 1 count the pulse AND OR send that count out to the status if statement
        if (n_trigger) begin
            if (echo == 1) begin
                pulse_count = pulse_count + 1;
            end
            if ((old_pulse == 1)&&(echo == 0)) begin
                count_out = pulse_count;
                pulse_count = 0;
            end
        end
    end
    // This number is the distance control the status is used as a buffer for filtering (OR filter below) 20832 equals 5cm and 5292 equals 2cm
    if (count_out < 33'd20832 && count_out > 33'd5292) begin
        object_counter <= 1;
        if (object_counter == 1)
        begin
        state=1;
        end
        else 
        begin
        state=0;
        end
        status = status << 1;
        status[0] = 1;
    end else begin
        status = status << 1;
        status[0] = 0;
    end
    old_pulse = echo;
    if(state == 1)
begin
ulzvarduino0 <= 1;
kipper_reg <= 50000;
  case (line_position)
    2'b000: begin // centar
      left_motor_speed_reg <= 65000; 
      right_motor_speed_reg <= 85000;
     end
    2'b010: begin // left
      left_motor_speed_reg <= 65000;
      right_motor_speed_reg <= 65000;
    end
    2'b001: begin // Right
      left_motor_speed_reg <= 85000;
      right_motor_speed_reg <= 85000;
    end
    2'b011: begin //At the end
        left_motor_speed_reg <=0;
      right_motor_speed_reg <= 0;
        ulzvarduino0 <= 0;
        state<=2;
        end
  endcase 
end
else
if(state == 2)
begin
ulzvarduino0 <= 0;
 case (line_position)
    2'b000: begin // centar
      left_motor_speed_reg <= 0; 
      right_motor_speed_reg <= 0;
        kipper_reg <= 100000;
        state <= 3;
     end
    2'b010: begin // left
      left_motor_speed_reg <= 65000;
      right_motor_speed_reg <= 65000;
    end
    2'b001: begin // Right
      left_motor_speed_reg <= 85000;
      right_motor_speed_reg <= 85000;
    end
    2'b011: begin //At the end
        left_motor_speed_reg <=85000;
      right_motor_speed_reg <= 85000;
        end
  endcase

end
else 
if (state == 3)
begin
ulzvarduino0 <= 0;
  case (line_position)
    2'b000: begin // centar
      left_motor_speed_reg <= 65000; 
      right_motor_speed_reg <= 85000;
     end
    2'b010: begin // left
      left_motor_speed_reg <= 65000;
      right_motor_speed_reg <= 65000;
    end
    2'b001: begin // Right
      left_motor_speed_reg <= 85000;
      right_motor_speed_reg <= 85000;
    end
    2'b011: begin //At the end
        left_motor_speed_reg <=0;
      right_motor_speed_reg <= 0;
        kipper_reg <= 100000;
        state<=4;
        end
  endcase
end
else 
if(state==4)
begin
ulzvarduino0 <= 0;
        kipper_reg <= 50000;
 case (line_position)
    2'b000: begin // centar
      left_motor_speed_reg <= 0; 
      right_motor_speed_reg <= 0;
        kipper_reg <= 50000;
        object_counter <= 0;
        state <=0;
     end
    2'b010: begin // left
      left_motor_speed_reg <= 65000;
      right_motor_speed_reg <= 65000;
    end
    2'b001: begin // Right
      left_motor_speed_reg <= 85000;
      right_motor_speed_reg <= 85000;
    end
    2'b011: begin //At the end
        left_motor_speed_reg <=65000;
      right_motor_speed_reg <= 65000;
        end
  endcase

end
else
if(state == 0)
begin
left_motor_speed_reg <=0;
right_motor_speed_reg <= 0;
ulzvarduino0 <= 0;
end 
end
assign trig = n_trigger;
//Logic OR filter status here
// Always block to read the QTI sensors and determine the line position
always @(posedge clk) begin
  // Read the QTI sensors
if (qti_sensors[0] == 0 ) begin
     arduino1 <= 1;
     arduino2 <= 0;
     arduino3 <= 0;
    line_position <= 2'b000; // Center
  end else if (qti_sensors[1] == 0 ) begin
    line_position <= 2'b001; // Right
     arduino1 <= 0;
     arduino2 <= 1;
     arduino3 <= 0;
  end 
  else if (qti_sensors[2] == 0) begin
    line_position <= 2'b010; // Left
     arduino1 <= 0;
     arduino2 <= 0;
     arduino3 <= 1;
    end 
    else 
    begin
    line_position <= 2'b011; // Lost
     arduino1 <= 0;
     arduino2 <= 0;
     arduino3 <= 0;
end
end
// Always block to calculate the motor speeds
always @(posedge clk) begin
  // Calculate the motor speeds
end 

  // Initialize the counter
  always @(posedge clk) begin
    if (counter>1_000_000) 
      counter <= 0;
    else begin
      counter <= counter + 1;
    end

    if (counter <= left_motor_speed_reg) 
    left_motor <= 1;
    else 
    left_motor <= 0;

    if (counter <= right_motor_speed_reg) 
    right_motor <= 1;
    else 
    right_motor <= 0;
     if (counter <= kipper_reg) 
    kipper <= 1;
    else 
    kipper <= 0;
  end
endmodule 

