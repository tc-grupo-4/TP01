function [] = out()
  clear all;
  clc;
  x = 0:2/200:2;
  y = zeros(1,length(x));
  y = chau(x,1);
  plot(x,y,'k');
  hold on;
  for  k =2:100
    y = y + chau(x,k);
    plot(x,y,'k');
    endfor
    grid on;
    title("Output Signal de 1 a 100 armonicos");
    xlabel("tiempo/periodo");
    ylabel("Tension");
  
  
endfunction