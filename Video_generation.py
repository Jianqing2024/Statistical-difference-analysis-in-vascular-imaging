import cv2
import glob
import os

# =========================
# 参数设置
# =========================
image_folder = "vedio"     # 图片文件夹路径
output_path = "video.mp4"      # 输出视频
fps = 30                        # 帧率
repeat_frame = 20               # 每张图重复帧数（=1表示不重复）

# 支持的图片格式
extensions = ["*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff"]

# =========================
# 读取文件（自动排序）
# =========================
files = []
for ext in extensions:
    files.extend(glob.glob(os.path.join(image_folder, ext)))

files = sorted(files)

if len(files) == 0:
    raise ValueError("文件夹中没有找到图片！")

print(f"共读取 {len(files)} 张图片")

# =========================
# 读取第一张图确定尺寸
# =========================
first_img = cv2.imread(files[0])

if first_img is None:
    raise ValueError("第一张图读取失败，请检查路径")

height, width = first_img.shape[:2]

# =========================
# 初始化视频写入器
# =========================
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式
video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# =========================
# 写入视频
# =========================
for i, file in enumerate(files):
    img = cv2.imread(file)

    if img is None:
        print(f"跳过无法读取的文件: {file}")
        continue

    # 写入多帧（用于控制显示时间）
    for _ in range(repeat_frame):
        video.write(img)

    print(f"已处理: {i+1}/{len(files)}")

# =========================
# 释放资源
# =========================
video.release()
print("视频生成完成:", output_path)