import platform
import socket
import psutil


SERVER_ID = "LINUX-WSL-001"


def get_server_info():

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "server_id": SERVER_ID,

        "hostname": socket.gethostname(),

        "ip_address": get_ip_address(),

        "environment": "WSL2",

        "os": platform.system(),

        "os_version": platform.platform(),

        "kernel": platform.release(),

        "cpu_count": psutil.cpu_count(),

        "memory_total_gb":
            round(
                memory.total /
                1024 /
                1024 /
                1024,
                2
            ),

        "disk_total_gb":
            round(
                disk.total /
                1024 /
                1024 /
                1024,
                2
            ),
    }


def get_ip_address():

    try:

        hostname = socket.gethostname()

        addresses = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_INET
        )

        for address in addresses:

            ip = address[
                4
            ][0]

            if not ip.startswith(
                "127."
            ):

                return ip

    except Exception:

        pass

    return "N/A"


if __name__ == "__main__":

    info = get_server_info()

    print("=" * 50)
    print("Server Information")
    print("=" * 50)

    for key, value in info.items():

        print(
            f"{key:20}: {value}"
        )
