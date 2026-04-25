clear;clc
folder = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\slice';

z = linspace(210, 310, 100);

files = dir(fullfile(folder, '**', '*.xlsx'));
n = length(files);

data_cols = cell(1,5);
file_names = cell(1,n);   % 存文件名

for i = 1:n
    file_path = fullfile(files(i).folder, files(i).name);

    % 去掉扩展名
    [~, name, ~] = fileparts(files(i).name);
    file_names{i} = name;

    T = readtable(file_path);

    for col = 2:6
        data_cols{col-1}{i} = T{:, col};
    end
end

for k = 1:5
    figure;
    hold on;

    for i = 1:n
        y = data_cols{k}{i};
        plot(z, y);
    end

    col_name = T.Properties.VariableNames{k+1};

    title(col_name, 'Interpreter', 'none');
    xlabel('z/um');
    ylabel('Value');
    grid on;

    legend(file_names, 'Interpreter', 'none'); % 加这一句
end

