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

    conn.commit()

    conn.close()


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

        now.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        description

    ))

    conn.commit()

    conn.close()

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

            now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            resolution,

            incident_id
        ))

    else:

        cursor.execute("""
            UPDATE incidents

            SET status = ?

            WHERE incident_id = ?

        """, (

            status,
            incident_id
        ))

    conn.commit()

    conn.close()


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


if __name__ == "__main__":

    init_database()

    print(
        "Database initialized successfully."
    )
