from tqdm import tqdm
from pathlib import Path
import warnings
import pandas as pd
import Image_Reconstruction as ir

warnings.filterwarnings("ignore", module="skimage")
warnings.filterwarnings("ignore", module="skan")

current_dir = Path.cwd()
Main_path = current_dir / 'Output' / 'slice'

subfolders = [p for p in Main_path.iterdir() if p.is_dir()]

for folder in tqdm(subfolders):
    tif_files = list(folder.glob("*.tif"))

    results = []
    for file in tif_files:
        Statistical_values = ir.double_layer_skeletonization_py(file)
        results.append({
            "file_name": file,               # 记录文件名
            "area": Statistical_values["area"],
            "branch_count": Statistical_values["branch_count"],
            "average_branch_length": Statistical_values["average_branch_length"],
            "mean_diameter": Statistical_values["mean_diameter"],
            "tortuosity": Statistical_values["tortuosity"]})
        
    df = pd.DataFrame(results)
    output_path = folder / f"{folder.name}.xlsx"
    df.to_excel(output_path, index=False)