clear;clc
files = dir('*.tif');
load normalDATA.mat

for i = 1:numel(files)
    I = imread(files(i).name);
    BW = I > 0;
    imshow(BW)
    
    branch = bwmorph(BW, 'branchpoints');
    endpts = bwmorph(BW, 'endpoints');
    nodes = branch | endpts;
    
    %% 4. 获取所有骨架点
    [y_all, x_all] = find(BW);
    
    visited = false(size(BW));
    
    tortuosity_list = [];
    
    %% 5. 遍历所有节点（作为起点）
    [node_y, node_x] = find(nodes);
    
    for l = 1:length(node_x)
    
        start = [node_y(l), node_x(l)];
    
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
    
    %% 6. 统计结果
    files(i).mean_tortuosity = mean(tortuosity_list);
    files(i).median_tortuosity = median(tortuosity_list);
    files(i).Branches = normalDATA(1,i);
    files(i).ABL = normalDATA(2,i);
    files(i).MBL = normalDATA(3,i);

    fprintf('Mean tortuosity = %.4f\n', files(i).mean_tortuosity);
    fprintf('Median tortuosity = %.4f\n', files(i).median_tortuosity);

end
names = strings(numel(files),1);

for i = 1:numel(files)
    names(i) = files(i).name;
    mean_tortuosity(i) = files(i).mean_tortuosity;
    median_tortuosity(i) = files(i).median_tortuosity;
    Branches(i) = files(i).Branches;
    ABL(i) = files(i).ABL;
    MBL(i) = files(i).MBL;
end

save data.mat files

T = table( ...
    names, ...
    mean_tortuosity(:), ...
    median_tortuosity(:), ...
    Branches(:), ...
    ABL(:), ...
    MBL(:), ...
    'VariableNames', { ...
        'FileName', ...
        'MeanTortuosity', ...
        'MedianTortuosity', ...
        'Branches', ...
        'AverageBranchLength_um', ...
        'MaxBranchLength_um' ...
    });
writetable(T, 'vessel_analysis.xlsx');

    %% 7. 辅助函数：获取8邻域
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