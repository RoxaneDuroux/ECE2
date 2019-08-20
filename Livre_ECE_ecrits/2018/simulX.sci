function x = simulX(n, alpha, lambda)
    x = zeros(1,n);
    for k=1:n
       u = rand()
       x(k) = alpha * u^(1/lambda) 
    end
endfunction
