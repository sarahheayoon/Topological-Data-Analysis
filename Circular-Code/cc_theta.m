function Theta = cc_theta(Edges, C1, p, Rcc, Kcc)

%CC_THETA -- construct circular coordinates
%
%Calculate the circular coordinates associated to a given collection of
%cocycles (mod p). The prime p must be specified.
%
%   Theta = cc_theta(Edges, C1, p, Rcc, Kcc)
%
%Input:
%   Edges    <structured array>
%   C1       m-by-m       persistent cochain basis
%   p        scalar       prime modulus by which C1 was calculated
%   Rcc      scalar       filtration parameter
%   Kcc      1-by-ncc     indices for the ncc chosen cocycles
%
%Output:
%   Theta    ncc-by-m     circular coordinates (values in [0,1)).
%
%Although the cocycles are typically chosen persistently, the calculation
%takes place in a fixed simplicial complex specified by Rcc.
%
%[Vin de Silva, 2015-04-19]

% construct coboundary matrix up to Rips parameter Rf
af = sum(Edges.D <= Rcc);
%find(DS <= Rf, 1, 'last');

D0 = sparse((1:af), Edges.V(2,(1:af)), 1, af, Edges.n) ...
    + sparse((1:af), Edges.V(1,(1:af)), -1, af, Edges.n);

ncc = length(Kcc);
Theta = zeros(ncc, Edges.n);

for a = (1: ncc)
    % extract the significant cocycles, lift to integer coefficients
    C1f = C1((1:af), Kcc(a));
    C1f = mod(C1f+(p-1)/2, p) - (p-1)/2;

    % smooth the integer 1-cocycles and reduce mod 1
    theta = lsqr(D0, C1f, [], 100);
    Theta(a,:) = mod(theta,1);

end
