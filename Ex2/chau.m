function y = chau(x,j)
  y = zeros(1,length(x));
  y = 20/((2*j-1)*pi*sqrt(power((2*j-1),2)+1))*cos(2*pi*(2*j-1)*x-atan((2*j-1))+pi/2); 
endfunction