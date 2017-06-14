maxn = 7;

progression = cell(maxn, 1);
estimates = zeros(maxn, 1);

for i = 1:maxn
    fprintf('Working on %dgrams.csv\n', i)
    filename = sprintf('../python/ptb/indices/%dgrams.csv', i);
    data = csvread(filename) + 1;
    N = numel(data);
    progression{i} = zeros(floor(N/1000), 1);
    for j = 1:N/1000
        if mod(j, 100) == 0
            fprintf('  up to %d\n', j)
        end
        f = makeFinger(data(1:j*1000));
        try
            progression{i}(j) = entropy_estC(f) / log(2);
        catch e
            % fprintf('Error in %d/%d: %s\r\n', i, j, getReport(e))
            progression{i}(j) = NaN;
        end
    end
    f = makeFinger(data);
    try
        estimates(i) = entropy_estC(f) / log(2);
    catch e
        % fprintf('Error in %d/end: %s\r\n', i, getReport(e))
        estimates(i) = progression{i}(find(~isnan(progression{i}), 1, 'last'));
    end
end

save('vv', 'estimates', 'progression')
