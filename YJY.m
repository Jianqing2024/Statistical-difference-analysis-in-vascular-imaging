clear; clc;
folderPath = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\tumer\output';
txtFiles = dir(fullfile(folderPath, '*.txt'));

tableList = cell(length(txtFiles), 1);  % 用 cell 存储表格
fileNames = cell(length(txtFiles), 1);
for i = 1:length(txtFiles)
    filePath = fullfile(folderPath, txtFiles(i).name);  % 完整路径
    opts = detectImportOptions(filePath, 'FileType', 'text');
    opts.VariableNamingRule = 'preserve';  % 保留原始列名
    tableList{i} = readtable(filePath, opts);  % 存入 cell
    fileNames{i} = txtFiles(i).name;
end

Branches = zeros(1,length(txtFiles));
ABL = zeros(1,length(txtFiles));
MBL = zeros(1,length(txtFiles));

for i = 1:length(txtFiles)
    Branches(i) = sum(tableList{i}.("# Branches"));
end