function [] = test()
  clear all;
  clc;
  x = 0:1/100:1;
  y = zeros(1,length(x));
  y = hola(x,1);
  plot(x,y);
  hold on;
  for  k =2:10
    y = y + hola(x,k);
    plot(x,y);
    endfor
    grid minor;
    title("Señal de entrada de 1 a 100 armonicos");
    xlabel("tiempo/período");
    ylabel("Tensión");
endfunction
