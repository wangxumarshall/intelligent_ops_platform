# --- 构建阶段 ---
FROM node:18-alpine AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# 运行构建命令，生成静态文件
RUN npm run build

# --- 生产阶段 ---
FROM nginx:stable-alpine

# 将构建阶段生成的静态文件复制到 Nginx 的 Web 服务器目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 清理掉 Nginx 默认的配置
RUN rm /etc/nginx/conf.d/default.conf

# 将我们自定义的 Nginx 配置复制到容器中 (下一步会创建这个文件)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
