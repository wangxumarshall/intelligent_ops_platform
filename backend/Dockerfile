# 使用官方 Python 3.10 slim 版本作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装，利用 Docker 的层缓存机制
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 复制项目所有文件到工作目录
COPY . .

# 声明容器对外暴露的端口
EXPOSE 8000

# 容器启动时运行的命令
# -w 4: 启动 4 个工作进程 (根据您的服务器 CPU 核心数调整)
# -k uvicorn.workers.UvicornWorker: 使用 Uvicorn 作为工作模式
# -b 0.0.0.0:8000: 绑定到容器的所有网络接口的 8000 端口
# main:app: 您的 FastAPI 应用实例 (main.py 文件中的 app 对象)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
