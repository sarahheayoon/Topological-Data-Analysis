# Generated with SMOP  0.41
from libsmop import *
# cc_interpolate_theta.m

    
@function
def cc_interpolate_theta(ThetaL=None,DL=None,L=None,*args,**kwargs):
    varargin = cc_interpolate_theta.varargin
    nargin = cc_interpolate_theta.nargin

    #CC_INTERPOLATE_THETA -- interpolate circle-valued functions
    
    #   ThetaX = cc_interpolate(ThetaL, DL, L);
    
    #This extends the definition of circle-valued functions ThetaL(a,:)
#defined on landmark points to circle-valued functions ThetaX(a,:)
#defined on the whole data.
    
    #Input:
#   ThetaL   ncc-by-n   each row is a circle-function on n landmarks
#   DL       n-by-N     landmark-to-data distance matrix
#   L        1-by-n     indices of landmarks in data
    
    #[Vin de Silva, 2015-04-29]
    
    ThetaL=mod(ThetaL,1)
# cc_interpolate_theta.m:18
    n=size(DL,1)
# cc_interpolate_theta.m:20
    N=size(DL,2)
# cc_interpolate_theta.m:21
    DLsort,DLsortI=sort(DL,1,'ascend',nargout=2)
# cc_interpolate_theta.m:23
    # indices for nearest 2 landmarks
    DLL=DL(arange(),L)
# cc_interpolate_theta.m:26
    Dab=DLL(sub2ind(concat([n,n]),DLsortI(1,arange()),DLsortI(2,arange()))) ** 2
# cc_interpolate_theta.m:27
    Dxa=DLsort(1,arange()) ** 2
# cc_interpolate_theta.m:28
    Dxb=DLsort(2,arange()) ** 2
# cc_interpolate_theta.m:29
    # interpolation coefficients using those two landmarks
    inter2C=zeros(2,N)
# cc_interpolate_theta.m:32
    inter2C[1,arange()]=concat([(0.5) + (Dxb - Dxa) / (dot(2,Dab))])
# cc_interpolate_theta.m:33
    inter2C[2,arange()]=1 - inter2C(1,arange())
# cc_interpolate_theta.m:34
    ncc=size(ThetaL,1)
# cc_interpolate_theta.m:36
    ThetaX=zeros(ncc,N)
# cc_interpolate_theta.m:37
    for a in (arange(1,ncc)).reshape(-1):
        ThetaXL=concat([[ThetaL(a,DLsortI(1,arange()))],[ThetaL(a,DLsortI(2,arange()))]])
# cc_interpolate_theta.m:40
        ThetaXL[2,arange()]=ThetaXL(2,arange()) - round(diff(ThetaXL,1))
# cc_interpolate_theta.m:41
        ThetaX[a,arange()]=mod(sum(multiply(inter2C,ThetaXL),1),1)
# cc_interpolate_theta.m:42
    