clear; clc;
folderPath = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\normal\output';
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

ABL = zeros(1,length(txtFiles));

for i = 1:length(txtFiles)
    ABL(i) = EVA(tableList{i});
end

normalDATA = ABL;

save normalDATA.mat normalDATA
%%
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

ABL = zeros(1,length(txtFiles));

for i = 1:length(txtFiles)
    ABL(i) = EVA(tableList{i});
end

tumerDATA = ABL;
save tumerDATA.mat tumerDATA

%%
folderPath = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\HC\output';
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

ABL = zeros(1,length(txtFiles));

for i = 1:length(txtFiles)
    ABL(i) = EVA(tableList{i});
end

HCDATA = ABL;
save HCDATA.mat HCDATA

%%
load normalDATA.mat
load tumerDATA.mat
load HCDATA.mat

A = normalDATA;
B = tumerDATA;
C = HCDATA;
%% 合并数据
data = [A B C];

%% 分组标签
group = [ ...
    ones(1,length(A)), ...
    2*ones(1,length(B)), ...
    3*ones(1,length(C)) ];

%% 单因素方差分析
[p,tbl,stats] = anova1(data,group);

fprintf('ANOVA p-value = %.4f\n',p)

%% 事后多重比较
figure
multcompare(stats)

function avgLength = EVA(T)
    
    totalBranches = sum(T.("# Branches"));

    avgLength = sum(T.("# Branches") .* T.("Average Branch Length")) ...
                / totalBranches;
end