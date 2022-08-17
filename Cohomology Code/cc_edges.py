# Generated with SMOP  0.41
from libsmop import *
# cc_edges.m

    
@function
def cc_edges(D=None,R=None,*args,**kwargs):
    varargin = cc_edges.varargin
    nargin = cc_edges.nargin

    #CC_EDGES -- convert distance matrix into sorted list of edges
    
    #   Edges = cc_edges(D, R);
    
    #The structured array Edges is intended to be used as input into the
#function cc_cocycles which calculated cohomology in dimension 1.
    
    #Input:
#   D    n-by-n    distance matrix
#   R    scalar    maximum edge length
    
    #Output:
#   Edges         <structured array>
#   Edges.n       scalar    number of vertices, n
#   Edges.m       scalar    number of edges, m
#   Edges.V       2-by-m    1st and 2nd vertex of each edge
#   Edges.D       1-by-m    length of each edge
#   Edges.lookup  n-by-n    sparse lookup table for edge indices
    
    #The lookup table functions as follows. If [p,q] is an edge then
    
    #   a = Edges.lookup(p,q)
    
    #is the index for which
    
    #   Edges.V(1,a)
#   Edges.V(2,a)
    
    #respectively return p and q.
    
    #[Vin de Silva, 2015-04-29]
    
    if logical_not(isequal(D,D.T)):
        error('Distance matrix must be symmetrix')
    
    n=size(D,1)
# cc_edges.m:39
    I,J=find(D <= R,nargout=2)
# cc_edges.m:41
    IlessJ=(I < J)
# cc_edges.m:42
    I=I(IlessJ)
# cc_edges.m:43
    J=J(IlessJ)
# cc_edges.m:44
    m=length(I)
# cc_edges.m:46
    DS,S=sort(D(sub2ind(concat([n,n]),I,J)),nargout=2)
# cc_edges.m:48
    I=I(S)
# cc_edges.m:50
    J=J(S)
# cc_edges.m:51
    IJ2ind=sparse(I,J,(arange(1,m)),n,n)
# cc_edges.m:52
    # collate output
    Edges.n = copy(n)
# cc_edges.m:55
    Edges.m = copy(m)
# cc_edges.m:56
    Edges.V = copy(concat([[I.T],[J.T]]))
# cc_edges.m:57
    Edges.D = copy(DS.T)
# cc_edges.m:58
    Edges.lookup = copy(IJ2ind)
# cc_edges.m:59
    return Edges