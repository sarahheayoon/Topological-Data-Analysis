# Generated with SMOP  0.41
from libsmop import *
# px_homologyplot.m

    
@function
def px_homologyplot(varargin=None,*args,**kwargs):
    varargin = px_homologyplot.varargin
    nargin = px_homologyplot.nargin

    #PX_HOMOLOGYPLOT  Display persistent homology data.
#   Given a cell array I of persistent homology interval data, such as
#   might be produced by a call to PERSISTENCE or COPERSISTENCE, this
#   function produces visual representations of the data in one of three
#   styles.
    
    #   The general form is PX_HOMOLOGYPLOT(I, ..., style, sign), where
#   the last two parameters are optional.
    
    #   I : Cell array of 2-row matrices; see PERSISTENCE. The columns of
#   the matrix I{p+1} specify the persistence intervals in dimension p,
#   by start and end times. A "positive" interval starts before it ends,
#   I{p+1}(1,a) < I{p+1}(2,a); whereas a "negative" interval ends before
#   it starts.
    
    #   style : one of three string options
#      'interval' : persistence intervals against time [**DEFAULT**]
#      'betti'    : graph of betti number against time
#      'scatter'  : time-time scatterplot of interval endpoints
    
    #   sign : one of two string options
#      '+' : display positive intervals only [**DEFAULT**]
#      '-' : display negative intervals only
    
    #   The other input parameters are explained below. The optional
#   parameters 'style', 'sign' can be added to any of the examples.
    
    #   PX_HOMOLOGYPLOT(I, k) displays k-dimensional homology in the current
#   figure.
    
    #   PX_HOMOLOGYPLOT(I, k1, k2) displays graphs for all integer values of
#   k between k1 and k2 (inclusive) as a sequence of subplots of the
#   current figure.
    
    #   PX_HOMOLOGYPLOT(I, 0, dim_I) is a synonym for PX_HOMOLOGYPLOT(I). 
#   Here dim_I (= length(I)-1) is the maximum dimension reported by I.
    
    #   Ha = PX_HOMOLOGYPLOT(...) returns a vector Ha containing the handles
#   of the axes in which the plots are made.
    
    #   See also PERSISTENCE, COPERSISTENCE.
    
    #Plex version 2.0 by Patrick Perry, Vin de Silva and contributors. See
#PX_PLEXINFO for credits and licensing information. [2004-October-17]
    
    #----------------------------------------------------------------
# trap errors and initialise
    
    pairs,klist,style,err=local_initialise(varargin[arange()],nargout=4)
# px_homologyplot.m:51
    error(err)
    nk=length(klist)
# px_homologyplot.m:53
    #----------------------------------------------------------------
# set up one subplot for each betti number
    Ha=zeros(1,nk)
# px_homologyplot.m:57
    if 1 == nk:
        Ha=copy(gca)
# px_homologyplot.m:61
        axes(gca)
        cla(Ha,'reset')
    else:
        figure(gcf)
        clf('reset')
        for a in (arange(1,nk)).reshape(-1):
            k=klist(a)
# px_homologyplot.m:69
            if isequal(style,'scatter'):
                Ha[a]=subplot(1,nk,a)
# px_homologyplot.m:71
            else:
                Ha[a]=subplot(nk,1,a)
# px_homologyplot.m:73
    
    #----------------------------------------------------------------
# determine range of data
    
    Fmin,Fmax,Imin,Imax=local_minmax(pairs,nargout=4)
# px_homologyplot.m:83
    # [Fmin,Fmax] = range spanned by finite entries
# [Imin,Imax] = range spanned by all entries (may include +/- inf)
    
    #----------------------------------------------------------------
# use MATLAB autoarrange algorithm to determine x-axis tickmarks
    
    if isnan(Fmin):
        # exceptional case: no finite filtration values
        xmin=- 1
# px_homologyplot.m:92
        xmax=1
# px_homologyplot.m:93
        xtick=concat([- 1,1])
# px_homologyplot.m:94
    
    axes(Ha(1))
    Ho=plot(concat([Fmin,Fmax]),concat([0,0]))
# px_homologyplot.m:98
    xtick=get(Ha(1),'xtick')
# px_homologyplot.m:99
    delete(Ho)
    cla(Ha(1),'reset')
    
    xmin=xtick(1)
# px_homologyplot.m:103
    xmax=xtick(end())
