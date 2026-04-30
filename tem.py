from glob import glob
from PIL import Image, ImageDraw, ImageFont
import os

def pic(input_folder, output_folder, font):

    text_color = (255, 255, 255)  # 白色文字 (RGB)
    shadow_color = (0, 0, 0)  # 黑色阴影 (RGB)
    position = (20, -38)  # 左下角偏移 (x=左, y=底部向上)

    os.makedirs(output_folder, exist_ok=True)

    image_files = []
    if os.path.exists(input_folder):
        # 查找该文件夹下所有指定格式文件
        png_files = glob(os.path.join(input_folder, '*.tif'))
        image_files.extend(png_files)  # 添加到总列表
    else:
        print(f"警告: 文件夹不存在 -> {input_folder}")

    print(image_files)

    bar_length_px = 58      # scale bar长度（像素）
    bar_thickness = 15      # 线宽
    margin = 25             # 边距

    for idx, img_path in enumerate(image_files, start=1):
        img = Image.open(img_path).convert("RGB")
        img = img.rotate(-90, expand=True)
        
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
        '''
        scale_text = "1 mm"   # 你自己定义
        
        bbox2 = font.getbbox(scale_text)
        sw = bbox2[2] - bbox2[0]
        sh = bbox2[3] - bbox2[1]
        
        text2_x = bar_x1 + (bar_length_px - sw) // 2 -20
        text2_y = bar_y1 - sh - 50  # 在线上方
        
        draw.text((text2_x + 2, text2_y + 2), scale_text, font=font, fill=shadow_color)
        draw.text((text2_x, text2_y), scale_text, font=font, fill=text_color)
        '''

        # 保存
        filename = os.path.basename(img_path)
        output_path = os.path.join(output_folder, filename)
        img.save(output_path)

        print(f"Processed: {filename} -> {output_path}")

    print("All images processed!")

font_size = 80  # 字体大小
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

pic("D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\SCA", "D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\scale_bar_2", font)