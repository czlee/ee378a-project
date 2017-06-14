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
