import tensorflow as tf
import os

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. 加载 MNIST 数据集
# MNIST 数据集包含 28x28 像素的手写数字图像，分为训练集和测试集
# 这里用 "特征" 表示图像数据，用 "标签" 表示对应的数字标签
(训练特征, 训练标签), (测试特征, 测试标签) = tf.keras.datasets.mnist.load_data()

# 2. 数据预处理
# 将像素值从 [0, 255] 归一化到 [0, 1]，加快训练速度并提高模型性能
训练特征, 测试特征 = 训练特征 / 255.0, 测试特征 / 255.0

# 3. 构建卷积神经网络模型
# 使用 Keras 的 Sequential 模型，按层次顺序构建网络
模型 = tf.keras.models.Sequential([
    # 将输入重构为 28x28x1 格式，因为卷积层需要明确的输入通道数（灰度图像有 1 个通道）
    tf.keras.layers.Reshape(target_shape=(28, 28, 1), input_shape=(28, 28)),
    
    # 第一层卷积层，使用 32 个 3x3 的卷积核，激活函数使用 ReLU
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    # 第一层池化层，使用 2x2 的池化窗口
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    # 第二层卷积层，使用 64 个 3x3 的卷积核，激活函数使用 ReLU
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    # 第二层池化层，使用 2x2 的池化窗口
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    # 展平层，将多维特征转换为一维向量，以便输入到全连接层
    tf.keras.layers.Flatten(),
    
    # 全连接层，包含 128 个神经元，激活函数使用 ReLU
    tf.keras.layers.Dense(128, activation='relu'),
    
    # 输出层，包含 10 个神经元（对应 0-9 十个类别），激活函数使用 softmax 以输出概率
    tf.keras.layers.Dense(10, activation='softmax')
])

# 4. 编译模型
# 使用 Adam 优化器，交叉熵损失函数和准确率作为评价指标
模型.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5. 训练模型
# 使用训练数据训练模型，设置训练轮数为 5，20% 的训练数据用作验证集
模型.fit(训练特征, 训练标签, epochs=5, validation_split=0.2)

# 6. 评估模型
# 在测试集上评估模型的性能，并输出测试准确率
测试损失, 测试准确率 = 模型.evaluate(测试特征, 测试标签)
print(f"测试集准确率: {测试准确率}")

# 7. 保存模型（可选）
# 使用推荐的 .keras 格式来保存模型
模型.save("手写数字识别模型.keras")