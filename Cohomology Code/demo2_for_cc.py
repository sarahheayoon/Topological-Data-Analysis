# Generated with SMOP  0.41
from libsmop import *
# demo2_for_cc.m

    # Demo script 2 for circular coordinates
    
    # This script carries out the following steps:
    
    # 1. Creates a time-series signal
# 2. Converts it to point-cloud data, using Takens delay embedding
# 3. Computes the persistence diagram.
# 4. Asks the user to select a quadrant in the persistence diagram.
# 5. Asks the user to select a point in the quadrant.
# 6. Converts the corresponding cocycle to a circle-valued function.
# 7. Plots the "circular coordinate" against time.
# 8. "Unrolls" the circular coordiate to a real-valued function.
    
    # For a clean periodic signal, the slope of the unrolled coordinate is
# equal to the number of cycles per second.
    
    #[VdS 2017-april-26]
    
    # generate signal
    T0=(arange(0,100,0.1))
# demo2_for_cc.m:21
    N0=length(T0)
# demo2_for_cc.m:22
    F=sin(T0) + dot(0.2,randn(1,N0))
# demo2_for_cc.m:23
    # Takens delay embedding
    delays=concat([0,7,12])
# demo2_for_cc.m:26
    nd=length(delays)
# demo2_for_cc.m:27
    N=N0 - max(delays)
# demo2_for_cc.m:28
    X=zeros(nd,N)
# demo2_for_cc.m:30
    for a in (arange(1,nd)).reshape(-1):
        X[a,arange()]=F(delays(a) + (arange(1,N)))
# demo2_for_cc.m:32
    
    T=T0(arange(1,N))
# demo2_for_cc.m:34
    # select landmarks
    nL=30
# demo2_for_cc.m:37
    L,DL,RL=px_maxmin(X,'vector',nL,'n',nargout=3)
# demo2_for_cc.m:38
    DLL=DL(arange(),L)
# demo2_for_cc.m:39
    # construct VR-complex (edges only)
    R=dot(RL,4)
# demo2_for_cc.m:42
    Edges=cc_edges(DLL,R)
# demo2_for_cc.m:43
    # persistent cohomology calculation
    C0,C1,I0,I1=cc_cocycles(Edges,47,nargout=4)
# demo2_for_cc.m:46
    # select one cocycle
    Rcc,Kcc=cc_select(I1,1,nargout=2)
# demo2_for_cc.m:49
    # calculate circular coordinates on landmarks
    ThetaL=cc_theta(Edges,C1,47,Rcc,Kcc)
# demo2_for_cc.m:52
    # extend to whole data
    ThetaX=cc_interpolate_theta(ThetaL,DL,L)
# demo2_for_cc.m:55
    ## plot results
    figure(147)
    clf
    # colours represent circular coordinate
    subplot(4,8,concat([1,28]))
    ncol=64
# demo2_for_cc.m:62
    hsv_map=hsv(ncol)
# demo2_for_cc.m:63
    HX=zeros(1,N)
# demo2_for_cc.m:64
    for b in (arange(1,N)).reshape(-1):
        HX[b]=plot(X(1,b),X(2,b),'.')
# demo2_for_cc.m:66
        set(HX(b),'color',hsv_map(1 + floor(dot(ThetaX(b),ncol)),arange()))
        hold('on')
    
    title('delay embedding coordinates 1 & 2')
    
    subplot(4,8,concat([5,8]))
    plot(T0,F,'.k')
    title('original signal')
    
    subplot(4,8,concat([13,16]))
    plot(T,ThetaX,'.')
    title('circular coordinate')
    
    UThetaX=copy(ThetaX)
# demo2_for_cc.m:84
    UThetaX[arange(),arange(2,end())]=UThetaX(arange(),arange(2,end())) - cumsum(round(diff(UThetaX,[],2)),2)
# demo2_for_cc.m:85
    subplot(4,8,concat([21,32]))
    plot(T,UThetaX,'.')
    title('unrolled coordinate')