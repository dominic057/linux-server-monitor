linux-server-monitor
一个基于 Python + psutil + Flask + SQLite 开发的轻量级 Linux 服务器监控系统。可以实时采集服务器的 CPU、内存、磁盘、网络 等核心运行指标，并根据阈值自动判断服务器健康状态。当服务器资源使用率异常时，系统会产生相应的 Incident（事件），并通过 Web Dashboard 实时展示服务器状态和近期告警记录。
本项目主要用于学习 Linux 服务器监控、系统资源采集、异常告警、Incident 管理、REST API 和 Web Dashboard 的基本实现方式。

💻 环境要求
Linux、Python 3.10+、Git
本项目开发和测试环境：
Windows
└── WSL2
    └── Ubuntu 24.04 LTS

🚀 快速开始
1. 克隆项目
git clone https://github.com/dominic057/linux-server-monitor.git
进入项目目录：cd linux-server-monitor

2.创建 Python 虚拟环境
python3 -m venv .venv
激活虚拟环境：source .venv/bin/activate

3. 安装依赖
pip install psutil flask
检查Flask：python -c "import flask; print(flask.__version__)"
检查 psutil：python -c "import psutil; print(psutil.__version__)"

4.初始化 / 注册服务器
python scripts/register_server.py

5. 启动监控程序
打开一个终端窗口
cd ~/linux-server-monitor
source .venv/bin/activate
python scripts/monitor.py 不要关闭监控程序

6.启动 Web Dashboard
重新打开一个终端窗口
cd ~/linux-server-monitor
source .venv/bin/activate
python scripts/web_app.py
然后打开浏览器:http://127.0.0.1:5000

🧪 CPU 压力测试
为了验证监控程序是否真的能够发现 CPU 异常，可以使用项目提供的测试脚本
python scripts/cpu_test.py

🔄 完整测试流程
① 启动 monitor.py
        ↓
② 启动 web_app.py
        ↓
③ 浏览器打开 Dashboard
        ↓
④ 运行 cpu_test.py
        ↓
⑤ CPU 使用率升高
        ↓
⑥ monitor.py 检测异常
        ↓
⑦ Server Status → WARNING / CRITICAL
        ↓
⑧ 创建 Incident
        ↓
⑨ Dashboard 更新
        ↓
⑩ CPU 压力结束
        ↓
⑪ Server Status → NORMAL
        ↓
⑫ Incident → RESOLVED



📌 项目特点
本项目实现了一套简单但完整的服务器监控流程：
Linux Server
     │
     │ psutil
     ▼
资源指标采集
     │
     ├── CPU
     ├── Memory
     ├── Disk
     └── Network
     │
     ▼
阈值判断
     │
     ├── NORMAL
     ├── WARNING
     └── CRITICAL
     │
     ▼
Incident 事件记录
     │
     ▼
SQLite 数据库
     │
     ▼
Flask Web API
     │
     ▼
Web Dashboard

✨ 功能
1. CPU 监控
实时获取服务器 CPU 使用率

2. 内存监控
监控服务器当前内存使用率

3. 磁盘监控
监控服务器磁盘空间使用情况

4. 网络流量监控
采集服务器网络发送和接收的数据量

5. 服务器健康状态
系统根据资源使用情况，将服务器状态划分为：NORMAL、WARNING、CRITICAL

6. Incident 管理
当服务器出现异常时，系统会创建 Incident。
Incident 可以理解为：一次需要被记录、处理和跟踪的服务器异常事件
形成一个：
异常发现
   ↓
Incident 创建
   ↓
问题处理
   ↓
服务器恢复
   ↓
Incident RESOLVED

7. Web Dashboard
项目使用 Flask 提供 Web 服务，并通过 Dashboard 展示服务器状态。
Dashboard 可以查看：Server ID、Server Status、CPU Usage、Memory Usage、Disk Usage、Network Traffic、Last Update、Recent Incidents
后台监控程序检测到服务器资源异常时，Dashboard 会同步更新

8.SQLite 数据库
项目使用 SQLite 保存服务器和 Incident 等数据
数据库文件:logs/incidents.db
用于保存：Server information、Server status、Incident information、Incident severity、Incident status、Incident timestamps

9. REST API
Flask 提供 API 接口，使 Dashboard 和后台数据之间可以通过 HTTP 通信

🛠️ 技术栈
Python       核心开发语言
psutil       获取 Linux 系统资源信息
Flask        Web Server / REST API
SQLite       数据持久化
HTML         Dashboard 页面
JavaScript   前端动态数据更新
Git          版本管理
GitHub       项目托管
Linux / WSL2 项目运行环境

📁 项目结构
linux-server-monitor/
│
├── scripts/
│   ├── database.py
│   ├── monitor.py
│   ├── server_info.py
│   ├── web_app.py
│   ├── metrics_summary.py
│   ├── query_metrics.py
│   ├── register_server.py
│   └── ...
│
├── templates/
│   └── dashboard.html
│
├── logs/
│   └── ...
│
├── .gitignore
│
└── README.md

scripts/monitor.py 核心监控程序
负责：CPU、Memory、Disk、Network等系统指标采集，并根据阈值判断服务器状态

scripts/server_info.py 获取服务器基础信息
获取服务器基础信息，例如：Server ID、Hostname、Operating System、CPU Count、Memory、Disk、Environment

scripts/database.py 负责 SQLite 数据库相关操作
包括：数据库连接、数据表操作、Server 信息保存、Incident 保存、Incident 状态更新

scripts/web_app.py Flask Web 应用
主要负责：Web Dashboard、REST API、Server information、Incident information等功能

templates/dashboard.html Web Dashboard 前端页面
负责展示：Server Status、CPU、Memory、Disk、Network、Recent Incidents等监控信息

