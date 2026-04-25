from tqdm import tqdm
from pathlib import Path
import warnings
from scipy import stats
import Image_Reconstruction as ir
import numpy as np
from statsmodels.stats.multitest import multipletests
import pandas as pd

warnings.filterwarnings("ignore", module="skimage")
warnings.filterwarnings("ignore", module="skan")

def process_group(main_path):
    subfolders = [p for p in main_path.iterdir() if p.is_dir()]

    results = {
        "area": [],
        "branch_count": [],
        "average_branch_length": [],
        "mean_diameter": [],
        "tortuosity": []
    }

    for folder in tqdm(subfolders):
        tif_files = list(folder.glob("*.tif"))

        area = []
        branch_count = []
        average_branch_length = []
        mean_diameter = []
        tortuosity = []
        
        exe = []

        for file in tif_files:
            stat = ir.double_layer_skeletonization_statistical_purposes_only(file)

            area.append(stat["area"])
            branch_count.append(stat["branch_count"])
            average_branch_length.append(stat["average_branch_length"])
            mean_diameter.append(stat["mean_diameter"])
            tortuosity.append(stat["tortuosity"])

            exe.append({
                "file_name": file,               # 记录文件名
                "area": stat["area"],
                "branch_count": stat["branch_count"],
                "average_branch_length": stat["average_branch_length"],
                "mean_diameter": stat["mean_diameter"],
                "tortuosity": stat["tortuosity"]})

        results["area"].append(area)
        results["branch_count"].append(branch_count)
        results["average_branch_length"].append(average_branch_length)
        results["mean_diameter"].append(mean_diameter)
        results["tortuosity"].append(tortuosity)

        df_exe = pd.DataFrame(exe)
        output_path = folder / f"{folder.name}.xlsx"
        df_exe.to_excel(output_path, index=False)

    for key in results:
        results[key] = np.array(results[key])  # shape: (n_samples, n_z)

    return results

current_dir = Path.cwd()
AOM = process_group(current_dir / 'Output' / 'AOM')
CT26 = process_group(current_dir / 'Output' / 'CT26')

results_excel = {}

for key in AOM.keys():
    data1 = AOM[key]
    data2 = CT26[key]

    # ===== 逐点 t 检验 =====
    t_vals, p_vals = stats.ttest_ind(
        data1,
        data2,
        axis=0,
        equal_var=False
    )

    # ===== FDR 修正 =====
    reject, p_fdr, _, _ = multipletests(p_vals, method='fdr_bh')

    # ===== 计算均值（方便一起导出）=====
    mean1 = np.mean(data1, axis=0)
    mean2 = np.mean(data2, axis=0)

    # ===== 整理成 DataFrame =====
    df = pd.DataFrame({
        "z_index": np.arange(len(p_vals)),
        "AOM_mean": mean1,
        "CT26_mean": mean2,
        "t_value": t_vals,
        "p_value": p_vals,
        "p_fdr": p_fdr,
        "significant(FDR<0.05)": reject
    })

    results_excel[key] = df

# ===== 写入 Excel（每个参数一个 sheet）=====
output_path = "t_test_results.xlsx"

with pd.ExcelWriter(output_path) as writer:
    for key, df in results_excel.items():
        df.to_excel(writer, sheet_name=key, index=False)

print(f"结果已保存到: {output_path}")