# px_homologyplot.m:104
    
    xstep=dot((xtick(2) - xtick(1)),(0.618))
# px_homologyplot.m:107
    if isinf(Imin) or isequal(style,'scatter'):
        xmin=xmin - xstep
# px_homologyplot.m:109
    
    if isinf(Imax) or isequal(style,'scatter'):
        xmax=xmax + xstep
# px_homologyplot.m:112
    
    #keyboard
    
    #----------------------------------------------------------------
# plot loop
    for a in (arange(1,nk)).reshape(-1):
        k=klist(a)
# px_homologyplot.m:121
        if 'interval' == style:
            kpairs=pairs[k + 1]
# px_homologyplot.m:127
            kpairs=sortrows(kpairs.T).T
# px_homologyplot.m:128
            nkpairs=size(kpairs,2)
# px_homologyplot.m:129
            kpairsF=copy(kpairs)
# px_homologyplot.m:132
            kpairsF[ravel(kpairs) == - Inf]=xmin + eps
# px_homologyplot.m:133
            kpairsF[ravel(kpairs) == Inf]=xmax - eps
# px_homologyplot.m:134
            axes(Ha(a))
            cla(Ha(a),'reset')
            hold('on')
            for b in (arange(1,nkpairs)).reshape(-1):
                plot(kpairsF(arange(),b),(nkpairs + 1) - concat([[b],[b]]),'-')
                if isinf(kpairs(1,b)):
                    plot(xmin + eps,nkpairs + 1 - b,'<')
                if isinf(kpairs(2,b)):
                    plot(xmax - eps,nkpairs + 1 - b,'>')
            set(Ha(a),'xtick',xtick)
            set(Ha(a),'xtickmode','manual')
            set(Ha(a),'xlim',concat([xmin,xmax]))
            set(Ha(a),'ylim',concat([0,nkpairs + 1]))
            ytick=get(Ha(a),'ytick')
# px_homologyplot.m:156
            set(Ha(a),'ytick',ytick(ytick == floor(ytick)))
            ylabel(sprintf('Betti_{%d}',k))
            hold('off')
            # end 'interval'
    #----------------------------------------
        else:
            if 'betti' == style:
                eventlist=unique(concat([[min(Imin,xmin)],[ravel(pairs[k + 1])],[max(Imax,xmax)]]))
# px_homologyplot.m:165
                bettilist=zeros(size(eventlist))
# px_homologyplot.m:166
                for b in (arange(1,size(pairs[k + 1],2))).reshape(-1):
                    pair=pairs[k + 1](arange(),b)
# px_homologyplot.m:169
                    start=find(eventlist == pair(1))
# px_homologyplot.m:170
                    finish=find(eventlist == pair(2)) - 1
# px_homologyplot.m:171
                    if isinf(pair(2)):
                        finish=finish + 1
# px_homologyplot.m:173
                    bettilist[arange(start,finish)]=bettilist(arange(start,finish)) + 1
# px_homologyplot.m:175
                # truncate infinities
                eventlistF=copy(eventlist)
# px_homologyplot.m:179
                eventlistF[eventlist == - Inf]=xmin + eps
# px_homologyplot.m:180
                eventlistF[eventlist == Inf]=xmax - eps
# px_homologyplot.m:181
                axes(Ha(a))
                cla(Ha(a),'reset')
                hold('on')
                # plot betti graph
                stairs(eventlistF,bettilist,'.-')
                if isinf(eventlist(1)):
                    plot(xmin,bettilist(1),'<')
                if isinf(eventlist(end())):
                    plot(xmax,bettilist(end()),'>')
                hold('off')
                set(Ha(a),'xtick',xtick)
                set(Ha(a),'xtickmode','manual')
                set(Ha(a),'xlim',concat([xmin,xmax]))
                set(Ha(a),'ylim',concat([0,max(bettilist) + 1]))
                ytick=get(Ha(a),'ytick')
# px_homologyplot.m:206
                set(Ha(a),'ytick',ytick(ytick == floor(ytick)))
                ylabel(sprintf('Betti_{%d}',k))
                #----------------------------------------
            else:
                if 'scatter' == style:
                    if (k == 2):
                        #  keyboard
                        pass
                    kpairs=pairs[k + 1]
# px_homologyplot.m:218
                    inflist=any(isinf(kpairs),1)
# px_homologyplot.m:219
                    kpairs[ravel(kpairs) == - inf]=xmin + eps
