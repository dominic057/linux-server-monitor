from database import (
    init_database,
    create_incident,
    update_incident_status,
    list_incidents
)


def main():

    # 初始化数据库
    init_database()

    # 创建事件
    incident_id = create_incident(
        server_name="linux-wsl-01",
        event_type="HIGH_CPU",
        severity="WARNING",
        description="CPU usage exceeded 80%."
    )

    print(f"Created incident: {incident_id}")

    # 模拟工作人员开始调查
    update_incident_status(
        incident_id,
        "INVESTIGATING"
    )

    print("Incident status: INVESTIGATING")

    # 模拟开始处理
    update_incident_status(
        incident_id,
        "PROCESSING"
    )

    print("Incident status: PROCESSING")

    # 模拟问题解决
    update_incident_status(
        incident_id,
        "RESOLVED",
        resolution="Terminated abnormal high-CPU process."
    )

    print("Incident status: RESOLVED")

    # 查询事件
    print("\nIncident Records:")

    incidents = list_incidents()

    for incident in incidents:
        print(incident)


if __name__ == "__main__":
    main()
