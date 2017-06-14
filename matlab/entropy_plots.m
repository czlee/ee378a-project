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

