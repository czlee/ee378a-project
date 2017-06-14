maxn = 7;

progression = cell(maxn, 1);
estimates = zeros(maxn, 1);

for i =  1:maxn
    fprintf('Working on %dgrams.csv\n', i)
    filename = sprintf('../python/ptb/indices/%dgrams.csv', i);
    data = csvread(filename) + 1;
    N = numel(data);
    progression{i} = zeros(floor(N/1000), 1);
    for j = 1:N/1000
        if mod(j, 100) == 0
            fprintf('  up to %d\n', j)
        end
        progression{i}(j) = estEntroPMLapproximate(data(1:j*1000)+1);
    end
    estimates(i) = estEntroPMLapproximate(data+1);
end

save('pml', 'estimates', 'progression')
