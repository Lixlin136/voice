# 语音聊天智能助手

基于大语言模型的拟人化语音交互系统，提供个性化聊天体验。

## 功能特点

- 拟人化语音交互
- 个性化人设设置
- 支持文本和语音输入
- 实时语音合成回复
- 用户信息管理

## 技术栈

- 前端: HTML5, CSS3, JavaScript, Bootstrap
- 后端: Django
- 语音识别: Web Speech API
- 语音合成: 第三方API(通义千问)


## 安装指南

1. 克隆仓库
```bash
git clone https://github.com/lxl136/Voiceai.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 数据库迁移
1. 先在setting文件中配置数据库信息
```bash
python manage.py migrate
```

4. 运行开发服务器
```bash
python manage.py runserver
```

## 使用说明
 可选 阿里云百炼大模型 注册账号 获取api key 链接 https://bailian.console.aliyun.com/?spm=5176.29597918.0.0.191e7ca0zy49N4&tab=model#/efm/model_experience_center/text
1. 访问 `http://localhost:8000/` 进入聊天界面
2. 点击麦克风图标进行语音输入
3. 或直接在输入框中输入文本
4. 在设置中可以修改个人资料和人设风格


## 许可证

MIT License