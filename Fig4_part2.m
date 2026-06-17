clear;clc;close all

set(groot, ...
    'defaultAxesFontName','Arial', ...
    'defaultTextFontName','Arial', ...
    'defaultLegendFontName','Arial');

color_of_AOM = '#d34a24';
color_of_CT26 = '#3c7f72';
color_of_HC = '#ffaf00';
color_of_Error = '#566071';

% color_of_AOM = '#bd3d3f';
% color_of_CT26 = '#104b51';
% color_of_HC = '#674448';
% color_of_Error = '#566071';

folder = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\slice';

files = dir(fullfile(folder, '**', '*.xlsx'));
n = length(files);
T = cell(3,1);
for i = 1:n
    file_path = fullfile(files(i).folder, files(i).name);
    T{i} = readtable(file_path); % 1AOM 2CT26 3HC
    T{i} = T{i}(:, 2:end);
end

% --- 定义组名 ---
groupNames = {'AOM/DSS', 'CT26', 'HC'}; 

% 获取参数名称（假设所有表格列名一致，取第一个表格的列名）
paramNames = T{1}.Properties.VariableNames;
numParams = length(paramNames);

% --- 初始化结果存储 ---
% 我们将结果存入一个元胞数组以便后续生成表格
Results = cell(numParams, 10); 
Results(:, 1) = paramNames; % 第一列放参数名
Results(1, 2:10) = {'Mean_AOM', 'Mean_CT26', 'Mean_HC', ...
                   'Stds_AOM', 'Stds_CT26', 'Stds_HC',...
                   'P(AOMvsCT26)', 'P(AOMvsHC)', 'P(CT26vsHC)'};

for i = 1:numParams
    % 1. 提取当前参数的三组数据
    % 使用 cell2mat 确保数据是数值向量（去除表格格式影响）
    data1 = table2array(T{1}(:, i)); % AOM
    data2 = table2array(T{2}(:, i)); % CT26
    data3 = table2array(T{3}(:, i)); % HC
    
    
    groupData = {data1, data2, data3};
    
    % 2. 计算均值和标准差
    means = zeros(1, 3);
    stds  = zeros(1, 3);
    
    for g = 1:3
        means(g) = mean(groupData{g});
        stds(g)  = std(groupData{g});
    end
    
    % 3. 进行 t-test (双样本t检验)
    % 比较 1 vs 2
    [~, p12] = ttest2(data1, data2);
    % 比较 1 vs 3
    [~, p13] = ttest2(data1, data3);
    % 比较 2 vs 3
    [~, p23] = ttest2(data2, data3);
    
    % 4. 保存统计数据到结果表
    Results{i, 2} = means(1); 
    Results{i, 3} = means(2); 
    Results{i, 4} = means(3);
    Results{i, 5} = stds(1); 
    Results{i, 6} = stds(2); 
    Results{i, 7} = stds(3);
    Results{i, 8} = p12;      
    Results{i, 9} = p13;      
    Results{i, 10} = p23;

    % da = [ ...
    %     data1; ...
    %     data2; ...
    %     data3 ...
    %     ];
    % 
    % group = [ ...
    %     repmat("G1", numel(data1), 1); ...
    %     repmat("G2", numel(data2), 1); ...
    %     repmat("G3", numel(data3), 1) ...
    % ];
    % 
    % [p, tbl, stats] = anova1(da, group);
    % multcompare(stats)
end
disp(Results)

x = {'HC', 'CT26', 'AOM/DSS'};

unit = 11.69; % um

VD = table(T{3}{:,1}*100, T{2}{:,1}*100, T{1}{:,1}*100, 'VariableNames', x);           % 不改
Branches = table(T{3}{:,2}, T{2}{:,2}, T{1}{:,2}, 'VariableNames', x);     % 不改
ABL = table(T{3}{:,3}*unit, T{2}{:,3}*unit, T{1}{:,3}*unit, 'VariableNames', x);
MD = table(T{3}{:,4}*unit, T{2}{:,4}*unit, T{1}{:,4}*unit, 'VariableNames', x);

f1 = figure(1);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [24, 12, 19, 7.5];

t = tiledlayout(2, 5);
t.TileSpacing = "compact";
t.Padding = "compact";

ax1 = nexttile(1);
hold on
v1 = violinplot(VD, x);
v1(3).FaceColor = color_of_AOM;
v1(2).FaceColor = color_of_CT26;
v1(1).FaceColor = color_of_HC;
ylabel('VD (%)')

