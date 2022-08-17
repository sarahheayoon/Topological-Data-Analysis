function [Rcc, Kcc] = cc_select(I1, ncc, Ha)

%CC_SELECT -- select (co)cycles by clicking on persistence diagram
%
%   [Rcc, Kcc] = cc_select(I1, ncc);
%
%Input:
%   I1     2-by-m    persistence intervals
%   ncc    scalar    number of (co)cycles wanted (default 1)
%
%Output:
%   Rcc    scalar    persistence index at which (co)cycles are sought
%   Kcc    1-by-ncc  index values of the chosen cocycles
%
%The first click selects a point on the diagonal. Subsequent clicks select
%indices for the the desired (co)cycles. If there are no cocycles in the
%chosen quadrant then Kcc = NaN.
%
%This function depends on px_homologyplot.m to draw the persistence
%diagram.
%
%[Vin de Silva, 2015-04-29]

if (nargin < 1)
    ncc = 1;
end

if (nargin <= 2)
    HF = figure;
else
    axes(Ha);
end
HaPD = px_homologyplot({I1,I1}, 1,'scatter');

% begin by selecting a quadrant
[u,v] = ginput(1);
Rcc = (u+v)/2;

PDlim = get(HaPD, 'xlim');
PDmin = PDlim(1);
PDmax = PDlim(2);

hold on
Hcensor = patch(...
    [PDmin, PDmin, Rcc, Rcc, PDmax], ...
    [PDmin, Rcc, Rcc, PDmax, PDmax], ...
    [0.5, 0.1 0.1], 'facealpha', 0.5);

% which points of the diagram lie in the quadrant?
PDquadlist = find((I1(1,:) < Rcc) & (I1(2,:) > Rcc));

if isempty(PDquadlist)
    disp('No cocycles in chosen quadrant.')
    Kcc = NaN;
    return
end

PDquad = I1(:, PDquadlist);
PDquad(PDquad == inf) = PDmax;
PDquad(PDquad == -inf) = PDmin;

% select the desired number of points
Kcc = zeros(1,ncc);
for a = (1: ncc)
    [u,v] = ginput(1);
    [~,PDclosest] = min((PDquad(1,:)-u).^2 + (PDquad(2,:)-v).^2);
    Kcc(a) = PDquadlist(PDclosest);
    Hchosen = plot(PDquad(1,PDclosest), PDquad(2,PDclosest), '*r');
end

if (nargin <= 2)
    close(HF)
end

%%
return



