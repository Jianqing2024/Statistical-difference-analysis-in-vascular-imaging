clear;clc;close all
f1 = figure(1);
f1.Color = 'w';
f1.Units = "centimeters";
f1.Position = [24, 12, 19, 6];

t = tiledlayout(2, 6);
t.TileSpacing = "tight";
t.Padding = "compact";

nexttile(1, [1, 2])
little_map1 = imread('35.tif');
imshow(little_map1(:,:,1:3))
nexttile(3, [1, 2])
little_map1 = imread('35.tif');
imshow(little_map1(:,:,1:3))
nexttile(5, [1, 2])
little_map1 = imread('35.tif');
imshow(little_map1(:,:,1:3))
nexttile(7, [1, 1])
bscan1 = imread('temaaa.png');
imshow(bscan1)
nexttile(8, [1, 1])

nexttile(9, [1, 1])
bscan2 = imread('temaaa.png');
imshow(bscan2)
nexttile(10, [1, 1])

nexttile(11, [1, 1])
bscan3 = imread('temaaa.png');
imshow(bscan3)
nexttile(12, [1, 1])