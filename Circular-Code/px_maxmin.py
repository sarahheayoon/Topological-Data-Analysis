# Generated with SMOP  0.41
from libsmop import *
# px_maxmin.m

    
@function
def px_maxmin(varargin=None,*args,**kwargs):
    varargin = px_maxmin.varargin
    nargin = px_maxmin.nargin

    #PX_MAXMIN -- select landmark points by greedy optimisation
    
    # Given a set of N points, PX_MAXMIN selects a subset of n points called
# 'landmark' points by an interative greedy optimisation. Specifically,
# when j landmark points have been chosen, the (j+1)-st landmark point
# maximises the function 'minimum distance to an existing landmark point'.
    
    # The initial landmark point is arbitrary, and may be chosen randomly or
# by decree. More generally, the process can be 'seeded' by up to k
# landmark points chosen randomly or by decree.
    
    # The input data can belong to one of the following types:
    
    #    'vector': set of d-dimensional Euclidean points passed to the
#              function as d-by-N matrix
    
    #    'metric': N-by-N matrix of distances
    
    #    'rows': function handle with one vector argument I=[i1,i2,...,ip]
#              which returns a p-by-N matrix of distances between the p
#              specified points and the full data set.
    
    # The output L is a list of indices for the landmark points, presented in
# the order of discovery. User-specified seeds are listed first, followed
# by randomly chosen seeds.
    
    # A second output argument, DL, returns the n-by-N matrix of distances
# between landmark points and all data points.
    
    # A third output argument, R, returns the covering number of the landmark
# set. R is the smallest number such that every data point lies within
# distance R of a landmark point.
    
    # Syntax:
    
    # L          = PX_MAXMIN(data1, type1, data2, type2, ...);
# [L, DL]    = PX_MAXMIN(data1, type1, data2, type2, ...);
# [L, DL, R] = PX_MAXMIN(data1, type1, data2, type2, ...);
    
    # Each pair (data, type) is one of the following:
    
    #  (X, 'vector'), (D, 'metric'), (fD,'rows')
    
    #  (n, 'n')     -- number of landmarks
    
    #  (S, 'seeds') -- list of seeds specified by the user; no repeats are
#                  allowed.
    
    #  (k, 'rand')  -- number of randomly chosen seeds
    
    # The pairs may be listed in any order. The type strings are sensitive to
# case. Exactly one of {X, D, fD} must be specified, and n must always be
# specified.
    
    # Both of {k, S} are optional arguments. If S is specified, and is not
# the empty list, then k=0 is the default. Otherwise, the defaults are
# k=1, S=[].
    
    # The function PX_LANDMARKD is a C++ version of PX_MAXMIN and may be used
# instead. The syntax and functionality are slightly different.
    
    #Plex Metric Data Toolbox version 2.0 by Vin de Silva, Patrick Perry and
#contributors. See PX_PLEXINFO for credits and licensing information.
#Released with Plex version 2.0. [2004-October-17]
    
    # [2004-May-06] Modifications:
#               -replacing @local_euclid with @local_euclid2
#               -returning R as an output argument
    
    # [2004-May-24] -speed up 'min' step using incremental updates.
#               -R now returns the *next* value of MaxMin.
    
    # [2004-Apr-28] Vin de Silva, Department of Mathematics, Stanford.
    
    #----------------------------------------------------------------
# collate the input variables
#----------------------------------------------------------------
    
    types=cellarray(['vector','metric','rows','n','seeds','rand'])
# px_maxmin.m:81
    if any(logical_not(ismember(varargin(arange(2,end(),2)),types))):
        error('Invalid data type specified.')
    
    if (nargin != (dot(2,length(unique(varargin(arange(2,end(),2))))))):
        error('Repeated or missing data types.')
    
    isused,input_ix=ismember(types,varargin(arange(2,end(),2)),nargout=2)
# px_maxmin.m:91
    if (sum(isused(arange(1,3))) != 1):
        error('Points must be specified in exactly one of the given formats.')
    
    if logical_not(isused(4)):
        error('Number of landmarks must be specifed.')
    
    #----------------------------------------------------------------
# standardize the input
#----------------------------------------------------------------
    
    #------------------------------------------------
# By the end of this section, feval(Dfun,list) 
# will return D(list,:), whichever the input
# format of the data
#------------------------------------------------
    
    dataformat=find(isused(arange(1,3)))
# px_maxmin.m:111
    
    # entered in?
    if 1 == dataformat:
        X=varargin[dot(2,input_ix(1)) - 1]
# px_maxmin.m:115
        d,N=size(X,nargout=2)
# px_maxmin.m:116
        L2sq=sum(X ** 2,1)
# px_maxmin.m:120
        Dfun=local_euclid2
