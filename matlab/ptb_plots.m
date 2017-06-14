% Generate a plot showing the evolution of conditional entropy with increasing
% sample size. This script should be used for the following two plots:
%   Penn Treebank (PTB) with profile maximum likelihood (PML)
%   Penn Treebank (PTB) with Valiant and Valiant (VV)
%
% Chuan-Zheng Lee
% EE378A project: Fundamental limits in language modeling
% June 2017

method = 'pml';

load(method)
fig = figure(1);
clf(fig)
ax = axes(fig);

for i = 7:-1:1
    plot((1:numel(progression{i}))*1000, progression{i})
    hold on
end

set(ax, 'TickLabelInterpreter', 'latex')
legend({'septigrams', 'sexigrams', 'quintigrams', 'quadrigrams', 'trigrams', ...
    'bigrams', 'unigrams'}, 'Interpreter', 'latex', ...
    'Location', 'best')
xlabel('number of words', 'Interpreter', 'latex')
ylabel('estimated entropy', 'Interpreter', 'latex')
xlim([0 12e5])
savefig(fig, ['ptb_' method])
saveas(fig, ['ptb_' method], 'epsc')
