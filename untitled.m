clear;clc;close all

I = nor(im2double(imread('200-250.tif')));
I2 = nor(im2double(imread('250-300.tif')));
I3 = nor(im2double(imread('300.tif')));

[m,n] = size(I);

y = linspace(0,14,n);
x = linspace(0,5,m);

[X,Y] = meshgrid(y,x);


% figure(1)
% im = imagesc(x,y,I2);
% im.AlphaData = I;
% colormap(load('acton.txt'))

%%
R = 2.5;
a = 0.25;
c = 1;
Z = -a*(Y-R).^2+c;

gap = 3.6;

Z2 = Z+gap;
Z3 = Z2+gap;

f = figure(1);
f.Color = 'k';

ax = axes;
s1 = surf(X,Y,Z3,I3);
s1.AlphaData = I3;
s1.FaceAlpha = 'interp'; 

hold on
s2 = surf(X,Y,Z2,I2);
s2.AlphaData = I2;
s2.FaceAlpha = 'interp'; 

s3 = surf(X,Y,Z,I);
s3.AlphaData = I;
s3.FaceAlpha = 'interp'; 
hold off

colormap(load('buda.txt'))
colormap hot

ax.Color = 'k';
ax.XColor = 'w';
ax.YColor = 'w';
ax.ZColor = 'w';

% lighting phong
camlight headlight

ax.XTick = [];
ax.YTick = [];
ax.ZTick = [];

xlabel('X','FontName','Times New Roman','Rotation',0)
ylabel('Y','FontName','Times New Roman','Rotation',0)
zlabel('Z','FontName','Times New Roman','Rotation',0)

shading interp
axis equal
view(3)
grid off


function A_norm = nor(A)

minVal = min(A(:)); % 获取整个矩阵的最小值
maxVal = max(A(:)); % 获取整个矩阵的最大值

% 防止分母为0的情况（如果矩阵所有元素相同）
if maxVal == minVal
    A_norm = zeros(size(A));
else
    A_norm = (A - minVal) / (maxVal - minVal);
end
end