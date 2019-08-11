function y = hola(x,j)
  y = zeros(1,length(x));
  y = 20/((2*j-1)*pi)*sin(2*pi*(2*j-1) * x);
 endfunction;