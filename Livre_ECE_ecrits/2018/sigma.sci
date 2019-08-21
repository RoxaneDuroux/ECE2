function s = sigma(x,n,alpha,lambda)
    N = 10000;
    Y = zeros(1,N);
    for k=1:N
        X = simulX(n-1,alpha,lambda);
        Y(k) = max(X);
    end
    E = sum(Y(Y<=x))/N;
    P = sum(Y<=x)/N;
    s = E/P
endfunction
