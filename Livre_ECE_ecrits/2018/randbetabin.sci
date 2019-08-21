function x = randbetabin(a,b)
    x = zeros(1,2) ;
    u = (a+b)*rand() ;
    v = (a+b+1)*rand() ;
    if (u < a) then
        x(1,1) = 1 ;
        if (v < a+1) then 
            x(1,2) = 1 ;
        end ;
    else if (v < a) then
            x(1,2) = 1 ;
        end ;
    end ;
endfunction
