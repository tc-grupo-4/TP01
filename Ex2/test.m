function [] = test()
  clear all;
  clc;
  x = 0:2/1000:2;
  y = zeros(1,length(x));
  y = hola(x,1);
  %plot(x,y,'k');
  hold on;
    for  k =2:1000
    y = y + hola(x,k);
    %plot(x,y,'k');
    endfor
  grid on;
  plot(x,y,'k');
  title("Input Signal de 1 a 100 armonicos");
  xlabel("tiempo/periodo");
  ylabel("Tension");
endfunction
