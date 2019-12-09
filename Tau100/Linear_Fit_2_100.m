clear
clc

% -------------------------------------------------------------------------
% Setting Parameters
% -------------------------------------------------------------------------

tau = 100; 

num_even_echos = 4;

CCM_min = 200; 

CCM_max = 900;

CCM_in = 100;

% -------------------------------------------------------------------------
% Calculations
% -------------------------------------------------------------------------

% Averaging stationary data for 3 measurments

sfname1 = ['cpmg_1_0_', num2str(tau), '.tnt'];
sfname2 = ['cpmg_2_0_', num2str(tau), '.tnt'];
sfname3 = ['cpmg_3_0_', num2str(tau), '.tnt'];

sdata1 = abs(bnrreadgarfield(sfname1));
sdata2 = abs(bnrreadgarfield(sfname2));
sdata3 = abs(bnrreadgarfield(sfname3));

sdata = (sdata1 + sdata2 + sdata3) ./ 3;

% Calculating time axis for the fit to find A and B

tau_s = 80 / 1000000;

time = [];

for i = tau_s*4:tau_s*4:tau_s*4*num_even_echos
    
    time = [time, i];
    
end

% Calculating A, B, C and D and the velocity for the first measurments 

CCM = CCM_min;

j1 = 1;

while CCM <= CCM_max
    
   ffname1 = ['cpmg_1_', num2str(CCM), '_' , num2str(tau), '.tnt'];
   
   fdata1 = abs(bnrreadgarfield(ffname1));
   
   fdata1_cell{j1} = fdata1;
   
   CCM = CCM + CCM_in;
   
   j1 = j1 + 1;
   
end

A1_row = [];

B1_row = [];

k1 = 1;

while k1 <= size(fdata1_cell, 2)
    
    fdata1_fit = fdata1_cell{k1};
    
    sdata1_fit = sdata;
    
    npeak1_even = [];
    
    for l1 = 1 : (2*num_even_echos)
        
        frow1 = (fdata1_fit(:,l1))';
        
        fpeak1 = max(frow1);
        
        srow1 = (sdata1_fit(:, l1))';
        
        speak1 = max(srow1);
        
        npeak1 = fpeak1/speak1;
        
        if 0 == rem(l1, 2)
            
            npeak1_even = [npeak1_even, npeak1];
            
        end
               
    end
   
sum_time = sum(time); 

sum_yAB1 = sum(npeak1_even); 

sum_time_squared = sum(time.^2); 

squared_sum_time = (sum(time))^2; 

sum_timeyAB1 = sum(time .* npeak1_even);

deltaAB1 =(num_even_echos * sum_time_squared) - squared_sum_time;

A1 = ((sum_time_squared * sum_yAB1) - (sum_time * sum_timeyAB1))/(deltaAB1);

B1 = ((num_even_echos * sum_timeyAB1) - (sum_time * sum_yAB1))/(deltaAB1);

A1_row = [A1_row, A1];

B1_row = [B1_row, B1];

k1 = k1 + 1;
    
end

% This section of dose not ahve to be repeated in the second and thrid
% measurments
% -------------------------------------------------------------------------

v = [CCM_min:CCM_in:CCM_max] ./ (pi * ((0.33)^2) * 100 * 60); 

sum_v = sum(v);

sum_v_squared = sum(v.^2);

squared_sum_v = (sum_v)^2;

N = size(v, 2);

% -------------------------------------------------------------------------

yCD1 = (-1)*(B1_row ./ A1_row);

sum_yCD1 = sum(yCD1);

sum_timeyCD1 = sum(yCD1 .* v);

deltaCD1 = (N * sum_v_squared) - squared_sum_v;

C1 = ((sum_v_squared * sum_yCD1) - (sum_v * sum_timeyCD1)) / deltaCD1;

D1 = ((N * sum_timeyCD1) - (sum_v * sum_yCD1)) / deltaCD1;

for n1 = 1:size(v, 2)
    
    vNMR1(n1) = ((yCD1(n1)) - C1) / D1;
    
end

% Calculating A, B, C and D and the velocity for the second measurments 

CCM = CCM_min;

j2 = 1;

while CCM <= CCM_max
    
   ffname2 = ['cpmg_2_', num2str(CCM), '_' , num2str(tau), '.tnt'];
   
   fdata2 = abs(bnrreadgarfield(ffname2));
   
   fdata2_cell{j2} = fdata2;
   
   CCM = CCM + CCM_in;
   
   j2 = j2 + 1;
   
end

A2_row = [];

B2_row = [];

k2 = 1;

while k2 <= size(fdata2_cell, 2)
    
    fdata2_fit = fdata2_cell{k2};
    
    sdata2_fit = sdata;
    
    npeak2_even = [];
    
    for l2 = 1 : (2*num_even_echos)
        
        frow2 = (fdata2_fit(:,l2))';
        
        fpeak2 = max(frow2);
        
        srow2 = (sdata2_fit(:, l2))';
        
        speak2 = max(srow2);
        
        npeak2 = fpeak2/speak2;
        
        if 0 == rem(l2, 2)
            
            npeak2_even = [npeak2_even, npeak2];
            
        end
               
    end
   
sum_time = sum(time); 

sum_yAB2 = sum(npeak2_even); 

sum_time_squared = sum(time.^2); 

squared_sum_time = (sum(time))^2; 

sum_timeyAB2 = sum(time .* npeak2_even);

deltaAB2 =(num_even_echos * sum_time_squared) - squared_sum_time;

A2 = ((sum_time_squared * sum_yAB2) - (sum_time * sum_timeyAB2))/(deltaAB2);