# px_homologyplot.m:221
                    kpairs[ravel(kpairs) == inf]=xmax - eps
# px_homologyplot.m:222
                    axes(Ha(a))
                    cla(Ha(a),'reset')
                    axis('equal')
                    hold('on')
                    Ho=plot(kpairs(1,logical_not(inflist)),kpairs(2,logical_not(inflist)),'.b')
# px_homologyplot.m:230
                    set(Ho,'markersize',12)
                    Ho=plot(kpairs(1,inflist),kpairs(2,inflist),'*b')
# px_homologyplot.m:232
                    set(Ho,'markersize',6)
                    Ho=plot(xtick(concat([1,1,end()])),xtick(concat([1,end(),end()])),'-')
# px_homologyplot.m:236
                    set(Ho,'color',get(gcf,'color'),'linewidth',0.5)
                    Ho=patch(concat([xmin,xmax,xmax]),concat([xmin,xmin,xmax]),'k')
# px_homologyplot.m:239
                    set(Ho,'facecolor',get(gcf,'color'))
                    hold('off')
                    set(Ha(a),'xaxislocation','top')
                    set(Ha(a),'xtick',xtick)
                    set(Ha(a),'xtickmode','manual')
                    set(Ha(a),'xlim',concat([xmin,xmax]))
                    set(Ha(a),'ytick',xtick)
                    set(Ha(a),'ytickmode','manual')
                    set(Ha(a),'ylim',concat([xmin,xmax]))
                    xlabel(sprintf('Betti_{%d}',k))
                    #----------------------------------------
    
    #----------------------------------------------------------------
# return
    if (nargout == 1):
        Ha_out=copy(Ha)
# px_homologyplot.m:265
    
    return Ha_out
    #----------------------------------------------------------------
# local functions
#----------------------------------------------------------------
    
    #----------------------------------------------------------------
# parse the input to extract the relevant parameters
    
@function
def local_initialise(varargin=None,*args,**kwargs):
    varargin = local_initialise.varargin
    nargin = local_initialise.nargin

    # dummy values for output arguments
# (needed in case of early 'return' on error)
    style=[]
# px_homologyplot.m:279
    pairs=[]
# px_homologyplot.m:280
    klist=[]
# px_homologyplot.m:281
    err=[]
# px_homologyplot.m:282
    err=nargchk(1,5,nargin)
# px_homologyplot.m:284
    if err:
        return pairs,klist,style,err
    
    # extract 'style' and 'sign' arguments and substitute defaults.
    
    stylelog=[]
# px_homologyplot.m:291
    style='interval'
# px_homologyplot.m:292
    signlog=[]
# px_homologyplot.m:293
    isign='+'
# px_homologyplot.m:294
    if (nargin >= 2):
        # how many trailing string arguments?
        if ischar(varargin[end()]):
            if ischar(varargin[end() - 1]):
                nchar=2
# px_homologyplot.m:300
            else:
                nchar=1
# px_homologyplot.m:302
        else:
            nchar=0
# px_homologyplot.m:305
        stylelist=cellarray(['interval','betti','scatter'])
# px_homologyplot.m:308
        stylelog=ismember(stylelist,varargin(arange(end() + 1 - nchar,end())))
# px_homologyplot.m:309
        if (sum(stylelog) == 1):
            style=stylelist[stylelog]
# px_homologyplot.m:311
        else:
            if (sum(stylelog) > 1):
                err='At most one display style may be specifed.'
# px_homologyplot.m:313
        signlist=cellarray(['+','-'])
# px_homologyplot.m:316
        signlog=ismember(signlist,varargin(arange(end() + 1 - nchar,end())))
# px_homologyplot.m:317
        if (sum(signlog) == 1):
            isign=signlist[signlog]
# px_homologyplot.m:319
        else:
            if (sum(signlog) > 1):
                err='At most one sign may be specified.'
# px_homologyplot.m:321
    
    if err:
        return pairs,klist,style,err
    
    # number of remaining input arguments
    nargin1=nargin - sum(concat([stylelog,signlog]))
# px_homologyplot.m:329
    if (nargin1 < 1):
        err='Interval data must be specified.'
# px_homologyplot.m:332
        return pairs,klist,style,err
    
    # extract and process interval pairs data
    pairs=varargin[1]
