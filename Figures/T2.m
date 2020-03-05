x=0:0.01:1000;
y=10*sin(1000*x).*exp(-0.003*x).*exp(-3*sin(0.1*x));
y1=200.9*exp(-0.003*x);

hold on
plot(x,y)
plot(x,y1, 'LineWidth', 3);


