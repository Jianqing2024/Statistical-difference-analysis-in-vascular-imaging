clear;clc;close all

set(groot, ...
    'defaultAxesFontName','Arial', ...
    'defaultTextFontName','Arial', ...
    'defaultLegendFontName','Arial');

color_of_AOM = '#d34a24';
color_of_CT26 = '#3c7f72';
color_of_HC = '#ffaf00';
color_of_stand = '#406682';
color_of_Error = '#566071';
color_of_ex = '#ced3d7';

AOM = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\quan\37data\Anti_ROI_thickness.txt")*7.5e-3;
CT26 = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\quan\1_1170data\Anti_ROI_thickness.txt")*7.5e-3;
HC = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\quan\data_normal\Anti_ROI_thickness.txt")*7.5e-3;

m_AOM = mean(AOM);
m_CT26 = mean(CT26);
m_HC = mean(HC);

disp(mean(CT26(1250:1500)))
disp(mean(HC(1:250)))

y = linspace(0,27,1500);

f1 = figure(1);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [25, 3, 15, 8];

ax1 = axes;
ax1.Units = 'centimeters';
ax1.Position = [2, 2, 3.25, 1.6];
hold on
plot(y,AOM, 'Color', color_of_AOM)
yline(m_AOM, '--', 'Color', color_of_AOM, 'Alpha', 0.5)

plot(y,HC, 'Color', color_of_ex, 'LineStyle','-')

text(6.75,1.15,...
    sprintf('Mean = %.2f mm', m_AOM),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)

hold off

ax1.XTick = [5, 15, 25];
ax1.XTickLabel = {'5', '15', '25'};
ax1.XLim = [-0.5, 27.5];
ax1.YLim = [0.4, 1.3];
ax1.YTick = [0.6, 0.8, 1, 1.2];
ax1.YTickLabel = {'0.6', '0.8', '1.0', '1.2'};
xlabel('Probe travel distance (mm)');
ylabel('Thickness (mm)')
box on
grid on
ax1.FontSize = 6;

%%
f2 = figure(2);
f2.Color = 'w';
f2.Units = "centimeters";
f2.Position = [25, 13, 15, 8];

ax2 = axes;
ax2.Units = 'centimeters';
ax2.Position = [2, 2, 3.25, 1.6];

hold on
plot(y,CT26,'Color', color_of_CT26)
yline(m_CT26, '--', 'Color', color_of_CT26, 'Alpha', 0.5)

plot(y,HC, 'Color', color_of_ex, 'LineStyle','-')

text(6.75,1.15,...
    sprintf('Mean = %.2f mm', m_CT26),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
hold off

ax2.XTick = [5, 15, 25];
ax2.XTickLabel = {'5', '15', '25'};
ax2.XLim = [-0.5, 27.5];
ax2.YLim = [0.4, 1.3];
ax2.YTick = [0.6, 0.8, 1, 1.2];
ax2.YTickLabel = {'0.6', '0.8', '1.0', '1.2'};
xlabel('Probe travel distance (mm)');
ylabel('Thickness (mm)');
box on
grid on
ax2.FontSize = 6;

%%
f3 = figure(3);
f3.Color = 'w';
f3.Units = "centimeters";
f3.Position = [12, 18, 15, 8];

ax3 = axes;
ax3.Units = 'centimeters';
ax3.Position = [2, 2, 3.25, 1.6];

hold on
plot(y,HC,'Color', color_of_HC)
yline(m_HC, '--', 'Color', color_of_HC, 'Alpha', 0.5)

text(6.75,1.15,...
    sprintf('Mean = %.2f mm', m_HC),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom',...
    'FontSize', 6)
hold off

ax3.XTick = [5, 15, 25];
ax3.XTickLabel = {'5', '15', '25'};
ax3.XLim = [-0.5, 27.5];
ax3.YLim = [0.4, 1.3];
ax3.YTick = [0.6, 0.8, 1, 1.2];
ax3.YTickLabel = {'0.6', '0.8', '1.0', '1.2'};
xlabel('Probe travel distance (mm)');
ylabel('Thickness (mm)')
box on
grid on
ax3.FontSize = 6;