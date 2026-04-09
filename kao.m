clear;clc
folderPath = "D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\output_of_skeletonization";

matched_files_A = find_txt_files(folderPath, 'den');
matched_files_B = find_txt_files(folderPath, 'branch');

TA = ones(length(matched_files_A), 1);  % 用 cell 存储表格

TL = ones(length(matched_files_B), 1);

width = ones(length(matched_files_B), 1);

for i = 1:length(matched_files_A)
    filePath_A = matched_files_A{i};
    opts = detectImportOptions(filePath_A, 'FileType', 'text');
    opts.VariableNamingRule = 'preserve';  % 保留原始列名
    T = readtable(filePath_A, opts);  % 存入 cell
    TA(i) = T.('Total Area');
end

for i = 1:length(matched_files_B)
    filePath_B = matched_files_B{i};
    opts = detectImportOptions(filePath_B, 'FileType', 'text');
    opts.VariableNamingRule = 'preserve';  % 保留原始列名
    T = readtable(filePath_B, opts);  % 存入 cell

    Branch = 0;
    TL(i) = 0;
    for j = 1:height(T)
        row = T(j, :);

        Branch = (row.("# Branches"))*(row.("Average Branch Length"));
        TL(i) = TL(i)+Branch;
    end
end

for i = 1:length(matched_files_B)
    width(i) = TA(i)/TL(i);
end

disp(width)

function matched_files = find_txt_files(folder, keyword)
% 在指定文件夹下查找所有文件名中包含 keyword 的 txt 文件
% 返回完整路径 cell 数组

% 获取文件夹中所有 txt 文件
files = dir(fullfile(folder, '*.txt'));

matched_files = {};
for k = 1:length(files)
    if contains(files(k).name, keyword)
        matched_files{end+1} = fullfile(folder, files(k).name);
    end
end

end