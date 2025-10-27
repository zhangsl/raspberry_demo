# Raspberry Pi Demo Projects

这是一个基于树莓派的多种传感器演示项目集合，包含人体检测、光线检测、邮件报警、碰撞检测和综合传感器检测等功能。

**注意：当前代码基于 Raspberry Pi 3 Model B 开发和测试**

## 项目结构

```
raspberry-pi-demo/
├── setup.py
├── README.md
├── README_en.md         # 英文版README
├── requirements.txt     # 项目依赖列表
├── venv/               # Python虚拟环境
├── __init__.py
├── sensor_detection.log     # 传感器检测日志文件
├── src/
│   ├── __init__.py
│   ├── body_detect.py       # 人体检测模块，使用红外传感器检测人体活动并通过邮件报警
│   ├── smartlite.py         # 光线检测模块，检测环境光线变化
│   ├── email_alarm.py       # 邮件报警模块，独立的邮件发送功能
│   ├── collision_detection.py   # 碰撞检测模块，使用红外避障传感器检测障碍物
│   └── sensor_integration.py    # 综合传感器检测模块，同时检测人体和碰撞
├── tests/
└── docs/
    └── collision_detection_design.md  # 碰撞检测设计方案
```

## 功能说明

### 人体检测 (src/body_detect.py)
- 使用 GPIO 18 连接人体红外传感器
- 检测到人体活动时发送邮件报警
- 邮件通过 SMTP 协议发送

### 光线检测 (src/smartlite.py)
- 使用 GPIO 3 检测环境光线变化
- 当检测到光线变化时输出时间戳和提示信息

### 邮件报警 (src/email_alarm.py)
- 独立的邮件发送模块
- 可以被其他模块调用发送报警邮件

### 碰撞检测 (src/collision_detection.py)
- 使用红外避障传感器检测前方障碍物
- 可调节检测距离2-30cm
- 实时检测并输出结果

### 综合传感器检测 (src/sensor_integration.py)
- 同时检测人体传感器(GPIO18)和碰撞传感器(GPIO4)
- 检测到人体时蜂鸣器持续响（GPIO17），检测到障碍物时LED灯亮（GPIO23）
- 实时轮询检测并记录日志
- 支持文件和控制台双重日志输出

## 硬件连接

- 人体红外传感器连接到 GPIO 18
- 光线传感器连接到 GPIO 3
- 红外避障传感器连接到 GPIO 4
- 蜂鸣器连接到 GPIO 17
- LED连接到 GPIO 23

## 安装

1. 克隆项目：
   ```bash
   git clone https://github.com/zhangsl/raspberry_demo.git
   cd raspberry-pi-demo
   ```

2. 创建虚拟环境（可选但推荐）：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # 或在Windows上使用 venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 设置环境变量：
   ```bash
   export MAIL_HOST=smtp.yeah.net
   export MAIL_USER=your_username
   export MAIL_PASS=your_password
   export SENDER=your_email@yeah.net
   export RECEIVERS=recipient1@domain.com,recipient2@domain.com
   ```

2. 运行程序：
   ```bash
   python src/body_detect.py
   python src/smartlite.py
   python src/email_alarm.py
   python src/collision_detection.py
   python src/sensor_integration.py
   ```

## 注意事项

1. 需要树莓派硬件环境才能运行（基于 Raspberry Pi 3 Model B 开发和测试）
2. 需要正确连接传感器硬件
3. 邮件报警功能需要配置正确的邮箱信息
