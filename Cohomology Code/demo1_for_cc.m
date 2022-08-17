% Demo script 1 for circular coordinates
%
% This script carries out the following steps:
%
% 1. Creates point-cloud dataset.
% 2. Computes the persistence diagram.
% 3. Asks the user to select a quadrant in the persistence diagram.
% 4. Asks the user to select a point in the quadrant.
% 5. Converts the corresponding cocycle to a circle-valued function.
% 6. Displays the function using a colour plot.
% 7. Repeats, as requested.
%
%[VdS 2017-april-26]


% generate data
N = 400;
t = rand(1,N);
x = cos(2*pi*t);
y = sin(2*pi*t) + sign(randn(1,N));

X = [x; y] + (0.1)*randn(2,N);
clear t x y

% set up figure
figure(47), clf
set(47, 'name', 'keyboard to quit, mouse to continue');
Ha = subplot(1,2,2);

% display data in monochrome
subplot(1,2,1)
plot(X(1,:), X(2,:), 'k.');
axis equal
title('PCD coordinates 1 & 2')


% select landmarks
nL = 50;
[L, DL, RL] = px_maxmin(X, 'vector', nL, 'n');
DLL = DL(:,L);

% construct VR-complex (edges only)
R = RL * 4;
Edges = cc_edges(DLL, R);

% persistent cohomology calculation (mod 47)
[C0, C1, I0, I1] = cc_cocycles(Edges, 47);


finish = 0;
while ~finish

    % select one cocycle
    
    %[Rcc, Kcc] = cc_select(I1,1);
    [Rcc, Kcc] = cc_select(I1,1,Ha);
    % (Ha option specifies a display axis)
    

    % calculate circular coordinates on landmarks
    ThetaL = cc_theta(Edges, C1, 47, Rcc, Kcc);

    % extend to whole data
    ThetaX = cc_interpolate_theta(ThetaL, DL, L);

    
    % plot data in colour
    figure(47)
    subplot(1,2,1)
    ncol = 64;
    hsv_map = hsv(ncol);
    HX = zeros(1,N);
    for b = (1: N)
        HX(b) = plot(X(1,b), X(2,b), '.');
        set(HX(b), 'color', hsv_map(1+floor(ThetaX(b)*ncol),:));
        hold on
    end
    axis equal
    title('PCD coordinates 1 & 2')
    
    % continue (mouse-click) or exit (keyboard)
    finish = waitforbuttonpress;

end

