function q = qmatrix(n)
    q = ones(n,n) ;
    for L = 2:n
        for K = 2:n
            if (K<L) then 
                q(L,K) = q(L-1,K) ;
            else if (K==L) then 
                    q(L,K) = q(L-1,K) + 1 ;
                else 
                    q(L,K) = q(L-1,K) + q(L,K-L)
                end
            end
        end
    end
endfunction
