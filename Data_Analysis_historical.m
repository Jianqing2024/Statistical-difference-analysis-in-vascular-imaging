clear;clc
folderPath = "D:\WORK\Statistical-difference-analysis-in-vascular-imaging\Output\p_map\output_of_skeletonization";

matched_files_den = find_txt_files(folderPath, 'density');
matched_files_branch = find_txt_files(folderPath, 'branch');
matched_files_tif = find_tif_files(folderPath, 'branch');

data = cell(1,length(matched_files_branch));

for i = 1:length(matched_files_den)
    T_branch = TxT2Table(matched_files_branch{i});
    T_den = TxT2Table(matched_files_den{i});
    [~, data{i}.name, ~] = fileparts(matched_files_den{i});

    data{i}.total_length = Total_length(T_branch);
    data{i}.average_width = Average_width(T_den, T_branch);
    data{i}.total_branches = Total_branches(T_branch);
    data{i}.average_branch_length = Average_branch_length(T_branch);
    data{i}.vascular_density = Vascular_density(T_den);
    data{i}.average_curvature = Average_curvature(matched_files_tif{i});
end

save data_cau.mat data

S = [data{:}];
T = struct2table(S);
writetable(T, 'result.xlsx');

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Tabble = TxT2Table(filePath)
    opts = detectImportOptions(filePath, 'FileType', 'text');
    opts.VariableNamingRule = 'preserve';
    Tabble = readtable(filePath, opts); 
end

function matched_files = find_txt_files(folder, keyword)
    % 在指定文件夹下查找所有文件名中包含 keyword 的 txt 文件
    % 返回完整路径 cell 数组
    
    % 获取文件夹中所有 txt 文件
    files = dir(fullfile(folder, '*.txt'));
    
    matched_files = {};
    for k = 1:length(files)
        if contains(files(k).name, keyword)
            matched_files{end+1} = fullfile(folder, files(k).name);
        end
    end
end

function matched_files = find_tif_files(folder, keyword)
    % 在指定文件夹下查找所有文件名中包含 keyword 的 txt 文件
    % 返回完整路径 cell 数组
    
    % 获取文件夹中所有 txt 文件
    files = dir(fullfile(folder, '*.tif'));
    
    matched_files = {};
    for k = 1:length(files)
        if contains(files(k).name, keyword)
            matched_files{end+1} = fullfile(folder, files(k).name);
        end
    end
end

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function total_length = Total_length(T_branch)
% 总长度
total_length = 0;

for j = 1:height(T_branch)
    row = T_branch(j, :);

    Branch = (row.("# Branches"))*(row.("Average Branch Length"));
    total_length = total_length+Branch;
end

end

function average_width = Average_width(T_den, T_branch)
% 平均宽度
total_length = Total_length(T_branch);

total_pixel = T_den.('Total Area');

average_width = total_pixel/total_length;
end

function total_branches = Total_branches(T_branch)
% 总分支数
total_branches = sum(T_branch.("# Branches"));
end

function average_branch_length = Average_branch_length(T_branch)
% 平均分支长度
total_length = Total_length(T_branch);
total_branches = Total_branches(T_branch);

average_branch_length = total_length/total_branches;
end

function vascular_density = Vascular_density(T_den)
% 血管密度
vascular_density = T_den.('%Area');
end

function average_curvature = Average_curvature(I)
    I = imread(I);
    BW = I > 0;
    
    branch = bwmorph(BW, 'branchpoints');
    endpts = bwmorph(BW, 'endpoints');
    nodes = branch | endpts;
    
    %% 获取所有骨架点
    visited = false(size(BW));
    
    tortuosity_list = [];
    
    %% 遍历所有节点（作为起点）
    [node_y, node_x] = find(nodes);
    
    for i = 1:length(node_x)
    
        start = [node_y(i), node_x(i)];
    
        if visited(start(1), start(2))
            continue;
        end
    
        current = start;
        prev = start;
    
        path = current;
    
        while true
    
            neighbors = get_neighbors(current, BW);
    
            if isempty(neighbors)
                break;
            end
    
            next_found = false;
    
            for k = 1:size(neighbors,1)
    
                ny = neighbors(k,1);
                nx = neighbors(k,2);
    
                if ~visited(ny, nx)
    
                    next = [ny, nx];
                    next_found = true;
                    break;
    
                end
            end
    
            % 如果没有可走的邻居，结束
            if ~next_found
                break;
            end
    
            % 记录路径
            path = [path; next];
    
            % 标记访问
            visited(next(1), next(2)) = true;
    
            % 如果遇到另一个节点，结束
            if nodes(next(1), next(2)) && ...
               ~(next(1)==start(1) && next(2)==start(2))
                break;
            end
    
            % 更新当前位置
            prev = current;
            current = next;
    
        end
    
        %% 计算 tortuosity
        if size(path,1) > 1
    
            L = 0;
            for k = 2:size(path,1)
                L = L + norm(path(k,:) - path(k-1,:));
            end
    
            D = norm(path(end,:) - path(1,:));
    
            if D > 0
                tortuosity_list(end+1) = L / D;
            end
        end
    
    end
    
    %% 统计结果
    average_curvature = mean(tortuosity_list);
    %median_tortuosity = median(tortuosity_list);
    
    %fprintf('Mean tortuosity = %.4f\n', mean_tortuosity);
    %fprintf('Median tortuosity = %.4f\n', median_tortuosity);
end
%% 辅助函数：获取8邻域
function neighbors = get_neighbors(p, BW)

    dirs = [-1 -1; -1 0; -1 1;
             0 -1;        0 1;
             1 -1;  1 0;  1 1];

    neighbors = [];

    for i = 1:size(dirs,1)

        ny = p(1) + dirs(i,1);
        nx = p(2) + dirs(i,2);

        if ny >= 1 && nx >= 1 && ny <= size(BW,1) && nx <= size(BW,2)

            if BW(ny, nx)
                neighbors = [neighbors; ny, nx];
            end
        end
    end
end