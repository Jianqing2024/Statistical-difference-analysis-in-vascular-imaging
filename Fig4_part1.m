clear;clc;close all
unit = 7.5e-3;
set(groot, ...
    'defaultAxesFontName','Arial', ...
    'defaultTextFontName','Arial', ...
    'defaultLegendFontName','Arial');

color_of_AOM = '#d34a24';
color_of_CT26 = '#3c7f72';
color_of_HC = '#ffaf00';
color_of_stand = '#674448';
color_of_Error = '#566071';

standard = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\quan\data_normal\Anti_ROI_thickness.txt")*unit;

data_37_ROI = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\37data\ROI_thickness.txt")*unit;

[h1, t1, c1, st1] = ttest2([standard(1:251); standard(351:551); standard(1151:1301)], data_37_ROI);

data_1170_ROI = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\1_1170data\ROI_thickness.txt")*unit;

[h2, t2, c2, st2] = ttest2(standard(1:251), data_1170_ROI);

data_nor2 = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\quan\data_normal2\Anti_ROI_thickness.txt")*unit;

[h3, t3, c3, st3] = ttest2(standard(1:150), data_nor2(1:150));

c = hot(256);

c = c(1:120, :); 

%%
f1 = figure(1);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [24, 12, 10, 10];

ax1 = axes;
ax1.Units = 'centimeters';
ax1.Position = [1,1,2.5,2.5];

hold on
b1 = bar([mean([standard(1:251); standard(351:551); standard(1151:1301)]), mean(data_37_ROI)]);

errorbar(1, mean([standard(1:251); standard(351:551); standard(1151:1301)]), ...
    std([standard(1:251); standard(351:551); standard(1151:1301)]), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);
errorbar(2, mean(data_37_ROI), ...
    std(data_37_ROI), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);

text(1,mean([standard(1:251); standard(351:551); standard(1151:1301)])+0.07,...
    sprintf('%3.2f', mean([standard(1:251); standard(351:551); standard(1151:1301)])),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
text(2,mean(data_37_ROI)+0.05,...
    sprintf('%3.2f', mean(data_37_ROI)),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
hold off
b1.FaceColor = 'flat';
b1.CData(1,:) = hex2rgb(color_of_stand);
b1.CData(2,:) = hex2rgb(color_of_AOM);
b1.LineWidth = 0.25;
b1.FaceAlpha = 0.2;
b1.EdgeColor = "flat";
box on
grid on
axis square

ax1.XLim = [0, 3];
ax1.YLim = [0, 1.45];
ax1.XTick = [1,2];
ax1.XTickLabel = {'Standard', 'AOM/DSS'};
ax1.TickLength = [0.025,1];
xtickangle(ax1, 20);
title('Thickness (mm)')
ax1.FontSize = 8;

%%
f2 = figure(2);
f2.Color = 'w';
f2.Units = "centimeters";
f2.Position = [24, 12, 10, 10];

ax2 = axes;
ax2.Units = 'centimeters';
ax2.Position = [1,1,2.5,2.5];

hold on

b2 = bar([mean(standard(1:251)), mean(data_1170_ROI)]);

errorbar(1, mean(standard(1:251)), ...
    std(standard(1:251)), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);
errorbar(2, mean(data_1170_ROI), ...
    std(data_1170_ROI), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);

text(1,mean(standard(1:251))+0.07,...
    sprintf('%3.2f', mean([standard(1:251); standard(351:551); standard(1151:1301)])),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
text(2,mean(data_1170_ROI)+0.05,...
    sprintf('%3.2f', mean(data_1170_ROI)),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
hold off
ylim([50, 200])
b2.FaceColor = 'flat';
b2.CData(1,:) = hex2rgb(color_of_stand);
b2.CData(2,:) = hex2rgb(color_of_CT26);
b2.LineWidth = 0.25;
b2.FaceAlpha = 0.2;
b2.EdgeColor = "flat";
box on
grid on
axis square
ax2.XLim = [0, 3];
ax2.YLim = [0, 1.45];
ax2.XTick = [1,2];
ax2.XTickLabel = {'Standard', 'CT26'};
ax2.TickLength = [0.025,1];
xtickangle(ax2, 20);
title('Thickness (mm)')
ax2.FontSize = 8;

%%
f3 = figure(3);
f3.Color = 'w';
f3.Units = "centimeters";
f3.Position = [24, 12, 10, 10];

ax3 = axes;
ax3.Units = 'centimeters';
ax3.Position = [1,1,2.5,2.5];

hold on
b3 = bar([mean(standard(1:150)), mean(data_nor2(1:150))]);

errorbar(1, mean(standard(1:150)), ...
    std(standard(1:150)), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);
errorbar(2, mean(data_nor2(1:150)), ...
    std(data_nor2(1:150)), ...
    'Marker', "square",...
    'MarkerFaceColor', color_of_Error,...
    'Color', color_of_Error,...
    'MarkerSize', 4);

text(1,mean(standard(1:150))+0.07,...
    sprintf('%3.2f', mean([standard(1:251); standard(351:551); standard(1151:1301)])),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
text(2,mean(standard(1:150))+0.04,...
    sprintf('%3.2f', mean(data_nor2(1:150))),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
hold off
ylim([50, 200])
b3.FaceColor = 'flat';
b3.CData(1,:) = hex2rgb(color_of_stand);
b3.CData(2,:) = hex2rgb(color_of_HC);
b3.LineWidth = 0.25;
b3.FaceAlpha = 0.2;
b3.EdgeColor = "flat";
box on
grid on
axis square
ax3.XLim = [0, 3];
ax3.YLim = [0, 1.45];
ax3.XTick = [1,2];
ax3.XTickLabel = {'Standard', 'HC'};
ax3.TickLength = [0.025,1];
xtickangle(ax3, 20);
title('Thickness (mm)')
ax3.FontSize = 8;
