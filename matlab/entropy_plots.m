% Generate a plot showing the evolution of conditional entropy with increasing
% sample size. This script should be used for the following three plots:
%   One Billion Words (1BW) with Jiantao-Venkat-Han-Weissman (JVHW)
%   One Billion Words (1BW) with profile maximum likelihood (PML)
%   Penn Treebank (PTB) with Jiantao-Venkat-Han-Weissman (JVHW)
%
% Chuan-Zheng Lee
% EE378A project: Fundamental limits in language modeling
% June 2017

estimate_type = 'jvhw'; % 'jvhw' or 'pml'
dataset = '1bw'; % '1bw' or 'ptb'
% But not 'pml' and 'ptb'/'vv' together, for that use 'ptb_plots.m', because
% that data was generated using the Matlab version (before the Python PML
% code existed, and Python VV code still doesn't exist.

names = {'unigrams', 'bigrams', 'trigrams', 'quadrigrams', 'quintigrams', ...
    'sexigrams', 'septigrams'};

fig = figure(1);
clf(fig)
ax = axes(fig);

estimates = zeros(7,1);

ns = [];
for n = 7:-1:1
    filename = fullfile(dataset, estimate_type, [num2str(n) 'grams.csv']);
    try
        data = csvread(filename);
    catch
        continue
    end
    plot(data(:,1), data(:,2))
    estimates(n) = data(end);
    hold on
    ns(end+1) = n; %#ok<SAGROW>
end

set(ax, 'TickLabelInterpreter', 'latex')
legend(names(ns), 'Interpreter', 'latex', 'Location', 'best')
xlabel('number of words', 'Interpreter', 'latex')
ylabel('estimated entropy', 'Interpreter', 'latex')
if strcmp(dataset, 'ptb')
    xlim([0 12e5])
end
savefig(fig, [dataset '_' estimate_type])
saveas(fig, [dataset '_' estimate_type], 'epsc')

