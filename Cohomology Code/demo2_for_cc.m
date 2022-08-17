% Demo script 2 for circular coordinates
%
% This script carries out the following steps:
%
% 1. Creates a time-series signal
% 2. Converts it to point-cloud data, using Takens delay embedding
% 3. Computes the persistence diagram.
% 4. Asks the user to select a quadrant in the persistence diagram.
% 5. Asks the user to select a point in the quadrant.
% 6. Converts the corresponding cocycle to a circle-valued function.
% 7. Plots the "circular coordinate" against time.
% 8. "Unrolls" the circular coordiate to a real-valued function.
%
% For a clean periodic signal, the slope of the unrolled coordinate is
% equal to the number of cycles per second.
%
%[VdS 2017-april-26]


% generate signal
T0 = (0: 0.1: 100);
N0 = length(T0);
F = sin(T0) + 0.2 * randn(1,N0);

% Takens delay embedding
delays = [0 7 12];
nd = length(delays);
N = N0 - max(delays);

X = zeros(nd, N);
for a = (1: nd)
    X(a, :) = F(delays(a)+(1:N));
end
T = T0(1:N);

% select landmarks
nL = 30;
[L, DL, RL] = px_maxmin(X, 'vector', nL, 'n');
DLL = DL(:,L);

% construct VR-complex (edges only)
R = RL * 4;
Edges = cc_edges(DLL, R);

% persistent cohomology calculation
[C0, C1, I0, I1] = cc_cocycles(Edges, 47);

% select one cocycle
[Rcc, Kcc] = cc_select(I1,1);

% calculate circular coordinates on landmarks
ThetaL = cc_theta(Edges, C1, 47, Rcc, Kcc);

% extend to whole data
ThetaX = cc_interpolate_theta(ThetaL, DL, L);

%% plot results
figure(147), clf

% colours represent circular coordinate
subplot(4,8,[1 28])
ncol = 64;
hsv_map = hsv(ncol);
HX = zeros(1,N);
for b = (1: N)
   HX(b) = plot(X(1,b), X(2,b), '.');
   set(HX(b), 'color', hsv_map(1+floor(ThetaX(b)*ncol),:));
   hold on
end
title('delay embedding coordinates 1 & 2')

%
subplot(4,8,[5 8])
plot(T0,F,'.k');
title('original signal')


%
subplot(4,8,[13 16])
plot(T,ThetaX,'.');
title('circular coordinate')

%
UThetaX = ThetaX;
UThetaX(:, 2:end) = UThetaX(:, 2:end) ...
    - cumsum(round(diff(UThetaX,[],2)),2);

subplot(4,8,[21 32])
plot(T,UThetaX,'.');
title('unrolled coordinate')

