# SplitPNG

一个用于分离PNG图像RGB和Alpha通道的Python工具。

## 功能

- 遍历指定文件夹中的所有PNG文件
- 分离每个PNG文件的RGB通道和Alpha通道
- 生成两个新的PNG文件：
  1. **RGB图像**：保留原始RGB颜色，移除Alpha通道，文件名保持不变
  2. **Alpha图像**：反转Alpha通道（255 - 原始Alpha值），保存为灰度RGB图像，文件名格式为`原文件名_.png`
   （不透明区域显示为黑色，透明区域显示为白色）

## 安装

### 使用pip安装

```bash
pip install -e .
```

### 依赖

- Python >= 3.12
- Pillow >= 10.0.0

## 使用方法

### 命令行

```bash
python main.py <文件夹路径>
```

示例：

```bash
# 处理当前目录下的所有PNG文件
python main.py .

# 处理指定目录
python main.py /path/to/images
```

### 输出说明

假设输入文件夹包含 `example.png`，处理后将生成：

- `example.png`（新的RGB图像，覆盖原文件）
- `example_.png`（Alpha反转图像）

**注意**：原文件将被RGB图像覆盖。如果需要保留原文件，请先备份。

## 开发

### 项目结构

```
splitpng/
├── main.py          # 主程序
├── pyproject.toml   # 项目配置和依赖
└── README.md        # 本文档
```

### 安装开发环境

```bash
# 克隆仓库
git clone <repository-url>
cd splitpng

# 创建虚拟环境（可选）
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -e .
```

## 工作原理

1. 使用Pillow库读取PNG图像
2. 将图像转换为RGBA模式（确保有Alpha通道）
3. 分离R、G、B、A四个通道
4. 合并R、G、B通道生成RGB图像
5. 反转Alpha通道（255 - 原始值）
6. 将反转后的Alpha通道复制到三个颜色通道，生成灰度RGB图像
7. 保存两个图像文件

**注意**：Alpha图像中，不透明区域显示为黑色，透明区域显示为白色（反转后的效果）。如果需要相反的显示效果，可以手动修改代码。

## 注意事项

- 如果PNG文件没有Alpha通道，程序会自动添加一个全不透明（255）的Alpha通道
- 如果Alpha通道是恒定的（所有像素值相同），生成的Alpha图像将是纯色
- 程序会输出每个文件的Alpha值范围，便于调试

## 许可证

MIT