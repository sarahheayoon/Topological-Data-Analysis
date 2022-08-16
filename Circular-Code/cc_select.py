# Generated with SMOP  0.41
from libsmop import *
# cc_select.m

    
@function
def cc_select(I1=None,ncc=None,Ha=None,*args,**kwargs):
    varargin = cc_select.varargin
    nargin = cc_select.nargin

    #CC_SELECT -- select (co)cycles by clicking on persistence diagram
    
    #   [Rcc, Kcc] = cc_select(I1, ncc);
    
    #Input:
#   I1     2-by-m    persistence intervals
#   ncc    scalar    number of (co)cycles wanted (default 1)
    
    #Output:
#   Rcc    scalar    persistence index at which (co)cycles are sought
#   Kcc    1-by-ncc  index values of the chosen cocycles
    
    #The first click selects a point on the diagonal. Subsequent clicks select
#indices for the the desired (co)cycles. If there are no cocycles in the
#chosen quadrant then Kcc = NaN.
    
    #This function depends on px_homologyplot.m to draw the persistence
#diagram.
    
    #[Vin de Silva, 2015-04-29]
    
    if (nargin < 1):
        ncc=1
# cc_select.m:25
    
    if (nargin <= 2):
        HF=copy(figure)
# cc_select.m:29
    else:
        axes(Ha)
    
    HaPD=px_homologyplot(cellarray([I1,I1]),1,'scatter')
# cc_select.m:33
    # begin by selecting a quadrant
    u,v=ginput(1,nargout=2)
# cc_select.m:36
    Rcc=(u + v) / 2
# cc_select.m:37
    PDlim=get(HaPD,'xlim')
# cc_select.m:39
    PDmin=PDlim(1)
# cc_select.m:40
    PDmax=PDlim(2)
# cc_select.m:41
    hold('on')
    Hcensor=patch(concat([PDmin,PDmin,Rcc,Rcc,PDmax]),concat([PDmin,Rcc,Rcc,PDmax,PDmax]),concat([0.5,0.1,0.1]),'facealpha',0.5)
# cc_select.m:44
    # which points of the diagram lie in the quadrant?
    PDquadlist=find(logical_and((I1(1,arange()) < Rcc),(I1(2,arange()) > Rcc)))
# cc_select.m:50
    if isempty(PDquadlist):
        disp('No cocycles in chosen quadrant.')
        Kcc=copy(NaN)
# cc_select.m:54
        return Rcc,Kcc
    
    PDquad=I1(arange(),PDquadlist)
# cc_select.m:58
    PDquad[PDquad == inf]=PDmax
# cc_select.m:59
    PDquad[PDquad == - inf]=PDmin
# cc_select.m:60
    # select the desired number of points
    Kcc=zeros(1,ncc)
# cc_select.m:63
    for a in (arange(1,ncc)).reshape(-1):
        u,v=ginput(1,nargout=2)
# cc_select.m:65
        __,PDclosest=min((PDquad(1,arange()) - u) ** 2 + (PDquad(2,arange()) - v) ** 2,nargout=2)
# cc_select.m:66
        Kcc[a]=PDquadlist(PDclosest)
# cc_select.m:67
        Hchosen=plot(PDquad(1,PDclosest),PDquad(2,PDclosest),'*r')
# cc_select.m:68
    
    if (nargin <= 2):
        close_(HF)
    
    ##
    return Rcc,Kcc