# Generated with SMOP  0.41
from libsmop import *
# cc_cocycles.m

    
@function
def cc_cocycles(Edges=None,p=None,*args,**kwargs):
    varargin = cc_cocycles.varargin
    nargin = cc_cocycles.nargin

    #CC_COCYCLES -- persistent cohomology of a weighted graph
    
    #   [C0, C1, I0, I1] = cc_cocycles(Edges, p)
    
    #Given a collection of edges with lengths, calculate the persistent
#cohomology in dimensions 0 and 1 of the corresponding 2-dimensional
#filtered simplicial complex. The input argument Edges is of the form
#produced by the function cc_edges in this library.
    
    #Input:
#   Edges         <structured array>
#   Edges.n       scalar    number of vertices, n
#   Edges.m       scalar    number of edges, m
#   Edges.V       2-by-m    1st and 2nd vertex of each edge
#   Edges.D       1-by-m    length of each edge
#   Edges.lookup  n-by-n    sparse lookup table for edge indices
    
    #   p             scalar    prime number
    
    #Output:
#   C0            n-by-n    0-cochains for persistence basis
#   C1            m-by-m    1-cochains for persistence basis
#   I0            2-by-n    persistence interval for each vertex
#   I1            2-by-m    persistence interval for each edge
    
    #Each vertex enters the filtration at parameter 0. The a-th edge enters the
#filtration at parameter Edges.D(a). Triangles enter as soon as they can
#(i.e. when all three edges are in).
    
    #Persistence intervals for the vertices are of the form [0; t]. Edges that
#are immediately trivial in cohomology have interval [NaN; NaN].
    
    #[Vin de Silva, 2015-04-29]
    
    if (nargin < 2):
        error('Two input arguments required.')
    
    if logical_not(isprime(p)):
        error('The second argument p must be a prime number.')
    
    ## collate input variables
    n=Edges.n
# cc_cocycles.m:46
    m=Edges.m
# cc_cocycles.m:47
    I=Edges.V(1,arange())
# cc_cocycles.m:49
    J=Edges.V(2,arange())
# cc_cocycles.m:50
    IJ2ind=Edges.lookup
# cc_cocycles.m:51
    DS=Edges.D
# cc_cocycles.m:53
    ## arithmetic tables (mod p)
    
    # multiplication
    Mp=mod(dot((arange(0,p - 1)).T,(arange(0,p - 1))),p)
# cc_cocycles.m:58
    # inverses
    Ip,__=find(Mp(arange(2,end()),arange(2,end())) == 1,nargout=2)
# cc_cocycles.m:61
    ## initialise
    C0=speye(n,n)
# cc_cocycles.m:64
    
    C1=speye(m,m)
# cc_cocycles.m:65
    
    H0=repmat(true,concat([1,n]))
# cc_cocycles.m:67
    
    H1=repmat(false,concat([1,m]))
# cc_cocycles.m:68
    
    I0=repmat(concat([[0],[Inf]]),concat([1,n]))
# cc_cocycles.m:70
    
    I1=repmat(NaN,concat([2,m]))
# cc_cocycles.m:71
    
    Ga=logical(sparse(n,n))
# cc_cocycles.m:73
    
    cb0=zeros(1,n)
# cc_cocycles.m:75
    
    cb1=zeros(1,m)
# cc_cocycles.m:76
    
    ## main loop
    
    disp(sprintf('[%d vertices, %d edges]',n,m))
    tstart=copy(tic)
# cc_cocycles.m:81
    tsec=1
# cc_cocycles.m:82
    for a in (arange(1,m)).reshape(-1):
        # the next edge to be processed: [Ia,Ja]
        Ia=I(a)
# cc_cocycles.m:87
        Ja=J(a)
# cc_cocycles.m:88
        Ka_list=find(logical_and(Ga(arange(),Ia),Ga(arange(),Ja)))
# cc_cocycles.m:91
        Ga[Ia,Ja]=true
# cc_cocycles.m:94
        Ga[Ja,Ia]=true
# cc_cocycles.m:94
        if isempty(Ka_list):
            # which 0-cocycles now fail?
            cb0[H0]=mod(C0(Ja,H0) - C0(Ia,H0),p)
# cc_cocycles.m:101
            cb0find=find(cb0)
