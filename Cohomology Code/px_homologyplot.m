function Ha_out = px_homologyplot(varargin)

%PX_HOMOLOGYPLOT  Display persistent homology data.
%   Given a cell array I of persistent homology interval data, such as
%   might be produced by a call to PERSISTENCE or COPERSISTENCE, this
%   function produces visual representations of the data in one of three
%   styles.
%
%   The general form is PX_HOMOLOGYPLOT(I, ..., style, sign), where
%   the last two parameters are optional.
%
%   I : Cell array of 2-row matrices; see PERSISTENCE. The columns of
%   the matrix I{p+1} specify the persistence intervals in dimension p,
%   by start and end times. A "positive" interval starts before it ends,
%   I{p+1}(1,a) < I{p+1}(2,a); whereas a "negative" interval ends before
%   it starts.
%
%   style : one of three string options
%      'interval' : persistence intervals against time [**DEFAULT**]
%      'betti'    : graph of betti number against time
%      'scatter'  : time-time scatterplot of interval endpoints
%
%   sign : one of two string options
%      '+' : display positive intervals only [**DEFAULT**]
%      '-' : display negative intervals only
%
%   The other input parameters are explained below. The optional
%   parameters 'style', 'sign' can be added to any of the examples.
%
%   PX_HOMOLOGYPLOT(I, k) displays k-dimensional homology in the current
%   figure.
%
%   PX_HOMOLOGYPLOT(I, k1, k2) displays graphs for all integer values of
%   k between k1 and k2 (inclusive) as a sequence of subplots of the
%   current figure.
%
%   PX_HOMOLOGYPLOT(I, 0, dim_I) is a synonym for PX_HOMOLOGYPLOT(I). 
%   Here dim_I (= length(I)-1) is the maximum dimension reported by I.
%
%   Ha = PX_HOMOLOGYPLOT(...) returns a vector Ha containing the handles
%   of the axes in which the plots are made.
%
%   See also PERSISTENCE, COPERSISTENCE.
%
%Plex version 2.0 by Patrick Perry, Vin de Silva and contributors. See
%PX_PLEXINFO for credits and licensing information. [2004-October-17]

%----------------------------------------------------------------
% trap errors and initialise

[pairs, klist, style, err] = local_initialise(varargin{:});
error(err);
nk = length(klist);

%----------------------------------------------------------------
% set up one subplot for each betti number
Ha = zeros(1, nk);

switch nk
    case 1
        Ha = gca;
        axes(gca);
        cla(Ha, 'reset')
        
    otherwise
        figure(gcf);
        clf reset
        for a = (1: nk)
            k = klist(a);
            if isequal(style, 'scatter')
                Ha(a) = subplot(1, nk, a);
            else
                Ha(a) = subplot(nk, 1, a);
            end
        end
end



%----------------------------------------------------------------
% determine range of data

[Fmin,Fmax,Imin,Imax] = local_minmax(pairs);
% [Fmin,Fmax] = range spanned by finite entries
% [Imin,Imax] = range spanned by all entries (may include +/- inf)

%----------------------------------------------------------------
% use MATLAB autoarrange algorithm to determine x-axis tickmarks

if isnan(Fmin)
  % exceptional case: no finite filtration values
  xmin = -1;
  xmax = 1;
  xtick = [-1 1];
end

  axes(Ha(1));
  Ho = plot([Fmin, Fmax], [0 0]);
  xtick = get(Ha(1), 'xtick');
  delete(Ho);
  cla(Ha(1),'reset')
  
  xmin = xtick(1);
  xmax = xtick(end);
  
  % extend range to accommodate +inf, -inf
  xstep = (xtick(2) - xtick(1)) * (0.618);
  if isinf(Imin) || isequal(style, 'scatter')
    xmin = xmin - xstep;
  end
  if isinf(Imax) || isequal(style, 'scatter')
    xmax = xmax + xstep;
  end


%keyboard

