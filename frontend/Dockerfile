FROM node:18-slim

WORKDIR /app

# 配置npm镜像源
RUN npm config set registry http://mirrors.cloud.tencent.com/npm/ \
    && npm config set strict-ssl false

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5173

# 启动命令
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"] 