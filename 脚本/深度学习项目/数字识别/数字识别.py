import tensorflow as tf
import numpy as np
import os
from PIL import Image

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 加载保存的模型
模型 = tf.keras.models.load_model("手写数字识别模型.keras")

# 加载并处理图像
图像路径 = "3.jpg"  # 选择你想要预测的图像文件
图像 = Image.open(图像路径).convert('L')  # 加载图像并转换为灰度模式
图像 = 图像.resize((28, 28))  # 调整图像大小为 28x28 像素

# 将图像转换为 numpy 数组并归一化
新图像 = np.array(图像) / 255.0  # 归一化到 [0, 1]
新图像 = 新图像.reshape(1, 28, 28, 1)  # 添加批次维度并重塑为 28x28x1 格式

# 使用模型进行预测
预测结果 = 模型.predict(新图像)
预测类别 = np.argmax(预测结果)  # 获取预测类别

# 假设你已经知道真实标签
真实标签 = 3  # 真实标签

print(f"模型预测类别: {预测类别}")
print(f"真实类别: {真实标签}")
