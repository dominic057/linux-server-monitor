linux-server-monitor  
一个基于 Python + psutil + Flask + SQLite 开发的轻量级 Linux 服务器监控系统。可以实时采集服务器的 CPU、内存、磁盘、网络 等核心运行指标，并根据阈值自动判断服务器健康状态。当服务器资源使用率异常时，系统会产生相应的 Incident（事件），并通过 Web Dashboard 实时展示服务器状态和近期告警记录，并通过 Docker Compose 完成容器化部署
  
💻 环境要求  
Linux、Python 3.10+、Git  
本项目开发和测试环境：WSL2、Ubuntu 24.04 LTS

🐳Docker 部署说明  
1. 环境要求  
Docker  
Docker Compose  
docker --version  
docker compose version  
2. 构建并启动服务  
cd ~/linux-server-monitor  
使用 Docker Compose 构建镜像并启动服务：docker compose up -d --build  
项目包含以下三个服务：  
init	初始化数据库并注册服务器资产信息
monitor	持续采集 CPU、内存、磁盘、网络指标并进行异常检测
web	提供 Flask Web Dashboard 和 REST API  

查看服务运行状态：  
docker compose ps  
正常情况下：  
NAME                 SERVICE   STATUS  
linux-monitor-init   init      Exited (0)  
linux-monitor        monitor   Up  
linux-monitor-web   web       Up (healthy)  
其中 init 是一次性初始化服务，执行完成后正常退出；monitor 和 web 会持续运行。  

3. 访问 Web Dashboard  
Web 服务默认监听 5000 端口。  
浏览器访问：http://127.0.0.1:5000  
REST API：curl http://127.0.0.1:5000/api/summary

4. 查看容器日志  
查看监控服务日志：docker compose logs -f monitor  
查看 Web 服务日志：docker compose logs -f web  
查看最近 30 条监控日志：docker compose logs --tail=30 monitor  

5. 查看容器健康状态  
Web 服务配置了 Docker Health Check：docker inspect -f '{{.State.Health.Status}}' linux-monitor-web  
正常情况下返回：healthy  
也可以查看详细健康检查结果：docker inspect -f '{{json .State.Health}}' linux-monitor-web  
Health Check 会定期访问：http://127.0.0.1:5000/health  用于判断 Web 服务是否正常运行。

6. 数据持久化  
项目使用 Docker Volume 保存 SQLite 数据：monitor-data  
查看 Volume：docker volume ls  
容器中的数据目录：/app/logs  
其中包含：/app/logs/incidents.db  
/app/logs/monitor.log  
monitor-data 同时挂载到 monitor 和 web 服务，使监控服务产生的数据能够被 Web Dashboard 读取。  
查看容器中的数据库：docker compose exec monitor ls -lh /app/logs  
检查监控数据：docker compose exec monitor python -c "import sqlite3; conn=sqlite3.connect('/app/logs/incidents.db'); print('metrics:', conn.execute('SELECT COUNT(*) FROM metrics').fetchone()[0]); conn.close()"  

7. 停止服务
停止并删除容器及 Compose 网络：docker compose down  
Docker Volume 默认不会被删除，因此监控数据仍然保留。  
再次启动：docker compose up -d  即可继续使用原有监控数据。

8. 重建镜像  
修改 Python 代码、Dockerfile 或依赖后，可以重新构建：docker compose up -d --build  
查看镜像：docker images  
查看容器：docker ps  

 

🚀 快速开始  
1. 克隆项目  
git clone https://github.com/dominic057/linux-server-monitor.git  
进入项目目录：cd ~/linux-server-monitor  
  
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
② 启动 web_app.py  
③ 浏览器打开 Dashboard  
④ 运行 cpu_test.py  
⑤ CPU 使用率升高  
⑥ monitor.py 检测异常  
⑦ Server Status → WARNING / CRITICAL  
⑧ 创建 Incident  
⑨ Dashboard 更新  
⑩ CPU 压力结束  
⑪ Server Status → NORMAL  
⑫ Incident → RESOLVED  

<img width="2559" height="1347" alt="4ad2dca9c98786a5ad2c5d61fc2692f0" src="https://github.com/user-attachments/assets/8b05fb33-5acd-47ae-ae22-429dfca30efc" />
<img width="2559" height="1347" alt="d5f5af918024b47897f60147a3a2ab99" src="https://github.com/user-attachments/assets/774e8134-879b-4c1f-9c7d-0d4055e3ba0a" />
<img width="2559" height="1347" alt="701cc36e9d69aa37e1fbbb62d791134a" src="https://github.com/user-attachments/assets/59710a94-499a-4229-93d6-7fbbc8a9e7e9" />  
开始压力测试  
<img width="2559" height="1347" alt="48cc0ed3db29340b243040c42b303c88" src="https://github.com/user-attachments/assets/cb8842cd-78c8-4e44-a288-bb042e8046f2" />
<img width="2559" height="1347" alt="c8b9bd3b28c0e300c769f2f908813b2d" src="https://github.com/user-attachments/assets/db9a32db-bd72-4b78-baf9-6238e1dd91a2" />  
停止压力测试  
<img width="2559" height="1347" alt="d6a94d0d9e29a60a2c7a2437d7da37d9" src="https://github.com/user-attachments/assets/6e281c0e-e0b6-4c45-97e6-1202708abaac" />
<img width="2559" height="1347" alt="2e469602f4cf67256279b90051f54c6c" src="https://github.com/user-attachments/assets/641cebf8-4136-4685-8cf9-9465d0fe85d3" />
  
📌 项目特点  
本项目实现了一套简单但完整的服务器监控流程：  
Linux Server->资源指标采集->阈值判断->Incident 事件记录->SQLite 数据库->Flask Web API->Web Dashboard  
  
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
当服务器出现异常时，系统会创建 Incident  
Incident 可以理解为：一次需要被记录、处理和跟踪的服务器异常事件  
形成一个：异常发现->Incident 创建->问题处理->服务器恢复->Incident RESOLVED闭环  
  
7. Web Dashboard  
项目使用 Flask 提供 Web 服务，并通过 Dashboard 展示服务器状态  
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

