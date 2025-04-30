# TextWeaver AI - 中文文本生成器

TextWeaver AI 是一个专为中文用户设计的文本生成应用程序，提供多种文本生成模型选择。

## 功能特点

- 支持多种中文优化的文本生成模型
- 简洁直观的用户界面
- 快速生成高质量中文文本
- 支持多种主题的文本生成

## 可用模型

应用程序提供以下文本生成模型：

1. **ChatGLM** - 专为中文优化的大型语言模型，生成流畅自然的中文文本
2. **Qwen (通义千问)** - 阿里巴巴开发的中文大模型，理解力和生成能力强
3. **Transformer (GPT-2)** - 强大的语言模型，生成连贯且富有创意的文本
4. **马尔可夫链** - 基于统计的文本生成模型，适合短文本生成

## 安装与运行

### 环境要求

- Python 3.8 或更高版本
- 足够的内存和磁盘空间（运行中文大模型需要至少 8GB RAM）
- 如果有 NVIDIA GPU，可以获得更好的性能

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/mufasa78/textgenerator.git
cd textgenerator
```

2. 创建并激活虚拟环境：

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 运行应用程序：

```bash
python app.py
```

5. 在浏览器中访问：`http://localhost:5000`

## 首次运行

首次运行时，应用程序会自动下载所需的模型文件。这可能需要一些时间，具体取决于您的网络速度。

- ChatGLM 模型约 6GB
- Qwen 模型约 7GB
- GPT-2 模型约 500MB

## 使用方法

1. 选择您想使用的文本生成模型
2. 输入关键词或短语作为提示
3. 点击"生成文本"按钮
4. 查看生成的文本结果
5. 可以使用复制按钮复制生成的文本

## 离线使用

所有模型在首次下载后可以离线使用，非常适合在中国网络环境中使用。

## 许可证

MIT 许可证
