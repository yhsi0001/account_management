# 使用官方的Python基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将requirements.txt文件复制到工作目录
COPY requirements.txt .

# 更新包管理器并安装依赖项
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        default-libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件复制到工作目录
COPY . .

# 设置环境变量
ENV FLASK_APP=account_management.py

# 暴露容器的端口
EXPOSE 5000

# 运行Flask应用
CMD ["flask", "run", "--host=0.0.0.0"]
