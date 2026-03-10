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

load normalDATA.mat
load tumerDATA.mat

normalDATA = normalDATA';
tumerDATA = tumerDATA';

tVal = tumerDATA;
cVal = normalDATA;

% 均值
meanTumor = mean(tVal);
meanControl = mean(cVal);

% 95% 置信区间 (基于正态分布假设)
nT = length(tVal);
nC = length(cVal);
ciTumor = [meanTumor - 1.96*std(tVal)/sqrt(nT), meanTumor + 1.96*std(tVal)/sqrt(nT)];
ciControl = [meanControl - 1.96*std(cVal)/sqrt(nC), meanControl + 1.96*std(cVal)/sqrt(nC)];

% t 检验
[h,p,ciDiff] = ttest2(tVal, cVal);

fprintf('%s:\n', 'ABL');
fprintf('  Tumor Mean ± 95%% CI: %.2f [%.2f, %.2f]\n', meanTumor, ciTumor(1), ciTumor(2));
fprintf('  Control Mean ± 95%% CI: %.2f [%.2f, %.2f]\n', meanControl, ciControl(1), ciControl(2));
fprintf('  t-test p = %.3f, CI of difference = [%.2f, %.2f]\n\n', p, ciDiff(1), ciDiff(2));

function avgLength = EVA(T)
    
    totalBranches = sum(T.("# Branches"));

    avgLength = sum(T.("# Branches") .* T.("Average Branch Length")) ...
                / totalBranches;
end