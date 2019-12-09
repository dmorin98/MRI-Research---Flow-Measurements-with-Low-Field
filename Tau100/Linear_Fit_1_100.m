clear 
clc

% setting parameters

sname1 = 'cpmg_1_0_100.tnt'; 
sname2 = 'cpmg_2_0_100.tnt'; 
sname3 = 'cpmg_3_0_100.tnt';  

fname = 'cpmg_1_200_100.tnt';

tau = 80 / 1000000;

num_even_echos = 5;

% Calculations

sdata1 = abs(bnrreadgarfield(sname1));
sdata2 = abs(bnrreadgarfield(sname2));
sdata3 = abs(bnrreadgarfield(sname3));

sdata = (sdata1 + sdata2 + sdata3) ./ 3;

fdata = abs(bnrreadgarfield(fname));

sdata_row1 = (sdata(:,1))';
sdata_row2 = (sdata(:,2))';
sdata_row3 = (sdata(:,3))';
sdata_row4 = (sdata(:,4))';
sdata_row5 = (sdata(:,5))';
sdata_row6 = (sdata(:,6))';
sdata_row7 = (sdata(:,7))';
sdata_row8 = (sdata(:,8))';
sdata_row9 = (sdata(:,9))';
sdata_row10 = (sdata(:,10))';
sdata_row11 = (sdata(:,11))';
sdata_row12 = (sdata(:,12))';
sdata_row13 = (sdata(:,13))';
sdata_row14 = (sdata(:,14))';
sdata_row15 = (sdata(:,15))';
sdata_row16 = (sdata(:,16))';

sdata_peak1 = max(sdata_row1);
sdata_peak2 = max(sdata_row2);
sdata_peak3 = max(sdata_row3);
sdata_peak4 = max(sdata_row4);
sdata_peak5 = max(sdata_row5);
sdata_peak6 = max(sdata_row6);
sdata_peak7 = max(sdata_row7);
sdata_peak8 = max(sdata_row8);
sdata_peak9 = max(sdata_row9);
sdata_peak10 = max(sdata_row10);
sdata_peak11 = max(sdata_row11);
sdata_peak12 = max(sdata_row12);
sdata_peak13 = max(sdata_row13);
sdata_peak14 = max(sdata_row14);
sdata_peak15 = max(sdata_row15);
sdata_peak16 = max(sdata_row16);

fdata_row1 = (fdata(:,1))';
fdata_row2 = (fdata(:,2))';
fdata_row3 = (fdata(:,3))';
fdata_row4 = (fdata(:,4))';
fdata_row5 = (fdata(:,5))';
fdata_row6 = (fdata(:,6))';
fdata_row7 = (fdata(:,7))';
fdata_row8 = (fdata(:,8))';
fdata_row9 = (fdata(:,9))';
fdata_row10 = (fdata(:,10))';
fdata_row11 = (fdata(:,11))';
fdata_row12 = (fdata(:,12))';
fdata_row13 = (fdata(:,13))';
fdata_row14 = (fdata(:,14))';
fdata_row15 = (fdata(:,15))';
fdata_row16 = (fdata(:,16))';

fdata_peak1 = max(fdata_row1);
fdata_peak2 = max(fdata_row2);
fdata_peak3 = max(fdata_row3);
fdata_peak4 = max(fdata_row4);
fdata_peak5 = max(fdata_row5);
fdata_peak6 = max(fdata_row6);
fdata_peak7 = max(fdata_row7);
fdata_peak8 = max(fdata_row8);
fdata_peak9 = max(fdata_row9);
fdata_peak10 = max(fdata_row10);
fdata_peak11 = max(fdata_row11);
fdata_peak12 = max(fdata_row12);
fdata_peak13 = max(fdata_row13);
fdata_peak14 = max(fdata_row14);
fdata_peak15 = max(fdata_row15);
fdata_peak16 = max(fdata_row16);

peak1 = fdata_peak1 / sdata_peak1;
peak2 = fdata_peak2 / sdata_peak2;
peak3 = fdata_peak3 / sdata_peak3;
peak4 = fdata_peak4 / sdata_peak4;
peak5 = fdata_peak5 / sdata_peak5;
peak6 = fdata_peak6 / sdata_peak6;
peak7 = fdata_peak7 / sdata_peak7;
peak8 = fdata_peak8 / sdata_peak8;
peak9 = fdata_peak9 / sdata_peak9;
peak10 = fdata_peak10 / sdata_peak10;
peak11 = fdata_peak11 / sdata_peak11;
peak12 = fdata_peak12 / sdata_peak12;
peak13 = fdata_peak13 / sdata_peak13;
peak14 = fdata_peak14 / sdata_peak14;
peak15 = fdata_peak15 / sdata_peak15;
peak16 = fdata_peak16 / sdata_peak16;

x = tau * 4 : tau * 4: (tau * 2 * (num_even_echos * 2));

x_sqr = x .* x;

y1 = [peak2, peak4, peak6, peak8, peak10];

xy1 = x .* y1;

sum_x = sum(x);

sum_x_sqr = sum(x_sqr);

sqr_sum_x = (sum_x)^2;

sum_y1 = sum(y1);

sum_xy1 = sum(xy1);

delta = (num_even_echos * sum_x_sqr) - sqr_sum_x;

A = ((sum_x_sqr * sum_y1) - (sum_x * sum_xy1)) / delta;

B = ((num_even_echos * sum_xy1) - (sum_x * sum_y1)) / delta;

neg_BA_ratio = (-1) * (B / A);

disp(['-(B/A) = ' num2str(neg_BA_ratio)]);




























