import psutil
import time
import logging
import sys
import os
from datetime import datetime


# =========================
# 添加 scripts 目录到 Python 路径
# =========================

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from database import (
    init_database,
    create_incident,
    update_incident_status,
    update_server_status
)


# =========================
# 监控阈值
# =========================

CPU_WARNING_THRESHOLD = 80
CPU_CRITICAL_THRESHOLD = 90


MEMORY_WARNING_THRESHOLD = 80
MEMORY_CRITICAL_THRESHOLD = 90

DISK_WARNING_THRESHOLD = 80
DISK_CRITICAL_THRESHOLD = 90


# =========================
# 服务器名称
# =========================

SERVER_ID = "LINUX-WSL-001"


# =========================
# 日志配置
# =========================

logging.basicConfig(
    filename="logs/monitor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def get_system_info():
    """获取服务器运行指标"""

    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    network = psutil.net_io_counters()

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
        "bytes_sent": network.bytes_sent,
        "bytes_recv": network.bytes_recv,
    }

def check_alerts(info):
    """检查系统指标是否超过告警阈值"""

    alerts = []

    # =========================
    # CPU 告警
    # =========================

    if info["cpu"] >= CPU_CRITICAL_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_CPU",
            "severity": "CRITICAL",
            "message": (
                f"CPU usage is critically high: "
                f"{info['cpu']:.1f}%"
            )
        })

    elif info["cpu"] >= CPU_WARNING_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_CPU",
            "severity": "WARNING",
            "message": (
                f"CPU usage is high: "
                f"{info['cpu']:.1f}%"
            )
        })

    # =========================
    # Memory 告警
    # =========================

    if info["memory"] >= MEMORY_CRITICAL_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_MEMORY",
            "severity": "CRITICAL",
            "message": (
                f"Memory usage is critically high: "
                f"{info['memory']:.1f}%"
            )
        })

    elif info["memory"] >= MEMORY_WARNING_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_MEMORY",
            "severity": "WARNING",
            "message": (
                f"Memory usage is high: "
                f"{info['memory']:.1f}%"
            )
        })

    # =========================
    # Disk 告警
    # =========================

    if info["disk"] >= DISK_CRITICAL_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_DISK",
            "severity": "CRITICAL",
            "message": (
                f"Disk usage is critically high: "
                f"{info['disk']:.1f}%"
            )
        })

    elif info["disk"] >= DISK_WARNING_THRESHOLD:

        alerts.append({
            "event_type": "HIGH_DISK",
            "severity": "WARNING",
            "message": (
                f"Disk usage is high: "
                f"{info['disk']:.1f}%"
            )
        })

    return alerts


def print_system_info(info, alerts):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("=" * 50)
    print("           Linux Server Monitor")
    print("=" * 50)

    print(f"Time:           {current_time}")
    print()

    print(
        f"CPU Usage:      "
        f"{info['cpu']:.1f}%"
    )

    print(
        f"Memory Usage:   "
        f"{info['memory']:.1f}%"
    )

    print(
        f"Disk Usage:     "
        f"{info['disk']:.1f}%"
    )

    sent_mb = (
        info["bytes_sent"] /
        1024 /
        1024
    )

    recv_mb = (
        info["bytes_recv"] /
        1024 /
        1024
    )

    print(
        f"Network Sent:   "
        f"{sent_mb:.2f} MB"
    )

    print(
        f"Network Recv:   "
        f"{recv_mb:.2f} MB"
    )

    print()

    if alerts:

        # 根据最高级别告警确定显示状态
        if any(
            alert["severity"] == "CRITICAL"
            for alert in alerts
        ):
            status = "CRITICAL"
        else:
            status = "WARNING"

        print(f"Status: {status}")

        for alert in alerts:

            print(
                f"[{alert['severity']}] "
                f"{alert['message']}"
            )

    else:

        print("Status: NORMAL")

    print("=" * 50)


def main():

    print(
        "Starting Linux Server "
        "Monitoring System..."
    )

    # 初始化数据库
    init_database()

    previous_status = "NORMAL"
    current_incident_id = None

    while True:

        try:

            info = get_system_info()

            alerts = check_alerts(info)

            print_system_info(
                info,
                alerts
            )

            # =========================
            # 异常状态
            # =========================

            if alerts:

               # 根据最高级别告警确定服务器状态
                if any(
                    alert["severity"] == "CRITICAL"
                    for alert in alerts
                ):
                    current_status = "CRITICAL"
                else:
                    current_status = "WARNING"

                update_server_status(
                    SERVER_ID,
                    current_status
                )

                # 第一次发现异常
                if previous_status == "NORMAL":

                    alert = alerts[0]

                    description = (
                        f"{alert['message']}. "
                        f"CPU={info['cpu']:.1f}%, "
                        f"Memory={info['memory']:.1f}%, "
                        f"Disk={info['disk']:.1f}%"
                    )

                    # 自动创建工单
                    current_incident_id = create_incident(
                        server_name=SERVER_ID,
                        event_type=alert["event_type"],
                        severity=alert["severity"],
                        description=description
                    )

                    print()

                    print(
                        "[INCIDENT CREATED]"
                    )

                    print(
                        f"Incident ID: "
                        f"{current_incident_id}"
                    )

                    logging.warning(
                        f"ALERT TRIGGERED - "
                        f"{description}"
                    )

                    logging.warning(
                        f"Incident created: "
                        f"{current_incident_id}"
                    )

                previous_status = current_status

            # =========================
            # 正常状态
            # =========================

            else:

                current_status = "NORMAL"

                update_server_status(
                    SERVER_ID,
                    "NORMAL"
                )

                # 从异常恢复
                if previous_status != "NORMAL":

                    print()

                    print(
                        "[RECOVERY] "
                        "Server status returned "
                        "to normal."
                    )

                    # 自动关闭工单
                    if current_incident_id:

                        update_incident_status(
                            current_incident_id,
                            "RESOLVED",
                            "Server resource "
                            "usage returned "
                            "to normal."
                        )

                        print(
                            "[INCIDENT RESOLVED]"
                        )

                        print(
                            f"Incident ID: "
                            f"{current_incident_id}"
                        )

                        logging.info(
                            f"ALERT RECOVERED - "
                            f"Incident "
                            f"{current_incident_id} "
                            f"resolved."
                        )

                        current_incident_id = None

                previous_status = current_status

            time.sleep(5)

        except KeyboardInterrupt:

            print(
                "\nMonitor stopped."
            )

            break

        except Exception as e:

            logging.error(
                f"Monitor error: {e}"
            )

            print(
                f"[ERROR] {e}"
            )

            time.sleep(5)


if __name__ == "__main__":

    main()