B2 = ((num_even_echos * sum_timeyAB2) - (sum_time * sum_yAB2))/(deltaAB2);

A2_row = [A2_row, A2];

B2_row = [B2_row, B2];

k2 = k2 + 1;
    
end

yCD2 = (-1)*(B2_row ./ A2_row);

sum_yCD2 = sum(yCD2);

sum_timeyCD2 = sum(yCD2 .* v);

deltaCD2 = (N * sum_v_squared) - squared_sum_v;

C2 = ((sum_v_squared * sum_yCD2) - (sum_v * sum_timeyCD2)) / deltaCD2;

D2 = ((N * sum_timeyCD2) - (sum_v * sum_yCD2)) / deltaCD2;

for n2 = 1:size(v, 2)
    
    vNMR2(n2) = ((yCD2(n2)) - C2) / D2;
    
end

% Calculating A, B, C and D and the velocity for the thrid measurments 3

CCM = CCM_min;

j3 = 1;

while CCM <= CCM_max
    
   ffname3 = ['cpmg_3_', num2str(CCM), '_' , num2str(tau), '.tnt'];
   
   fdata3 = abs(bnrreadgarfield(ffname3));
   
   fdata3_cell{j3} = fdata3;
   
   CCM = CCM + CCM_in;
   
   j3 = j3 + 1;
   
end

A3_row = [];

B3_row = [];

k3 = 1;

while k3 <= size(fdata3_cell, 2)
    
    fdata3_fit = fdata3_cell{k3};
    
    sdata3_fit = sdata;
    
    npeak3_even = [];
    
    for l3 = 1 : (2*num_even_echos)
        
        frow3 = (fdata3_fit(:,l3))';
        
        fpeak3 = max(frow3);
        
        srow3 = (sdata3_fit(:, l3))';
        
        speak3 = max(srow3);
        
        npeak3 = fpeak3/speak3;
        
        if 0 == rem(l3, 2)
            
            npeak3_even = [npeak3_even, npeak3];
            
        end
               
    end
   
sum_time = sum(time); 

sum_yAB3 = sum(npeak3_even); 

sum_time_squared = sum(time.^2); 

squared_sum_time = (sum(time))^2; 

sum_timeyAB3 = sum(time .* npeak3_even);

deltaAB3 =(num_even_echos * sum_time_squared) - squared_sum_time;

A3 = ((sum_time_squared * sum_yAB3) - (sum_time * sum_timeyAB3))/(deltaAB3);

B3 = ((num_even_echos * sum_timeyAB3) - (sum_time * sum_yAB3))/(deltaAB3);

A3_row = [A3_row, A3];

B3_row = [B3_row, B3];

k3 = k3 + 1;
    
end

yCD3 = (-1)*(B3_row ./ A3_row);

sum_yCD3 = sum(yCD3);

sum_timeyCD3 = sum(yCD3 .* v);

deltaCD3 = (N * sum_v_squared) - squared_sum_v;

C3 = ((sum_v_squared * sum_yCD3) - (sum_v * sum_timeyCD3)) / deltaCD3;

D3 = ((N * sum_timeyCD3) - (sum_v * sum_yCD3)) / deltaCD3;

for n3 = 1:size(v, 2)
    
    vNMR3(n3) = ((yCD3(n3)) - C3) / D3;
    
end

% Calcualting vertical and horozontal error bars

yCD_avg = (yCD1 + yCD2 + yCD3) ./ 3;

d1 = (yCD1 - yCD_avg).^2;
  
d2 = (yCD2 - yCD_avg).^2; 
  
d3 = (yCD3 - yCD_avg).^2;

d = d1 + d2 + d3;

SD = sqrt((1/(N-1))*d);

for o = 1:size(v, 2)
    
    err_x(o) = ((2800) * 0.005)/(pi * ((0.33)^2) * 100 * 60); 
    
end

% Averagig each estiamte of -(B/A) and putting them in a vector to be
% plotted on the vertical axis

y_axis = (yCD1 + yCD2 + yCD3) ./ 3;

% Finding the average velocity for all three measurments

vNMR_avg = (vNMR1 + vNMR2 + vNMR3) ./ 3;

% Calculating the the corrolation coefficient (r) for the graph of -(B/A) 
% vs v_avg

y_avg = sum(y_axis) / size(y_axis, 2);

x_avg = sum(vNMR_avg) / size(vNMR_avg, 2);

sigma_xy = sum((vNMR_avg - x_avg) .* (y_axis - y_avg));

sigma_x = sum((vNMR_avg - x_avg) .^ 2);

sigma_y = sum((y_axis - y_avg) .^2);

r = sigma_xy / sqrt(sigma_x * sigma_y);

% -------------------------------------------------------------------------
% Plotting
% -------------------------------------------------------------------------

errorbar(v, y_axis, SD, SD, err_x, err_x, 'o');
xlabel('Velocity (m/s)');
ylabel('-B/A (1/s)');

% -------------------------------------------------------------------------
% Displaying results
% -------------------------------------------------------------------------

for m = 1 : size(v, 2)
    
    disp(['Flow Velocity (Rotameter): ' num2str(v(m)) ' m/s']);
    disp(['Flow Velocity (NMR)      : ' num2str(vNMR_avg(m)) ' m/s']);
    disp('                                                         '); 
    
end

disp(['r = ' num2str(r)]);

% -------------------------------------------------------------------------
% Excel Exports
% -------------------------------------------------------------------------

v_col = v';

vNMR_avg_col = vNMR_avg';





