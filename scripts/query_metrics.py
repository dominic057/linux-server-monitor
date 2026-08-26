from database import get_connection


SERVER_ID = "LINUX-WSL-001"


def get_latest_metrics(
    server_id,
    limit=10
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            cpu_usage,
            memory_usage,
            disk_usage,
            network_sent_mb,
            network_recv_mb
        FROM metrics
        WHERE server_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (
        server_id,
        limit
    ))

    metrics = cursor.fetchall()

    conn.close()

    return metrics


def print_metrics(metrics):

    print()
    print("=" * 80)
    print("              Linux Server Metrics")
    print("=" * 80)

    print(
        f"{'Time':20}"
        f"{'CPU':>10}"
        f"{'Memory':>10}"
        f"{'Disk':>10}"
        f"{'Net Sent':>12}"
        f"{'Net Recv':>12}"
    )

    print("-" * 80)

    for metric in reversed(metrics):

        timestamp = metric[0]
        cpu = metric[1]
        memory = metric[2]
        disk = metric[3]
        sent = metric[4]
        recv = metric[5]

        print(
            f"{timestamp:20}"
            f"{cpu:>9.1f}%"
            f"{memory:>9.1f}%"
            f"{disk:>9.1f}%"
            f"{sent:>11.2f}MB"
            f"{recv:>11.2f}MB"
        )

    print("=" * 80)


if __name__ == "__main__":

    metrics = get_latest_metrics(
        SERVER_ID,
        10
    )

    print_metrics(metrics)