# px_homologyplot.m:337
    pairs,err=local_checkpairs(pairs,isign,nargout=2)
# px_homologyplot.m:338
    if err:
        return pairs,klist,style,err
    
    # determine range of dimensions
    if 1 == nargin1:
        k1=0
# px_homologyplot.m:346
        k2=length(pairs) - 1
# px_homologyplot.m:347
    else:
        if 2 == nargin1:
            k1=varargin[2]
# px_homologyplot.m:350
            k2=copy(k1)
# px_homologyplot.m:351
        else:
            if 3 == nargin1:
                k1=varargin[2]
# px_homologyplot.m:354
                k2=varargin[3]
# px_homologyplot.m:355
    
    err=local_checkinteger(k1,k2)
# px_homologyplot.m:358
    if err:
        return pairs,klist,style,err
    
    
    if (max(k1,k2) >= length(pairs)):
        err='Specified dimensions out of range.'
# px_homologyplot.m:364
        return pairs,klist,style,err
    
    if (k1 <= k2):
        klist=(arange(k1,k2))
# px_homologyplot.m:369
    else:
        klist=(arange(k1,k2,- 1))
# px_homologyplot.m:371
    
    return pairs,klist,style,err
    #----------------------------------------------------------------
    
@function
def local_checkpairs(pairs=None,isign=None,*args,**kwargs):
    varargin = local_checkpairs.varargin
    nargin = local_checkpairs.nargin

    err=[]
# px_homologyplot.m:378
    if logical_not(iscell(pairs)) or isempty(pairs):
        err='First input must be a non-empty cell-array.'
# px_homologyplot.m:380
        return pairs,err
    
    for a in (arange(1,length(pairs))).reshape(-1):
        if logical_not(isnumeric(pairs[a])) or (size(pairs[a],1) != 2):
            err='Interval data is incorrectly specified.'
# px_homologyplot.m:385
            return pairs,err
        else:
            # retain positive (resp. negative) pairs only
            if '+' == isign:
                pairs[a]=pairs[a](arange(),(pairs[a](1,arange()) < pairs[a](2,arange())))
# px_homologyplot.m:391
            else:
                if '-' == isign:
                    pairs[a]=pairs[a](concat([2,1]),(pairs[a](1,arange()) > pairs[a](2,arange())))
# px_homologyplot.m:393
    
    return pairs,err
    #----------------------------------------------------------------
    
@function
def local_checkinteger(varargin=None,*args,**kwargs):
    varargin = local_checkinteger.varargin
    nargin = local_checkinteger.nargin

    # all inputs are required to be integers
    err=[]
# px_homologyplot.m:403
    for a in (arange(1,nargin)).reshape(-1):
        k=varargin[a]
# px_homologyplot.m:405
        if logical_not(isnumeric(k)) or (length(k) > 1) or logical_not(isequal(k,floor(k))) or (k < 0):
            err='Dimension values must be nonnegative integers.'
# px_homologyplot.m:408
            return err
    
    
    #----------------------------------------------------------------
    
@function
def local_minmax(pairs=None,*args,**kwargs):
    varargin = local_minmax.varargin
    nargin = local_minmax.nargin

    # Fmin, Fmax denote the min and max of the finite entries of pairs{:}
# Imin, Imax denote the min and max of all the entries of pairs{:}
    pairs_=[]
# px_homologyplot.m:417
    for a in (arange(1,length(pairs))).reshape(-1):
        pairs_=concat([[pairs_],[ravel(pairs[a])]])
# px_homologyplot.m:419
    
    # all entries, finite and infinite
    pairs_=unique(pairs_)
# px_homologyplot.m:423
    if logical_not(isempty(pairs_)):
        Imax=max(pairs_)
# px_homologyplot.m:425
        Imin=min(pairs_)
# px_homologyplot.m:426
    else:
        Imax=copy(NaN)
# px_homologyplot.m:428
        Imin=copy(NaN)
# px_homologyplot.m:429
    
    # finite entries only
    pairs_=pairs_(isfinite(ravel(pairs_)))
# px_homologyplot.m:433
    if logical_not(isempty(pairs_)):
        Fmax=max(pairs_)
# px_homologyplot.m:435
        Fmin=min(pairs_)
# px_homologyplot.m:436
    else:
        Fmax=copy(NaN)
# px_homologyplot.m:438
        Fmin=copy(NaN)
# px_homologyplot.m:439
    
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------