import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# 梯度函数，用于平滑插值
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

# 线性插值
def lerp(t, a, b):
    return a + t * (b - a)

# 生成随机梯度向量
def random_gradient():
    angle = random.uniform(0, 2 * np.pi)
    return np.array([np.cos(angle), np.sin(angle)])

# 点积梯度
def dot_grid_gradient(ix, iy, x, y, gradients):
    dx, dy = x - ix, y - iy
    gradient = gradients[iy % len(gradients)][ix % len(gradients[0])]
    return dx * gradient[0] + dy * gradient[1]

# 生成柏林噪声
def perlin_noise(x, y, gradients, grid_size=100):
    x0, y0 = int(x // grid_size), int(y // grid_size)
    x1, y1 = x0 + 1, y0 + 1
    sx, sy = fade((x % grid_size) / grid_size), fade((y % grid_size) / grid_size)
    n0 = dot_grid_gradient(x0, y0, x, y, gradients)
    n1 = dot_grid_gradient(x1, y0, x, y, gradients)
    ix0 = lerp(sx, n0, n1)
    n0 = dot_grid_gradient(x0, y1, x, y, gradients)
    n1 = dot_grid_gradient(x1, y1, x, y, gradients)
    ix1 = lerp(sx, n0, n1)
    return lerp(sy, ix0, ix1)

# 生成随机梯度网格
def generate_gradients(width, height):
    gradients = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(random_gradient())
        gradients.append(row)
    return gradients

# 生成 3D 地形高度图
def generate_terrain(width, height, grid_size=100):
    gradients = generate_gradients(width // grid_size + 1, height // grid_size + 1)
    terrain = np.zeros((width, height))
    
    for x in range(width):
        for y in range(height):
            noise_value = perlin_noise(x, y, gradients, grid_size=grid_size)
            terrain[x][y] = (noise_value + 1) / 2  # 将噪声值归一化到 [0, 1]
    
    return terrain

# 计算法线
def calculate_normals(terrain):
    width, height = terrain.shape
    normals = np.zeros((width, height, 3))
    
    for x in range(1, width-1):
        for y in range(1, height-1):
            dzdx = (terrain[x+1, y] - terrain[x-1, y]) / 2.0
            dzdy = (terrain[x, y+1] - terrain[x, y-1]) / 2.0
            normal = np.array([-dzdx, -dzdy, 1.0])
            normal = normal / np.linalg.norm(normal)  # 归一化法线
            normals[x, y] = normal
    
    return normals

# 光照计算 (Lambert光照模型)
def calculate_lighting(normals, light_direction):
    light_direction = light_direction / np.linalg.norm(light_direction)
    lighting = np.zeros(normals.shape[:2])
    
    for x in range(normals.shape[0]):
        for y in range(normals.shape[1]):
            dot_product = np.dot(normals[x, y], light_direction)
            lighting[x, y] = max(dot_product, 0)  # 确保不为负值，避免反射光线
    
    return lighting

# 可视化 3D 地形，并加入光影效果与光源标记
def plot_3d_terrain(terrain, lighting, light_position):
    width, height = terrain.shape
    x = np.arange(0, width)
    y = np.arange(0, height)
    x, y = np.meshgrid(x, y)
    z = terrain.T  # 使用转置来匹配坐标系

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # 使用光照强度影响颜色
    ax.plot_surface(x, y, z, facecolors=plt.cm.terrain(lighting.T), rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)
    
    # 标记光源位置
    ax.scatter(light_position[0], light_position[1], light_position[2], color='yellow', s=500, label='Light Source')
    
    ax.set_title("3D Terrain with Lighting and Light Source")
    plt.show()

# 生成并显示带光影的 3D 地形
width = 100
height = 100
terrain = generate_terrain(width, height, grid_size=10)

# 计算法线和光照
normals = calculate_normals(terrain)
light_direction = np.array([1.0, 1.0, 1.0])  # 光源方向
lighting = calculate_lighting(normals, light_direction)

# 设置光源位置，调整光源高度
light_position = np.array([width // 2, height // 2, 10])  # 光源放置在地形上方的中央点

plot_3d_terrain(terrain, lighting, light_position)
