clear;clc;

c = hot(256);      % 原始 colormap

c2 = c(1:120, :); 

path_ori = "D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\slice\4_14data\pmap2.tif";
img = imread(path_ori);
img = im2gray(img(:,:,1:3));

[~, w, ~] = size(img);

f1 = figure(2);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [24, 12, 19, 8];

hold on

gap = 2500;

x1 = linspace(0, gap, 23);
for i = 1:23
    path = sprintf("D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Output\\slice\\4_14data\\%d.tif", i-1);
    A = -0.01*i+1;
    sub(x1(i), w, path, A)
end

x2 = linspace(6000, 6000+gap, 23);
for i = 1:23
    path = sprintf("D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Output\\slice\\4_14data\\%d.tif", i+31);
    A = -0.01*i+1;
    sub(x2(i), w, path, A)
end

x3 = linspace(12000, 12000+gap, 23);
for i = 1:23
    path = sprintf("D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Output\\slice\\4_14data\\%d.tif", i+45);
    A = -0.01*i+1;
    sub(x3(i), w, path, A)
end

img = imread(path_ori);
img = img(:,:,1:3);
img = im2gray(img);
img = fliplr(img);

[Y, Z] = meshgrid(1:w, 1:w);
X = zeros(w, w)-(6000-gap);

alpha = img;

surf(X, Y, Z, img, ...
    'EdgeColor', 'none', ...
    'FaceColor', 'texturemap');

x = [-(6000-gap), -(6000-gap)];

y1 = [0, 0];
y2 = [0, w];
y3 = [w, w];

z1 = [0, 0];
z2 = [0, w];
z3 = [w, w];
 
plot3(x, y2, z1, '-', 'LineWidth', 2, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y1, z2, '-', 'LineWidth', 2, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y2, z3, '-', 'LineWidth', 2, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y3, z2, '-', 'LineWidth', 2, 'Color', [0.322, 0.369, 0.459]);


text(x1(1),0,-100, 'Layer A')
text(x2(1),0,-100, 'Layer B')
text(x3(1),0,-100, 'Layer C')

colormap('hot')
axis image
axis off
hold off
view(-83.5,1.3);

camlight;
lighting none;

function sub(x, w, path, A)
img = imread(path);
img = img(:,:,1:3);
img = im2gray(img);
img = fliplr(img);
%img = img.^2;

[Y, Z] = meshgrid(1:w, 1:w);
X = zeros(w, w)+x;

alpha = A*ones(w, w);

surf(X, Y, Z, img, ...
    'EdgeColor', 'none', ...
    'FaceColor', 'texturemap',...
    'FaceAlpha','texturemap',...
    'AlphaData',alpha);

x = [x, x];

y1 = [0, 0];
y2 = [0, w];
y3 = [w, w];

z1 = [0, 0];
z2 = [0, w];
z3 = [w, w];
 
plot3(x, y2, z1, '-', 'LineWidth', 1, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y1, z2, '-', 'LineWidth', 1, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y2, z3, '-', 'LineWidth', 1, 'Color', [0.322, 0.369, 0.459]);
plot3(x, y3, z2, '-', 'LineWidth', 1, 'Color', [0.322, 0.369, 0.459]);
end