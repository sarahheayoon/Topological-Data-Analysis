# Generated with SMOP  0.41
from libsmop import *
# cc_theta.m

    
@function
def cc_theta(Edges=None,C1=None,p=None,Rcc=None,Kcc=None,*args,**kwargs):
    varargin = cc_theta.varargin
    nargin = cc_theta.nargin

    #CC_THETA -- construct circular coordinates
    
    #Calculate the circular coordinates associated to a given collection of
#cocycles (mod p). The prime p must be specified.
    
    #   Theta = cc_theta(Edges, C1, p, Rcc, Kcc)
    
    #Input:
#   Edges    <structured array>
#   C1       m-by-m       persistent cochain basis
#   p        scalar       prime modulus by which C1 was calculated
#   Rcc      scalar       filtration parameter
#   Kcc      1-by-ncc     indices for the ncc chosen cocycles
    
    #Output:
#   Theta    ncc-by-m     circular coordinates (values in [0,1)).
    
    #Although the cocycles are typically chosen persistently, the calculation
#takes place in a fixed simplicial complex specified by Rcc.
    
    #[Vin de Silva, 2015-04-19]
    
    # construct coboundary matrix up to Rips parameter Rf
    af=sum(Edges.D <= Rcc)
# cc_theta.m:26
    #find(DS <= Rf, 1, 'last');
    
    D0=sparse((arange(1,af)),Edges.V(2,(arange(1,af))),1,af,Edges.n) + sparse((arange(1,af)),Edges.V(1,(arange(1,af))),- 1,af,Edges.n)
# cc_theta.m:29
    ncc=length(Kcc)
# cc_theta.m:32
    Theta=zeros(ncc,Edges.n)
# cc_theta.m:33
    for a in (arange(1,ncc)).reshape(-1):
        # extract the significant cocycles, lift to integer coefficients
        C1f=C1((arange(1,af)),Kcc(a))
# cc_theta.m:37
        C1f=mod(C1f + (p - 1) / 2,p) - (p - 1) / 2
# cc_theta.m:38
        theta=lsqr(D0,C1f,[],100)
# cc_theta.m:41
        Theta[a,arange()]=mod(theta,1)
# cc_theta.m:42
    