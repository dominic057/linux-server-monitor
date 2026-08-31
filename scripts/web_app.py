from flask import Flask, render_template, jsonify
import sqlite3
import os


# =========================
# Flask application
# =========================

app = Flask(
    __name__,
    template_folder="../templates"
)


# =========================
# Database configuration
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "logs",
    "incidents.db"
)


def get_connection():

    return sqlite3.connect(DB_PATH)


# =========================
# Dashboard
# =========================

@app.route("/")
def index():

    return render_template(
        "dashboard.html"
    )

@app.route("/health")
def health():

    if os.getenv("HEALTHCHECK_FAIL") == "true":
        return jsonify({
            "status": "unhealthy"
        }), 500

    return jsonify({
        "status": "healthy"
    }), 200




# =========================
# Metrics API
# =========================

@app.route("/api/metrics")
def metrics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            cpu_usage,
            memory_usage,
            disk_usage
        FROM metrics
        WHERE server_id = ?
        ORDER BY id DESC
        LIMIT 30
    """, (
        "LINUX-WSL-001",
    ))

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    data = []

    for row in rows:

        data.append({
            "timestamp": row[0],
            "cpu": row[1],
            "memory": row[2],
            "disk": row[3]
        })

    return jsonify(data)


# =========================
# Incident API
# =========================

@app.route("/api/incidents")
def incidents():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            incident_id,
            event_type,
            severity,
            status,
            detected_time,
            resolved_time
        FROM incidents
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({
            "incident_id": row[0],
            "event_type": row[1],
            "severity": row[2],
            "status": row[3],
            "detected_time": row[4],
            "resolved_time": row[5]
        })

    return jsonify(data)


# =========================
# Server API
# =========================

@app.route("/api/server")
def server():

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
        WHERE server_id = ?
    """, (
        "LINUX-WSL-001",
    ))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return jsonify({
            "error": "Server not found"
        }), 404

    data = {

        "server_id": row[0],

        "hostname": row[1],

        "ip_address": row[2],

        "environment": row[3],

        "os": row[4],

        "cpu_count": row[5],

        "memory_total_gb": row[6],

        "disk_total_gb": row[7],

        "status": row[8],

        "last_check": row[9]
    }

    return jsonify(data)


# =========================
# Dashboard Summary API
# =========================

@app.route("/api/summary")
def summary():

    conn = get_connection()
    cursor = conn.cursor()

    # 最新一次监控数据

    cursor.execute("""
        SELECT
            cpu_usage,
            memory_usage,
            disk_usage
        FROM metrics
        WHERE server_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (
        "LINUX-WSL-001",
    ))

    metric = cursor.fetchone()


    # Incident statistics

    cursor.execute("""
        SELECT COUNT(*)
        FROM incidents
    """)

    total_incidents = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'OPEN'
    """)

    open_incidents = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'RESOLVED'
    """)

    resolved_incidents = cursor.fetchone()[0]


    conn.close()


    if metric:

        cpu = metric[0]
        memory = metric[1]
        disk = metric[2]

    else:

        cpu = 0
        memory = 0
        disk = 0


    return jsonify({

        "cpu": cpu,

        "memory": memory,

        "disk": disk,

        "total_incidents":
            total_incidents,

        "open_incidents":
            open_incidents,

        "resolved_incidents":
            resolved_incidents
    })


# =========================
# Start Flask
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
