import sqlite3
from datetime import datetime


DB_PATH = "logs/incidents.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # Incident表
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            incident_id TEXT UNIQUE NOT NULL,

            server_name TEXT NOT NULL,

            event_type TEXT NOT NULL,

            severity TEXT NOT NULL,

            status TEXT NOT NULL,

            detected_time TEXT NOT NULL,

            resolved_time TEXT,

            description TEXT,

            resolution TEXT
        )
    """)

    # =========================
    # Server资产表
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            server_id TEXT UNIQUE NOT NULL,

            hostname TEXT NOT NULL,

            ip_address TEXT,

            environment TEXT,

            os TEXT,

            os_version TEXT,

            kernel TEXT,

            cpu_count INTEGER,

            memory_total_gb REAL,

            disk_total_gb REAL,

            status TEXT DEFAULT 'UNKNOWN',

            last_check TEXT
        )
    """)

    # =========================
    # Metrics监控数据表
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            server_id TEXT NOT NULL,

            cpu_usage REAL,

            memory_usage REAL,

            disk_usage REAL,

            network_sent_mb REAL,

            network_recv_mb REAL,

            timestamp TEXT NOT NULL

        )
    """)

    # =========================
    # Incident历史记录表
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incident_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            incident_id TEXT NOT NULL,

            status TEXT NOT NULL,

            operator TEXT NOT NULL,

            action TEXT NOT NULL,

            timestamp TEXT NOT NULL,

            comment TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# Incident管理
# ============================================================


def create_incident(
    server_name,
    event_type,
    severity,
    description
):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()

    incident_id = (
        "INC-" +
        now.strftime(
            "%Y%m%d-%H%M%S"
        )
    )

    timestamp = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # 创建Incident
    cursor.execute("""
        INSERT INTO incidents (

            incident_id,
            server_name,
            event_type,
            severity,
            status,
            detected_time,
            description

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        incident_id,
        server_name,
        event_type,
        severity,
        "OPEN",
        timestamp,
        description

    ))

    # 记录Incident历史
    cursor.execute("""
        INSERT INTO incident_history (

            incident_id,
            status,
            operator,
            action,
            timestamp,
            comment

        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        incident_id,
        "OPEN",
        "SYSTEM",
        "INCIDENT_CREATED",
        timestamp,
        "Incident automatically created by monitoring system."

    ))

    conn.commit()
    conn.close()

    add_incident_history(
    incident_id=incident_id,
    status="OPEN",
    operator="SYSTEM",
    action="CREATE_INCIDENT",
    comment=description
    )

    return incident_id

def update_incident_status(
    incident_id,
    status,
    resolution=None
):

    conn = get_connection()

    cursor = conn.cursor()

    if status == "RESOLVED":

        now = datetime.now()

        cursor.execute("""
            UPDATE incidents

            SET
                status = ?,
                resolved_time = ?,
                resolution = ?

            WHERE incident_id = ?

        """, (
            status,
            now.strftime("%Y-%m-%d %H:%M:%S"),
            resolution,
            incident_id
        ))

        action = "RESOLVE_INCIDENT"

    else:

        cursor.execute("""
            UPDATE incidents

            SET status = ?

            WHERE incident_id = ?

        """, (
            status,
            incident_id
        ))

        action = "UPDATE_STATUS"

    conn.commit()

    conn.close()

    add_incident_history(
        incident_id=incident_id,
        status=status,
        operator="SYSTEM",
        action=action,
        comment=resolution
    )

def add_incident_history(
    incident_id,
    status,
    operator,
    action,
    comment=None
):

    conn = get_connection()

    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        INSERT INTO incident_history (
            incident_id,
            status,
            operator,
            action,
            timestamp,
            comment
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        incident_id,
        status,
        operator,
        action,
        now.strftime("%Y-%m-%d %H:%M:%S"),
        comment
    ))

    conn.commit()

    conn.close()


# ============================================================
# Server资产管理
# ============================================================


def register_server(info):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        INSERT INTO servers (

            server_id,
            hostname,
            ip_address,
            environment,
            os,
            os_version,
            kernel,
            cpu_count,
            memory_total_gb,
            disk_total_gb,
            status,
            last_check

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(server_id)

        DO UPDATE SET

            hostname = excluded.hostname,

            ip_address = excluded.ip_address,

            environment = excluded.environment,

            os = excluded.os,

            os_version = excluded.os_version,

            kernel = excluded.kernel,

            cpu_count = excluded.cpu_count,

            memory_total_gb =
                excluded.memory_total_gb,

            disk_total_gb =
                excluded.disk_total_gb,

            last_check =
                excluded.last_check

    """, (

        info["server_id"],
        info["hostname"],
        info["ip_address"],
        info["environment"],
        info["os"],
        info["os_version"],
        info["kernel"],
        info["cpu_count"],
        info["memory_total_gb"],
        info["disk_total_gb"],
        "NORMAL",
        now.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    ))

    conn.commit()
    conn.close()

