## 安装

1. 激活虚拟环境
2. 创建 .env 文件，并添加以下内容：
   ```
   BASE_URL=your_base_url
   API_KEY=your_api_key

   ```
2. 安装依赖（如果需要）：
   ```
   pip install "fastapi[standard]" python-dotenv
   ```

## 启动

在虚拟环境中运行以下命令：
```
fastapi run main.py --port 3000
```
或如果需要开发模式：
```
fastapi dev main.py --port 3000
```
