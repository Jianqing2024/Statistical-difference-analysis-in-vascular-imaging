clear;clc
files = dir('*.png');

I = zeros(1024,1024);
for i=1:numel(files)
    I = I+double(imread(files(i).name));
end
I = I / numel(files);

imagesc(I)
colormap gray
axis equal
axis off