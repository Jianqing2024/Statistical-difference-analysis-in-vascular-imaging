clear;clc;close all
tbl = readtable("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\核质比.xlsx", 'VariableNamingRule', 'preserve');

set(groot, ...
    'defaultAxesFontName','Arial', ...
    'defaultTextFontName','Arial', ...
    'defaultLegendFontName','Arial');

color_of_AOM = '#d34a24';
color_of_CT26 = '#3c7f72';
color_of_HC = '#ffaf00';
color_of_stand = '#406682';
color_of_Error = '#566071';

% data = [ ...
%     tbl{:,1}; ...
%     tbl{:,2}; ...
%     tbl{:,3} ...
% ];
% 
% group = [ ...
%     repmat("G1", height(tbl), 1); ...
%     repmat("G2", height(tbl), 1); ...
%     repmat("G3", height(tbl), 1) ...
% ];
% 
% [p, tbl2, stats] = anova1(data, group);
% 
% multcompare(stats)

f1 = figure(1);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [24, 12, 5, 5];

hold on
r1 = raincloudplot(tbl, "AOM\DSS");
r1.FaceColor = color_of_AOM;
hold off
box on
xlabel('NAF (%)')
text(20,1.6,...
    sprintf('Mean = %3.2f%%', mean(tbl.("AOM\DSS"))),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)

ax1 = gca;
ax1.Units = "centimeters";
ax1.Position = [1,1,3,2];
ax1.XLim = [8, 48];
ax1.YTick = [];
ax1.YLim = [0,2];
ax1.FontSize = 6;
%%
f2 = figure(2);
f2.Color = 'w';
f2.Units = "centimeters";
f2.Position = [30, 12, 5, 5];

hold on
r2 = raincloudplot(tbl, "CT26");
r2.FaceColor = color_of_CT26;
hold off
box on
xlabel('NAF (%)')
text(20,1.6,...
    sprintf('Mean = %3.2f%%', mean(tbl.CT26)),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)

ax2 = gca;
ax2.Units = "centimeters";
ax2.Position = [1,1,3,2];
ax2.XLim = [8, 48];
ax2.YTick = [];
ax2.YLim = [0,2];
ax2.FontSize = 6;
%%
f3 = figure(3);
f3.Color = 'w';
f3.Units = "centimeters";
f3.Position = [36, 12, 5, 5];

hold on
r3 = raincloudplot(tbl, "HC");
r3.FaceColor = color_of_HC;
hold off
box on
xlabel('NAF (%)')
text(20,1.6,...
    sprintf('Mean = %3.2f%%', mean(tbl.HC)),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)

ax3 = gca;
ax3.Units = "centimeters";
ax3.Position = [1,1,3,2];
ax3.XLim = [8, 48];
ax3.YTick = [];
ax3.YLim = [0,2];
ax3.FontSize = 6;
