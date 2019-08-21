n=6;
lambda = 0.2;
alpha = 50;
x=0.5:.1:50;
l = length(x);

s=zeros(1,l);
//for i = 1:l
//    s(i) = (n-1)*lambda*x(i)/((n-1)*lambda +1);
//end

for i = 1:l
    s(i) = sigma(x(i),n,alpha,lambda);
end

clf()
plot(x,s,color='black', 'Linewidth', 2)
//plot(x,0.5*x, color = 'blue', 'Linewidth', 2)
