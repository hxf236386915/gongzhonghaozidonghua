FROM python:3.9-slim

WORKDIR /app

# 配置pip镜像源
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple \
    && pip config set install.trusted-host mirrors.cloud.tencent.com

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 