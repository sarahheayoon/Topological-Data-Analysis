function [C0, C1, I0, I1] = cc_cocycles(Edges, p)

%CC_COCYCLES -- persistent cohomology of a weighted graph
%
%   [C0, C1, I0, I1] = cc_cocycles(Edges, p)
%
%Given a collection of edges with lengths, calculate the persistent
%cohomology in dimensions 0 and 1 of the corresponding 2-dimensional
%filtered simplicial complex. The input argument Edges is of the form
%produced by the function cc_edges in this library.
%
%Input:
%   Edges         <structured array>
%   Edges.n       scalar    number of vertices, n
%   Edges.m       scalar    number of edges, m
%   Edges.V       2-by-m    1st and 2nd vertex of each edge
%   Edges.D       1-by-m    length of each edge
%   Edges.lookup  n-by-n    sparse lookup table for edge indices
%
%   p             scalar    prime number
%
%Output:
%   C0            n-by-n    0-cochains for persistence basis
%   C1            m-by-m    1-cochains for persistence basis
%   I0            2-by-n    persistence interval for each vertex
%   I1            2-by-m    persistence interval for each edge
%
%Each vertex enters the filtration at parameter 0. The a-th edge enters the
%filtration at parameter Edges.D(a). Triangles enter as soon as they can
%(i.e. when all three edges are in).
%
%Persistence intervals for the vertices are of the form [0; t]. Edges that
%are immediately trivial in cohomology have interval [NaN; NaN].
%
%[Vin de Silva, 2015-04-29]

if (nargin < 2)
    error('Two input arguments required.')
end

if ~isprime(p)
   error('The second argument p must be a prime number.') 
end

%% collate input variables
n = Edges.n;
m = Edges.m;

I = Edges.V(1,:);
J = Edges.V(2,:);
IJ2ind = Edges.lookup;

DS = Edges.D;

%% arithmetic tables (mod p)

% multiplication
Mp = mod((0:p-1)'*(0:p-1),p);

% inverses
[Ip,~] = find(Mp(2:end,2:end) == 1);

%% initialise
C0 = speye(n,n);    % list of 0-cochains
C1 = speye(m,m);    % list of 1-cochains

H0 = repmat(true, [1 n]);   % active 0-coclasses (logical)
H1 = repmat(false, [1, m]); % active 1-coclasses (logical)

I0 = repmat([0; Inf], [1 n]);    % 0-persistence intervals
I1 = repmat(NaN, [2 m]);         % 1-persistence intervals

Ga = logical(sparse(n,n)); % edges used so far

cb0 = zeros(1,n);   % 0-boundary workspace
cb1 = zeros(1,m);   % 1-boundary workspace

%% main loop

disp(sprintf('[%d vertices, %d edges]', n, m))
tstart = tic;
tsec = 1;

for a = (1: m)
    
    % the next edge to be processed: [Ia,Ja]
    Ia = I(a);
    Ja = J(a);
    
    % find triangles
    Ka_list = find(Ga(:,Ia) & Ga(:,Ja));

    % update graph
    Ga(Ia,Ja) = true; Ga(Ja,Ia) = true;

    if isempty(Ka_list);
    % no new triangles

        % which 0-cocycles now fail?
        
        cb0(H0)  = mod(C0(Ja,H0)-C0(Ia,H0),p);
        % cb0(~H0) = 0;      % (already enforced on pivot deletion)
        cb0find = find(cb0);
        
        if isempty(cb0find)
            % new 1-coclass
            H1(a) = true;
            I1(:,a) = [DS(a); Inf];
            
        else
            % most recent affected 0-coclass disappears
            % earlier affected 0-coclasses adjusted
            pivot = cb0find(end);
            others = cb0find(1: end-1);

            pivotvalue = cb0(pivot);
            othervalues = cb0(others);

            % eliminate pivot from coclass list
            H0(pivot) = false;
            cb0(pivot) = 0;
            I0(2,pivot) = DS(a);
            
            % adjust earlier entries
            pivotcolumn = Mp(C0(:, pivot)+1, Ip(pivotvalue)+1);
            
            C0(:, others) =...
                mod( C0(:, others) - Mp(pivotcolumn+1, othervalues+1), p);
            %pcnz = find(pivotcolumn);
            %C0(pcnz, others) =...
            %    mod( C0(pcnz, others) - Mp(pivotcolumn(pcnz)+1, othervalues+1), p);

        end
        
        
    else
    % one or more new triangles

    % new edge creates a cocycle
        H1(a) = true;
        I1(1,a) = DS(a);

        % process each new triangle
        for b = 1: length(Ka_list)
           Ka = Ka_list(b);
   
           % identify the edges of the triangle
           if (Ka < Ia)
               E0 = IJ2ind(Ia,Ja);
               E1 = IJ2ind(Ka,Ja);
               E2 = IJ2ind(Ka,Ia);
           elseif (Ja < Ka)
               E0 = IJ2ind(Ja,Ka);
               E1 = IJ2ind(Ia,Ka);
               E2 = IJ2ind(Ia,Ja);               
           else
               E0 = IJ2ind(Ka,Ja);
               E1 = IJ2ind(Ia,Ja);
               E2 = IJ2ind(Ia,Ka);                              
           end
                      
           % which 1-cocycles now fail?

           cb1(H1) = mod(C1(E0,H1) - C1(E1,H1) + C1(E2,H1), p);
           % cb1(~H1) = 0;      % (already enforced on pivot deletion)
           cb1find = find(cb1);
           
           if isempty(cb1find)
               % new 2-coclass
               % do nothing, since we are not tracking 2-coclasses
               
           else
               % most recent affected 1-coclass disappears
               % earlier affected 1-coclasses adjusted
               
               pivot = cb1find(end);
               others = cb1find(1: end-1);
               
               pivotvalue = cb1(pivot);
               othervalues = cb1(others);
               
               % eliminate pivot from coclass list
               H1(pivot) = false;
               cb1(pivot) = 0;
               I1(2,pivot) = DS(a);
               
               % adjust earlier entries
               pivotcolumn = Mp(C1(:, pivot)+1, Ip(pivotvalue)+1);            

               C1(:, others) =...
                   mod( C1(:, others) - Mp(pivotcolumn+1, othervalues+1), p);
               %pcnz = find(pivotcolumn);
               %C1(pcnz, others) =...
               %    mod( C1(pcnz, others) - Mp(pivotcolumn(pcnz)+1, othervalues+1), p);
           end
           
        end
    end
    
    % indicate progress every second
    if (toc(tstart) > tsec)
        fprintf(' %d', a)
        if ~mod(tsec,10)
            fprintf(': %ds\n', tsec)
        end
        tsec = tsec + 1;
    end
    
end
fprintf('\n')

%%
return




