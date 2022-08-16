# Generated with SMOP  0.41
from libsmop import *
# demo1_for_cc.m

    # Demo script 1 for circular coordinates
    
    # This script carries out the following steps:
    
    # 1. Creates point-cloud dataset.
# 2. Computes the persistence diagram.
# 3. Asks the user to select a quadrant in the persistence diagram.
# 4. Asks the user to select a point in the quadrant.
# 5. Converts the corresponding cocycle to a circle-valued function.
# 6. Displays the function using a colour plot.
# 7. Repeats, as requested.
    
    #[VdS 2017-april-26]
    
    # generate data
    N=400
# demo1_for_cc.m:17
    t=rand(1,N)
# demo1_for_cc.m:18
    x=cos(dot(dot(2,pi),t))
# demo1_for_cc.m:19
    y=sin(dot(dot(2,pi),t)) + sign(randn(1,N))
# demo1_for_cc.m:20
    X=concat([[x],[y]]) + dot((0.1),randn(2,N))
# demo1_for_cc.m:22
    clear('t','x','y')
    # set up figure
    figure(47)
    clf
    set(47,'name','keyboard to quit, mouse to continue')
    Ha=subplot(1,2,2)
# demo1_for_cc.m:28
    # display data in monochrome
    subplot(1,2,1)
    plot(X(1,arange()),X(2,arange()),'k.')
    axis('equal')
    title('PCD coordinates 1 & 2')
    # select landmarks
    nL=50
# demo1_for_cc.m:38
    L,DL,RL=px_maxmin(X,'vector',nL,'n',nargout=3)
# demo1_for_cc.m:39
    DLL=DL(arange(),L)
# demo1_for_cc.m:40
    # construct VR-complex (edges only)
    R=dot(RL,4)
# demo1_for_cc.m:43
    Edges=cc_edges(DLL,R)
# demo1_for_cc.m:44
    # persistent cohomology calculation (mod 47)
    C0,C1,I0,I1=cc_cocycles(Edges,47,nargout=4)
# demo1_for_cc.m:47
    finish=0
# demo1_for_cc.m:50
    while logical_not(finish):

        # select one cocycle
        #[Rcc, Kcc] = cc_select(I1,1);
        Rcc,Kcc=cc_select(I1,1,Ha,nargout=2)
# demo1_for_cc.m:56
        # calculate circular coordinates on landmarks
        ThetaL=cc_theta(Edges,C1,47,Rcc,Kcc)
# demo1_for_cc.m:61
        ThetaX=cc_interpolate_theta(ThetaL,DL,L)
# demo1_for_cc.m:64
        figure(47)
        subplot(1,2,1)
        ncol=64
# demo1_for_cc.m:70
        hsv_map=hsv(ncol)
# demo1_for_cc.m:71
        HX=zeros(1,N)
# demo1_for_cc.m:72
        for b in (arange(1,N)).reshape(-1):
            HX[b]=plot(X(1,b),X(2,b),'.')
# demo1_for_cc.m:74
            set(HX(b),'color',hsv_map(1 + floor(dot(ThetaX(b),ncol)),arange()))
            hold('on')
        axis('equal')
        title('PCD coordinates 1 & 2')
        # continue (mouse-click) or exit (keyboard)
        finish=copy(waitforbuttonpress)
# demo1_for_cc.m:82

    