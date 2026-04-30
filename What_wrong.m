clear;clc;close

x = linspace(0, 1500, 1500);

CT262 = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\1_1170data\Anti_ROI_thickness.txt");
CT261 = readmatrix("D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\新建文件夹\1_1170data\ROI_thickness.txt");

plot(CT261)
hold on
plot(CT262)