errorbar(3,Results{1, 2}*100,Results{1, 5}*100, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(2,Results{1, 3}*100,Results{1, 6}*100, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(1,Results{1, 4}*100,Results{1, 7}*100, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
hold off
ax1.XTickLabel = x;
ax1.XTick = [1, 2, 3];
ax1.FontSize = 6;

ax2 = nexttile(2);
hold on
v2 = violinplot(Branches,x);
v2(3).FaceColor = color_of_AOM;
v2(2).FaceColor = color_of_CT26;
v2(1).FaceColor = color_of_HC;
ylabel('BN')

errorbar(3,Results{2, 2},Results{2, 5}, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(2,Results{2, 3},Results{2, 6}, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(1,Results{2, 4},Results{2, 7}, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
hold off
ax2.XTickLabel = x;
ax2.XTick = [1, 2, 3];
ax2.YTick = [0, 2000, 4000, 6000];
ax2.YAxis.Exponent = 3;
ax2.FontSize = 6;

ax6 = nexttile(6);
hold on
v3 = violinplot(ABL,x);
xticklabels(x);
v3(3).FaceColor = color_of_AOM;
v3(2).FaceColor = color_of_CT26;
v3(1).FaceColor = color_of_HC;
ylabel('ABL (μm)')

errorbar(3,Results{3, 2}*unit,Results{3, 5}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(2,Results{3, 3}*unit,Results{3, 6}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(1,Results{3, 4}*unit,Results{3, 7}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
hold off
ax6.XTickLabel = x;
ax6.XTick = [1, 2, 3];
ax6.FontSize = 6;

ax7 = nexttile(7);
hold on
v4 = violinplot(MD,x);
v4(3).FaceColor = color_of_AOM;
v4(2).FaceColor = color_of_CT26;
v4(1).FaceColor = color_of_HC;
ylabel('AVD (μm)')

errorbar(3,Results{4, 2}*unit,Results{4, 5}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(2,Results{4, 3}*unit,Results{4, 6}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
errorbar(1,Results{4, 4}*unit,Results{4, 7}*unit, 'Marker', "square", 'MarkerFaceColor', color_of_Error, 'Color', color_of_Error, 'MarkerSize', 4)
hold off
ax7.XTickLabel = x;
ax7.XTick = [1, 2, 3];
ax7.FontSize = 6;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%
T_area = readtable("area.xlsx", VariableNamingRule ="preserve");
T_branch_count = readtable("branch_count.xlsx", VariableNamingRule ="preserve");
T_mean_diameter = readtable("mean_diameter.xlsx", VariableNamingRule ="preserve");

folder_AOM = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\AOM';

files = dir(fullfile(folder_AOM, '**', '*.xlsx'));
n = length(files);

for i = 1:n
    file_path = fullfile(files(i).folder, files(i).name);
    
    T = readtable(file_path);
    
    T = T(:, 2:end);          % ❗去掉第一列（文件名）
    A = table2array(T);       % 再转数值矩阵
    
    if i == 1
        max_mat_AOM = A;
        min_mat_AOM = A;
    else
        max_mat_AOM = max(max_mat_AOM, A);
        min_mat_AOM = min(min_mat_AOM, A);
    end
end

folder_AOM = 'D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\CT26';

files = dir(fullfile(folder_AOM, '**', '*.xlsx'));
n = length(files);

for i = 1:n
    file_path = fullfile(files(i).folder, files(i).name);
    
    T = readtable(file_path);
    
    T = T(:, 2:end);          % ❗去掉第一列（文件名）
    A = table2array(T);       % 再转数值矩阵
    
    if i == 1
        max_mat_CT26 = A;
        min_mat_CT26 = A;
    else
        max_mat_CT26 = max(max_mat_CT26, A);
        min_mat_CT26 = min(min_mat_CT26, A);
    end
end

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%
x = (linspace(220, 309, 90)-175)*7.5e-3;
y_tem = ones(1, 100)*1.1;

ax3 = nexttile(3);
hold on
fill([x, fliplr(x)], [(max_mat_AOM(:,1)')/(930*1155)*100, fliplr(min_mat_AOM(:,1)')/(930*1155)*100],...
    hex2rgb(color_of_AOM), 'FaceAlpha', 0.2, 'EdgeColor', 'none');
fill([x, fliplr(x)], [(max_mat_CT26(:,1)')/(930*1155)*100, fliplr(min_mat_CT26(:,1)')/(930*1155)*100],...
    hex2rgb(color_of_CT26), 'FaceAlpha', 0.2, 'EdgeColor', 'none');

plot(x, T_area.AOM_mean/(930*1155)*100, 'Color', color_of_AOM)
plot(x, T_area.CT26_mean/(930*1155)*100, 'Color', color_of_CT26)
hold off
ax3.XLim = [x(1), x(end)];
ax3.XTick = [0.5, 0.75, 1.0];
ax3.XTickLabel = {'0.5', '0.75', '1.0'};
xlabel('Depth (mm)')
ylabel('VD (%)')
ax3.FontSize = 6;

ax4 = nexttile(4);
hold on
fill([x, fliplr(x)], [(max_mat_AOM(:,2)'), fliplr(min_mat_AOM(:,2)')],...
    hex2rgb(color_of_AOM), 'FaceAlpha', 0.2, 'EdgeColor', 'none');
fill([x, fliplr(x)], [(max_mat_CT26(:,2)'), fliplr(min_mat_CT26(:,2)')],...
    hex2rgb(color_of_CT26), 'FaceAlpha', 0.2, 'EdgeColor', 'none');

plot(x, T_branch_count.AOM_mean, 'Color', color_of_AOM)
plot(x, T_branch_count.CT26_mean, 'Color', color_of_CT26)
hold off
ax4.XLim = [x(1), x(end)];
ax4.XTick = [0.5, 0.75, 1.0];
ax4.XTickLabel = {'0.5', '0.75', '1.0'};
ax4.YLim = [0, 8e3];
ax4.YAxis.Exponent = 3;
xlabel('Depth (mm)')
ylabel('BN')
ax4.FontSize = 6;

ax5 = nexttile(5);
hold on
fill([x, fliplr(x)], [(max_mat_AOM(:,4)')*unit, fliplr(min_mat_AOM(:,4)')*unit],...
    hex2rgb(color_of_AOM), 'FaceAlpha', 0.2, 'EdgeColor', 'none');
fill([x, fliplr(x)], [(max_mat_CT26(:,4)')*unit, fliplr(min_mat_CT26(:,4)')*unit],...
    hex2rgb(color_of_CT26), 'FaceAlpha', 0.2, 'EdgeColor', 'none');

plot(x, T_mean_diameter.AOM_mean*unit, 'Color', color_of_AOM)
plot(x, T_mean_diameter.CT26_mean*unit, 'Color', color_of_CT26)
hold off
ax5.XLim = [x(1), x(end)];
ax5.XTick = [0.5, 0.75, 1.0];
ax5.XTickLabel = {'0.5', '0.75', '1.0'};
xlabel('Depth (mm)')
ylabel('AVD (μm)')
ax5.FontSize = 6;

ax8 = nexttile(8);
hold on
area(x, T_area.p_fdr, 'FaceColor', '#9eafbf', 'FaceAlpha', 0.25, 'EdgeColor', 'none')
plot(x, T_area.p_fdr, 'LineWidth', 1, 'Color', '#406682')

idx = (x >= x(3) & x <= x(33));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);

idx = (x >= x(59) & x <= x(62));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);

idx = (x >= x(71) & x <= x(85));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);
hold off
grid on
box on
ax8.XLim = [x(1), x(end)];
ax8.XTick = [0.5, 0.75, 1.0];
ax8.XTickLabel = {'0.5', '0.75', '1.0'};
ax8.YTick = [0.25, 0.75];
ax8.YLim = [0, 1.05];
ylabel('p-value')
xlabel('Depth (mm)')
ax8.FontSize = 6;

ax9 = nexttile(9);
hold on
area(x, T_branch_count.p_fdr, 'FaceColor', '#9eafbf', 'FaceAlpha', 0.25, 'EdgeColor', 'none')

plot(x, T_branch_count.p_fdr, 'LineWidth', 1, 'Color', '#406682')

idx = (x >= x(3) & x <= x(26));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);

idx = (x >= x(57) & x <= x(89));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);
hold off
grid on
box on
ax9.XLim = [x(1), x(end)];
ax9.XTick = [0.5, 0.75, 1.0];
ax9.XTickLabel = {'0.5', '0.75', '1.0'};
ax9.YTick = [0.25, 0.75];
ax9.YLim = [0, 1.05];
ylabel('p-value')
xlabel('Depth (mm)')
ax9.FontSize = 6;

ax10 = nexttile(10);
hold on
area(x, T_mean_diameter.p_fdr, 'FaceColor', '#9eafbf', 'FaceAlpha', 0.25, 'EdgeColor', 'none')

plot(x, T_mean_diameter.p_fdr, 'LineWidth', 1, 'Color', '#406682')

idx = (x >= x(34) & x <= x(56));
area(x(idx), y_tem(idx), 'FaceColor', '#566071', 'FaceAlpha', 0.5);
hold off
grid on
box on
ax10.XLim = [x(1), x(end)];
ax10.XTick = [0.5, 0.75, 1.0];
ax10.XTickLabel = {'0.5', '0.75', '1.0'};
ax10.YTick = [0.25, 0.75];
ax10.YLim = [0, 1.05];
ylabel('p-value')
xlabel('Depth (mm)')
ax10.FontSize = 6;