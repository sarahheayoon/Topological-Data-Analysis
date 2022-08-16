function Edges = cc_edges(D, R)

%CC_EDGES -- convert distance matrix into sorted list of edges
%
%   Edges = cc_edges(D, R);
%
%The structured array Edges is intended to be used as input into the
%function cc_cocycles which calculated cohomology in dimension 1.
%
%Input:
%   D    n-by-n    distance matrix
%   R    scalar    maximum edge length
%
%Output:
%   Edges         <structured array>
%   Edges.n       scalar    number of vertices, n
%   Edges.m       scalar    number of edges, m
%   Edges.V       2-by-m    1st and 2nd vertex of each edge
%   Edges.D       1-by-m    length of each edge
%   Edges.lookup  n-by-n    sparse lookup table for edge indices
%
%The lookup table functions as follows. If [p,q] is an edge then
%
%   a = Edges.lookup(p,q)
%
%is the index for which
%
%   Edges.V(1,a)
%   Edges.V(2,a)
%
%respectively return p and q.
%
%[Vin de Silva, 2015-04-29]

if ~isequal(D,D')
    error('Distance matrix must be symmetrix')
end

n = size(D,1);

[I,J] = find(D <= R);
IlessJ = (I < J);
I = I(IlessJ);
J = J(IlessJ);

m = length(I);

[DS, S] = sort(D(sub2ind([n n], I, J)));

I = I(S);
J = J(S);
IJ2ind = sparse(I, J, (1:m), n, n);

% collate output
Edges.n = n;
Edges.m = m;
Edges.V = [I'; J'];
Edges.D = DS';
Edges.lookup = IJ2ind;

return


