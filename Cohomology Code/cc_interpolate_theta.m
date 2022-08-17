function ThetaX = cc_interpolate_theta(ThetaL, DL, L);

%CC_INTERPOLATE_THETA -- interpolate circle-valued functions
%
%   ThetaX = cc_interpolate(ThetaL, DL, L);
%
%This extends the definition of circle-valued functions ThetaL(a,:)
%defined on landmark points to circle-valued functions ThetaX(a,:)
%defined on the whole data.
%
%Input:
%   ThetaL   ncc-by-n   each row is a circle-function on n landmarks
%   DL       n-by-N     landmark-to-data distance matrix
%   L        1-by-n     indices of landmarks in data
%
%[Vin de Silva, 2015-04-29]

ThetaL = mod(ThetaL,1);

n = size(DL,1);
N = size(DL,2);

[DLsort, DLsortI] = sort(DL, 1, 'ascend');

% indices for nearest 2 landmarks
DLL = DL(:, L);
Dab = DLL(sub2ind([n n], DLsortI(1,:), DLsortI(2,:))).^2;
Dxa = DLsort(1,:).^2;
Dxb = DLsort(2,:).^2;

% interpolation coefficients using those two landmarks 
inter2C = zeros(2,N);
inter2C(1,:) = [(0.5) + (Dxb - Dxa)./(2*Dab)];
inter2C(2,:) = 1 - inter2C(1,:);

ncc = size(ThetaL, 1);
ThetaX = zeros(ncc, N);

for a = (1: ncc)
    ThetaXL = [ThetaL(a,DLsortI(1,:)); ThetaL(a,DLsortI(2,:))];
    ThetaXL(2,:) = ThetaXL(2,:) - round(diff(ThetaXL,1));
    ThetaX(a,:) = mod(sum(inter2C .* ThetaXL, 1), 1);
end