%----------------------------------------------------------------
% plot loop
for a = (1: nk)
  k = klist(a);

  switch style
    %----------------------------------------
   case 'interval'
    
    kpairs = pairs{k+1};
    kpairs = sortrows(kpairs')';
    nkpairs = size(kpairs, 2);

    % finite truncation
    kpairsF = kpairs;
    kpairsF(kpairs(:) == -Inf) = xmin + eps;
    kpairsF(kpairs(:) == Inf) = xmax - eps;
    
    axes(Ha(a))
    cla(Ha(a),'reset');
    
    hold on
    
    for b = (1: nkpairs)
      plot(kpairsF(:,b), (nkpairs+1) - [b;b], '-');
      if isinf(kpairs(1,b))
	plot(xmin+eps, nkpairs+1-b, '<');
      end
      if isinf(kpairs(2,b))
	plot(xmax-eps, nkpairs+1-b, '>');
      end
    end    
        
    set(Ha(a), 'xtick', xtick);
    set(Ha(a), 'xtickmode', 'manual');
    set(Ha(a), 'xlim', [xmin xmax]);
    
    set(Ha(a), 'ylim', [0, nkpairs + 1]);
    ytick = get(Ha(a), 'ytick');
    set(Ha(a), 'ytick', ytick(ytick == floor(ytick)));
    ylabel(sprintf('Betti_{%d}', k));
    
    hold off
    
    % end 'interval'
    %----------------------------------------
   case 'betti'
    eventlist = unique([min(Imin,xmin); pairs{k+1}(:); max(Imax,xmax)]);
    bettilist = zeros(size(eventlist));
    
    for b = (1: size(pairs{k+1}, 2))
      pair = pairs{k+1}(:,b);
      start = find(eventlist == pair(1));
      finish = find(eventlist == pair(2)) - 1;
      if isinf(pair(2))
	finish = finish + 1;
      end
      bettilist(start:finish) = bettilist(start:finish) + 1;
    end
    
    % truncate infinities
    eventlistF = eventlist;
    eventlistF(eventlist == -Inf) = xmin + eps;
    eventlistF(eventlist == Inf) = xmax - eps;
    
    axes(Ha(a))
    cla(Ha(a),'reset');
    
    hold on
    
    % plot betti graph
    stairs(eventlistF, bettilist, '.-');
    
    % plot arrows towards +/- infinity
    if isinf(eventlist(1))
      plot(xmin, bettilist(1), '<');
    end
    if isinf(eventlist(end))
      plot(xmax, bettilist(end), '>');
    end
    hold off
    
    set(Ha(a), 'xtick', xtick);
    set(Ha(a), 'xtickmode', 'manual');
    set(Ha(a), 'xlim', [xmin xmax]);
    
    %set(Ha(a), 'ylim', [max(min(bettilist) - 1, 0), max(bettilist) + 1]);
    set(Ha(a), 'ylim', [0, max(bettilist) + 1]);
    ytick = get(Ha(a), 'ytick');
    set(Ha(a), 'ytick', ytick(ytick == floor(ytick)));
    ylabel(sprintf('Betti_{%d}', k));
    
    % end: 'betti'   
    %----------------------------------------   
   case 'scatter'
    
    if (k == 2)
    %  keyboard
    end
    
    kpairs = pairs{k+1};
    inflist = any(isinf(kpairs), 1);
    
    kpairs(kpairs(:) == -inf) = xmin + eps;
    kpairs(kpairs(:) == inf) = xmax - eps;
      
    axes(Ha(a))
    cla(Ha(a),'reset');
    axis equal

    hold on
    
    Ho = plot(kpairs(1,~inflist), kpairs(2,~inflist), '.b');
    set(Ho, 'markersize', 12);
    Ho = plot(kpairs(1,inflist), kpairs(2,inflist), '*b');
    set(Ho, 'markersize', 6);
        
    % draw box around finite area
    Ho = plot(xtick([1 1 end]), xtick([1 end end]), '-');
    set(Ho, 'color', get(gcf,'color'), 'linewidth', 0.5);
    % grey out subdiagonal region
    Ho = patch([xmin xmax xmax],[xmin xmin xmax],'k');
    set(Ho, 'facecolor', get(gcf,'color'));
    
    hold off
    
    set(Ha(a), 'xaxislocation', 'top');
    set(Ha(a), 'xtick', xtick);
    set(Ha(a), 'xtickmode', 'manual');
    set(Ha(a), 'xlim', [xmin xmax]);
    
    set(Ha(a), 'ytick', xtick);
    set(Ha(a), 'ytickmode', 'manual');
    set(Ha(a), 'ylim', [xmin xmax]);

    xlabel(sprintf('Betti_{%d}', k));
    
    % end: 'scatter'
    %----------------------------------------    
  end  

end


%----------------------------------------------------------------
% return
if (nargout == 1)
  Ha_out = Ha;
end
return

%----------------------------------------------------------------
% local functions
%----------------------------------------------------------------

%----------------------------------------------------------------
% parse the input to extract the relevant parameters
function [pairs, klist, style, err] = local_initialise(varargin)

% dummy values for output arguments
% (needed in case of early 'return' on error)
style = [];
pairs = [];
klist = [];
err = [];

err = nargchk(1, 5, nargin);
if err
  return
end

% extract 'style' and 'sign' arguments and substitute defaults.

stylelog = [];
style = 'interval';
signlog = [];
isign = '+';

if (nargin >= 2)
  % how many trailing string arguments?
  if ischar(varargin{end})
    if ischar(varargin{end-1})
      nchar = 2;
    else
      nchar = 1;
    end
  else
    nchar = 0;
  end
  
  stylelist = {'interval', 'betti', 'scatter'};
  stylelog = ismember(stylelist, varargin(end+1-nchar:end));
  if (sum(stylelog) == 1)
    style = stylelist{stylelog};
  elseif (sum(stylelog) > 1)
    err = 'At most one display style may be specifed.';
  end
  
  signlist = {'+', '-'};
  signlog = ismember(signlist, varargin(end+1-nchar:end));
  if (sum(signlog) == 1)
    isign = signlist{signlog};
  elseif (sum(signlog) > 1)
    err = 'At most one sign may be specified.';
  end
end
if err
  return
end

% number of remaining input arguments
nargin1 = nargin - sum([stylelog, signlog]);

if (nargin1 < 1)
  err = 'Interval data must be specified.';
  return
end

% extract and process interval pairs data
pairs = varargin{1};
[pairs, err] = local_checkpairs(pairs, isign);
if err
  return
end

% determine range of dimensions
switch nargin1
 case 1
  k1 = 0;
  k2 = length(pairs) - 1;
  
 case 2
  k1 = varargin{2};
  k2 = k1;
  
 case 3
  k1 = varargin{2};
  k2 = varargin{3};
end

err = local_checkinteger(k1, k2);
if err
  return
end
  
if (max(k1,k2) >= length(pairs))
  err = 'Specified dimensions out of range.';
  return
end

if (k1 <= k2)
  klist = (k1: k2);
else
  klist = (k1: -1: k2);
end

return

%----------------------------------------------------------------
function [pairs, err] = local_checkpairs(pairs, isign)
err = [];
if ~iscell(pairs) || isempty(pairs)
  err = 'First input must be a non-empty cell-array.';
  return
end
for a = (1: length(pairs))
  if ~isnumeric(pairs{a}) || (size(pairs{a}, 1) ~= 2)
    err = 'Interval data is incorrectly specified.';
    return
  else
    % retain positive (resp. negative) pairs only
    switch isign
     case '+'
      pairs{a} = pairs{a}(:, (pairs{a}(1,:) < pairs{a}(2,:)));
     case '-'
      pairs{a} = pairs{a}([2 1], (pairs{a}(1,:) > pairs{a}(2,:)));
    end
  end
end

return

%----------------------------------------------------------------
function err = local_checkinteger(varargin)
% all inputs are required to be integers
err = [];
for a = (1: nargin)
  k = varargin{a};
  if ~isnumeric(k) || (length(k) > 1) ...
        || ~isequal(k,floor(k)) || (k < 0)
    err = 'Dimension values must be nonnegative integers.';
    return
  end
end
  
%----------------------------------------------------------------
function [Fmin,Fmax,Imin,Imax] = local_minmax(pairs)
% Fmin, Fmax denote the min and max of the finite entries of pairs{:}
% Imin, Imax denote the min and max of all the entries of pairs{:}
pairs_ = [];
for a = (1: length(pairs))
  pairs_ = [pairs_; pairs{a}(:)];
end

% all entries, finite and infinite
pairs_ = unique(pairs_);
if ~isempty(pairs_)
  Imax = max(pairs_);
  Imin = min(pairs_);
else
  Imax = NaN;
  Imin = NaN;
end

% finite entries only
pairs_ = pairs_(isfinite(pairs_(:)));
if ~isempty(pairs_)
  Fmax = max(pairs_);
  Fmin = min(pairs_);
else
  Fmax = NaN;
  Fmin = NaN;
end


%----------------------------------------------------------------

%----------------------------------------------------------------
