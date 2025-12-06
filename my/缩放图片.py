from PIL import Image

# 加载图像
image = Image.open('images\\yuanshen.png')

image.show()
# 计算缩放因子
width, height = image.size
print(image.size)
max_size = (700, 450)  # 假设最大尺寸为200x150

# 计算缩放因子
width_factor = max_size[0] / width
height_factor = max_size[1] / height
factor = min(width_factor, height_factor)

# 使用缩放因子计算新的图像尺寸
new_size = (int(width * factor), int(height * factor))

# 调整图像大小
resized_image_with_ratio = image.resize(new_size)

# 显示调整大小后的图像
resized_image_with_ratio.show()

# 保存
resized_image_with_ratio.save('yuanshen1.png')