# cc_cocycles.m:103
            if isempty(cb0find):
                # new 1-coclass
                H1[a]=true
# cc_cocycles.m:107
                I1[arange(),a]=concat([[DS(a)],[Inf]])
# cc_cocycles.m:108
            else:
                # most recent affected 0-coclass disappears
            # earlier affected 0-coclasses adjusted
                pivot=cb0find(end())
# cc_cocycles.m:113
                others=cb0find(arange(1,end() - 1))
# cc_cocycles.m:114
                pivotvalue=cb0(pivot)
# cc_cocycles.m:116
                othervalues=cb0(others)
# cc_cocycles.m:117
                H0[pivot]=false
# cc_cocycles.m:120
                cb0[pivot]=0
# cc_cocycles.m:121
                I0[2,pivot]=DS(a)
# cc_cocycles.m:122
                pivotcolumn=Mp(C0(arange(),pivot) + 1,Ip(pivotvalue) + 1)
# cc_cocycles.m:125
                C0[arange(),others]=mod(C0(arange(),others) - Mp(pivotcolumn + 1,othervalues + 1),p)
# cc_cocycles.m:127
                #C0(pcnz, others) =...
            #    mod( C0(pcnz, others) - Mp(pivotcolumn(pcnz)+1, othervalues+1), p);
        else:
            # one or more new triangles
            # new edge creates a cocycle
            H1[a]=true
# cc_cocycles.m:140
            I1[1,a]=DS(a)
# cc_cocycles.m:141
            for b in arange(1,length(Ka_list)).reshape(-1):
                Ka=Ka_list(b)
# cc_cocycles.m:145
                if (Ka < Ia):
                    E0=IJ2ind(Ia,Ja)
# cc_cocycles.m:149
                    E1=IJ2ind(Ka,Ja)
# cc_cocycles.m:150
                    E2=IJ2ind(Ka,Ia)
# cc_cocycles.m:151
                else:
                    if (Ja < Ka):
                        E0=IJ2ind(Ja,Ka)
# cc_cocycles.m:153
                        E1=IJ2ind(Ia,Ka)
# cc_cocycles.m:154
                        E2=IJ2ind(Ia,Ja)
# cc_cocycles.m:155
                    else:
                        E0=IJ2ind(Ka,Ja)
# cc_cocycles.m:157
                        E1=IJ2ind(Ia,Ja)
# cc_cocycles.m:158
                        E2=IJ2ind(Ia,Ka)
# cc_cocycles.m:159
                # which 1-cocycles now fail?
                cb1[H1]=mod(C1(E0,H1) - C1(E1,H1) + C1(E2,H1),p)
# cc_cocycles.m:164
                cb1find=find(cb1)
# cc_cocycles.m:166
                if isempty(cb1find):
                    # new 2-coclass
               # do nothing, since we are not tracking 2-coclasses
                    pass
                else:
                    # most recent affected 1-coclass disappears
               # earlier affected 1-coclasses adjusted
                    pivot=cb1find(end())
# cc_cocycles.m:176
                    others=cb1find(arange(1,end() - 1))
# cc_cocycles.m:177
                    pivotvalue=cb1(pivot)
# cc_cocycles.m:179
                    othervalues=cb1(others)
# cc_cocycles.m:180
                    H1[pivot]=false
# cc_cocycles.m:183
                    cb1[pivot]=0
# cc_cocycles.m:184
                    I1[2,pivot]=DS(a)
# cc_cocycles.m:185
                    pivotcolumn=Mp(C1(arange(),pivot) + 1,Ip(pivotvalue) + 1)
# cc_cocycles.m:188
                    C1[arange(),others]=mod(C1(arange(),others) - Mp(pivotcolumn + 1,othervalues + 1),p)
# cc_cocycles.m:190
                    #C1(pcnz, others) =...
               #    mod( C1(pcnz, others) - Mp(pivotcolumn(pcnz)+1, othervalues+1), p);
        # indicate progress every second
        if (toc(tstart) > tsec):
            fprintf(' %d',a)
            if logical_not(mod(tsec,10)):
                fprintf(': %ds\n',tsec)
            tsec=tsec + 1
# cc_cocycles.m:206
    
    fprintf('\n')
    ##
    return C0,C1,I0,I1