def get_server(server_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            server_id,
            hostname,
            ip_address,
            environment,
            os,
            os_version,
            kernel,
            cpu_count,
            memory_total_gb,
            disk_total_gb,
            status,
            last_check

        FROM servers

        WHERE server_id = ?

    """, (server_id,))


    server = cursor.fetchone()


    conn.close()


    return server



def update_server_status(
    server_id,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        UPDATE servers

        SET
            status = ?,
            last_check = ?

        WHERE server_id = ?

    """, (

        status,

        now.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        server_id

    ))

    conn.commit()
    conn.close()


def save_metric(
    server_id,
    cpu_usage,
    memory_usage,
    disk_usage,
    network_sent_mb,
    network_recv_mb
):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        INSERT INTO metrics (
            server_id,
            cpu_usage,
            memory_usage,
            disk_usage,
            network_sent_mb,
            network_recv_mb,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        server_id,
        cpu_usage,
        memory_usage,
        disk_usage,
        network_sent_mb,
        network_recv_mb,
        now.strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def insert_metric(
    server_id,
    cpu,
    memory,
    disk,
    sent,
    recv
):

    conn = get_connection()

    cursor = conn.cursor()

    now = datetime.now()


    cursor.execute("""
        INSERT INTO metrics (

            server_id,
            cpu_usage,
            memory_usage,
            disk_usage,
            network_sent_mb,
            network_recv_mb,
            timestamp

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        server_id,
        cpu,
        memory,
        disk,
        sent,
        recv,

        now.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    ))


    conn.commit()

    conn.close()


def list_servers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            server_id,
            hostname,
            ip_address,
            environment,
            os,
            cpu_count,
            memory_total_gb,
            disk_total_gb,
            status,
            last_check

        FROM servers

        ORDER BY server_id
    """)

    servers = cursor.fetchall()

    conn.close()

    return servers


# ============================================================
# Incident查询
# ============================================================


def list_incidents():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            incident_id,
            server_name,
            event_type,
            severity,
            status,
            detected_time,
            resolved_time

        FROM incidents

        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()

    conn.close()

    return incidents


def get_incident_history(incident_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            status,
            operator,
            action,
            timestamp,
            comment

        FROM incident_history

        WHERE incident_id = ?

        ORDER BY id ASC
    """, (incident_id,))

    history = cursor.fetchall()

    conn.close()

    return history


def get_metric_summary(server_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            AVG(cpu_usage),
            MAX(cpu_usage),
            MIN(cpu_usage),
            AVG(memory_usage),
            MAX(memory_usage),
            AVG(disk_usage),
            MAX(disk_usage)
        FROM metrics
        WHERE server_id = ?
    """, (
        server_id,
    ))

    summary = cursor.fetchone()

    conn.close()

    return summary

def get_incident_summary(server_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN status = 'RESOLVED'
                    THEN 1
                    ELSE 0
                END
            ),
            SUM(
                CASE
                    WHEN status != 'RESOLVED'
                    THEN 1
                    ELSE 0
                END
            )
        FROM incidents
        WHERE server_name = ?
    """, (
        server_id,
    ))

    summary = cursor.fetchone()

    conn.close()

    return summary


if __name__ == "__main__":

    init_database()

    print(
        "Database initialized successfully."
    )