# px_maxmin.m:121
    else:
        if 2 == dataformat:
            D=varargin[dot(2,input_ix(2)) - 1]
# px_maxmin.m:124
            N=length(D)
# px_maxmin.m:125
            Dfun=local_submatrix
# px_maxmin.m:126
        else:
            if 3 == dataformat:
                Dfun=varargin[dot(2,input_ix(3)) - 1]
# px_maxmin.m:129
                N=size(feval(Dfun,1),2)
# px_maxmin.m:130
    
    #------------------------------------------------
# collect n
#------------------------------------------------
    n=varargin[dot(2,input_ix(4)) - 1]
# px_maxmin.m:137
    #------------------------------------------------
# determine seeding
#------------------------------------------------
    if isused(5):
        S=varargin[dot(2,input_ix(5)) - 1]
# px_maxmin.m:144
        if (length(S) != length(unique(S))):
            error('S must not contain repeated elements.')
    else:
        S=[]
# px_maxmin.m:149
    
    if isused(6):
        k=varargin[dot(2,input_ix(6)) - 1]
# px_maxmin.m:153
    else:
        if isempty(S):
            k=1
# px_maxmin.m:155
        else:
            k=0
# px_maxmin.m:157
    
    #----------------------------------------------------------------
# main loop
#----------------------------------------------------------------
    s=length(S)
# px_maxmin.m:164
    if (n < s + k):
        error('Too many seeds!')
    
    # read in seed points from S
    L=zeros(1,n)
# px_maxmin.m:170
    L[arange(1,s)]=S
# px_maxmin.m:171
    unused=setdiff((arange(1,N)),S)
# px_maxmin.m:173
    if (length(unused) != (N - s)):
        error('Seeds specified incorrectly.')
    
    
    # generate random seed points
    foo=randperm(N - s)
# px_maxmin.m:179
    randseeds=unused(foo(arange(1,k)))
# px_maxmin.m:180
    clear('foo')
    L[arange(s + 1,s + k)]=randseeds
# px_maxmin.m:183
    # generate remaining landmarks by maxmin
    DD=zeros(n,N)
# px_maxmin.m:186
    DD[(arange(1,s + k)),arange()]=feval(Dfun,L(arange(1,s + k)))
# px_maxmin.m:187
    DDmin=min(DD((arange(1,s + k)),arange()),[],1)
# px_maxmin.m:189
    for a in (arange(s + k + 1,n)).reshape(-1):
        r,newL=max(DDmin,[],2,nargout=2)
# px_maxmin.m:192
        L[a]=newL
# px_maxmin.m:193
        DD[a,arange()]=feval(Dfun,newL)
# px_maxmin.m:194
        DDmin=min(DDmin,DD(a,arange()))
# px_maxmin.m:195
    
    r=max(DDmin)
# px_maxmin.m:198
    #----------------------------------------------------------------
# finish!
#----------------------------------------------------------------
    
    if (nargout >= 2):
        DL=copy(DD)
# px_maxmin.m:205
    
    
    if (nargout >= 3):
        R=copy(r)
# px_maxmin.m:209
    
    return L,DL,R
    #----------------------------------------------------------------
# local functions
#----------------------------------------------------------------
    
@function
def local_euclid(list=None,*args,**kwargs):
    varargin = local_euclid.varargin
    nargin = local_euclid.nargin

    X=evalin('caller','X')
# px_maxmin.m:217
    d,N=size(X,nargout=2)
# px_maxmin.m:218
    DD=sqrt(max(0,repmat(sum(X(arange(),list) ** 2,1).T,concat([1,N])) + repmat(sum(X ** 2,1),concat([length(list),1])) - dot(dot(2,X(arange(),list).T),X)))
# px_maxmin.m:220
    #----------------------------------------------------------------
    
@function
def local_euclid2(list=None,*args,**kwargs):
    varargin = local_euclid2.varargin
    nargin = local_euclid2.nargin

    X=evalin('caller','X')
# px_maxmin.m:226
    d,N=size(X,nargout=2)
# px_maxmin.m:227
    L2sq=evalin('caller','L2sq')
# px_maxmin.m:228
    DD=sqrt(max(0,repmat(L2sq(list).T,concat([1,N])) + repmat(L2sq,concat([length(list),1])) - dot(dot(2,X(arange(),list).T),X)))
# px_maxmin.m:230
    #----------------------------------------------------------------
    
@function
def local_submatrix(list=None,*args,**kwargs):
    varargin = local_submatrix.varargin
    nargin = local_submatrix.nargin

    D=evalin('caller','D')
# px_maxmin.m:236
    DD=D(list,arange())
# px_maxmin.m:237
    #----------------------------------------------------------------