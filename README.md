# AI Text Generator - 中英文本生成器

AI Text Generator 是一个支持中英文的文本生成应用程序，专为中国用户设计，提供多种本地运行的文本生成模型选择。

*[English version below](#english-version)*

## 功能特点

- 支持多种中文优化的文本生成模型
- 简洁直观的用户界面
- 快速生成高质量中文文本
- 支持多种主题的文本生成
- 完全本地运行，无需依赖外部API

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

**步骤 1:** 克隆仓库

```bash
git clone https://github.com/mufasa78/urban-palm-tree.git
cd urban-palm-tree
```

**步骤 2:** 创建并激活虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

**步骤 3:** 安装依赖

```bash
pip install -r requirements.txt
```

**步骤 4:** 运行应用程序

```bash
python app.py
```

**步骤 5:** 在浏览器中访问：`http://127.0.0.1:5000`

## 首次运行

首次运行时，应用程序会自动下载所需的模型文件。这可能需要一些时间，具体取决于您的网络速度。

- ChatGLM 模型约 6GB
- Qwen 模型约 7GB
- GPT-2 模型约 500MB

## 使用方法

**步骤 1:** 选择您想使用的文本生成模型（推荐使用ChatGLM获得最佳中文效果）

**步骤 2:** 输入关键词或短语作为提示

**步骤 3:** 点击"生成文本"按钮

**步骤 4:** 查看生成的文本结果

**步骤 5:** 可以使用复制按钮复制生成的文本

## 离线使用

所有模型在首次下载后可以离线使用，非常适合在中国网络环境中使用，无需VPN或访问受限的国外服务。

## 技术说明

- 使用Flask框架构建Web应用
- 支持中文语言界面
- 集成了多种开源的中文大语言模型
- 针对中文文本生成进行了特别优化

## 许可证

MIT 许可证

---

## English Version {#english-version}

AI Text Generator is a text generation application supporting both English and Chinese, specifically designed for users in China, offering a variety of locally-run text generation models.

## Features

- Multiple Chinese-optimized text generation models
- Clean and intuitive user interface
- Fast generation of high-quality Chinese text
- Support for various text generation themes
- Completely local operation, no external API dependencies

## Available Models

The application provides the following text generation models:

1. **ChatGLM** - A large language model optimized for Chinese, generating fluent and natural Chinese text
2. **Qwen** - A Chinese large model developed by Alibaba, with strong comprehension and generation capabilities
3. **Transformer (GPT-2)** - A powerful language model that generates coherent and creative text
4. **Markov Chain** - A statistics-based text generation model, suitable for short text generation

## Installation and Running

### Requirements

- Python 3.8 or higher
- Sufficient memory and disk space (running Chinese large models requires at least 8GB RAM)
- An NVIDIA GPU will provide better performance

### Installation Steps

**Step 1:** Clone the repository

```bash
git clone https://github.com/mufasa78/urban-palm-tree.git
cd urban-palm-tree
```

**Step 2:** Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

**Step 3:** Install dependencies

```bash
pip install -r requirements.txt
```

**Step 4:** Run the application

```bash
python app.py
```

**Step 5:** Access in browser: `http://127.0.0.1:5000`

## First Run

When running for the first time, the application will automatically download the required model files. This may take some time, depending on your network speed.

- ChatGLM model: approximately 6GB
- Qwen model: approximately 7GB
- GPT-2 model: approximately 500MB

## Usage Instructions

**Step 1:** Select the text generation model you want to use (ChatGLM is recommended for best Chinese results)

**Step 2:** Enter keywords or phrases as prompts

**Step 3:** Click the "Generate Text" button

**Step 4:** View the generated text results

**Step 5:** Use the copy button to copy the generated text

## Offline Use

All models can be used offline after the initial download, making them ideal for use in China's network environment, without requiring VPN or access to restricted foreign services.

## Technical Notes

- Built with Flask framework
- Supports Chinese language interface
- Integrates multiple open-source Chinese large language models
- Specially optimized for Chinese text generation

## License

MIT License
