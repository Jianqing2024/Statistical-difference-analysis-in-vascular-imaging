from glob import glob
from PIL import Image, ImageDraw, ImageFont
import os
import cv2

def pic(input_folder, output_folder, font):

    text_color = (255, 255, 255)  # 白色文字 (RGB)
    shadow_color = (0, 0, 0)  # 黑色阴影 (RGB)
    position = (20, -38)  # 左下角偏移 (x=左, y=底部向上)

    os.makedirs(output_folder, exist_ok=True)

    # 获取所有图片文件（按文件名数字排序）
    image_files = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith(('.tif'))],
        key=lambda x: int(''.join(filter(str.isdigit, x)))  # 提取文件名中的数字排序
    )

    bar_length_px = 91      # scale bar长度（像素）
    bar_thickness = 10       # 线宽
    margin = 50              # 边距

    for idx, filename in enumerate(image_files, start=1):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGB")
        
        draw = ImageDraw.Draw(img)
        
        # 文字内容
        text = f"Num.{idx}"
        
        # 计算文字位置（左下角）
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        img_width, img_height = img.size
        x = position[0]  # 水平偏移
        y = img_height - text_height + position[1]  # 垂直偏移（从底部向上）
        
        # ========= Scale Bar =========
        # 放在右下角
        bar_x1 = img_width - bar_length_px - margin
        bar_y1 = img_height - margin
        bar_x2 = img_width - margin
        bar_y2 = bar_y1

        # 画线
        draw.line(
            [(bar_x1, bar_y1), (bar_x2, bar_y2)],
            fill=(255, 255, 255),
            width=bar_thickness
        )
        
        # ========= 可选：scale文字 =========
        scale_text = "1 mm"   # 你自己定义
        
        bbox2 = font.getbbox(scale_text)
        sw = bbox2[2] - bbox2[0]
        sh = bbox2[3] - bbox2[1]
        
        text2_x = bar_x1 + (bar_length_px - sw) // 2-20
        text2_y = bar_y1 - sh - 30  # 在线上方
        
        draw.text((text2_x + 2, text2_y + 2), scale_text, font=font, fill=shadow_color)
        draw.text((text2_x, text2_y), scale_text, font=font, fill=text_color)

        # 保存
        output_path = os.path.join(output_folder, filename)
        img.save(output_path)
        
        # 保存图片
        output_path = os.path.join(output_folder, filename)
        img.save(output_path)
        print(f"Processed: {filename} -> {output_path}")

    print("All images processed!")
#########################################################################################################
# 设置字体（Times New Roman）
font_size = 60  # 字体大小
try:
    # Windows 和 macOS 通常自带 Times New Roman
    font = ImageFont.truetype("times.ttf", font_size)  # Windows
    # font = ImageFont.truetype("Times New Roman.ttf", font_size)  # macOS
except:
    try:
        # 如果默认路径找不到，尝试其他常见路径
        font = ImageFont.truetype("timesbd.ttf", font_size)  # 加粗版本
    except:
        print("Times New Roman 字体未找到，使用默认字体。")
        font = ImageFont.load_default()  # 备用字体

pic("Group_A", "A", font)
pic("Group_B", "B", font)
pic("Group_C", "C", font)

folder = "A"
current_dir = os.getcwd()
all_files_A = []
folder_path = os.path.join(current_dir, folder)
if os.path.exists(folder_path):
    # 查找该文件夹下所有 .tif 文件
    png_files = glob(os.path.join(folder_path, '*.tif'))
    all_files_A.extend(png_files)  # 添加到总列表
else:
    print(f"警告: 文件夹不存在 -> {folder_path}")

text_color = (255, 255, 255)  # 白色文字 (RGB)
shadow_color = (0, 0, 0)  # 黑色阴影 (RGB)

print(len(all_files_A))

for j in range(len(all_files_A)):
    # 假设是你的图片路径列表
    image_files = [f'd:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\A\\{j}.tif', 
                   f'd:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\B\\{j}.tif', 
                   f'd:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\C\\{j}.tif']


    # 读取所有图片
    images = [Image.open(f).convert("RGB") for f in image_files]

    # 间隔
    gap = 100

    # 高度检查
    heights = [img.height for img in images]
    assert len(set(heights)) == 1, "所有图片高度必须相同"

    height = images[0].height

    # 总宽度 = 所有图宽 + 间隔
    total_width = sum(img.width for img in images) + gap * (len(images) - 1)+160

    # 创建画布（黑色背景）
    new_img = Image.new("RGB", (total_width, height+150), color=(0, 0, 0))

    # 拼接
    x_offset = 80
    for i, img in enumerate(images):
        new_img.paste(img, (x_offset, 100))
        x_offset += img.width
        
        # 最后一张不加间隔
        if i < len(images) - 1:
            x_offset += gap

    draw = ImageDraw.Draw(new_img)

    labels = ["AOM/DSS", "CT26", "HC"]

    # 画布尺寸
    W, H = new_img.size

    # 顶部区域高度（你设的是100）
    top_margin = 100

    # 计算y（垂直居中）
    bbox = font.getbbox(labels[0])
    text_height = bbox[3] - bbox[1]
    y = (top_margin - text_height) // 2

    # 均匀分布（1/6, 3/6, 5/6）
    for k, text in enumerate(labels):
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        
        x = int((2*k + 1) / 6 * W - text_width / 2)

        # 阴影
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
        # 正文
        draw.text((x, y), text, font=font, fill=text_color)

        # 保存
        new_img.save(f"D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\vedio\\merged_{j}.tif")

    print("Done!")

#############################################################################################################

# =========================
# 参数设置
# =========================
image_folder = "vedio"     # 图片文件夹路径
output_path = "vedio\\video.mp4"      # 输出视频
fps = 30                        # 帧率
repeat_frame = 5               # 每张图重复帧数（=1表示不重复）

# 支持的图片格式
extensions = ["*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff"]

# =========================
# 读取文件（自动排序）
# =========================
files = []
for ext in extensions:
    files.extend(glob(os.path.join(image_folder, ext)))

files = sorted(files)

files = sorted(files, key=lambda x: int(''.join(filter(str.isdigit, x))))
print(files)

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