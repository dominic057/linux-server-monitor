import platform
import socket
import psutil
from datetime import datetime


SERVER_ID = "LINUX-WSL-001"


def get_ip_address():

    try:

        hostname = socket.gethostname()

        addresses = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_INET
        )

        for address in addresses:

            ip = address[4][0]

            if not ip.startswith("127."):

                return ip

    except Exception:

        pass

    return "N/A"


def get_cpu_model():

    try:

        with open("/proc/cpuinfo", "r") as file:

            for line in file:

                if line.startswith("model name"):

                    return line.split(
                        ":",
                        1
                    )[1].strip()

    except Exception:

        pass

    return platform.processor()


def get_server_info():

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    return {

        "server_id":
            SERVER_ID,

        "hostname":
            socket.gethostname(),

        "ip_address":
            get_ip_address(),

        "environment":
            "WSL2",

        "os":
            platform.system(),

        "os_version":
            platform.platform(),

        "kernel":
            platform.release(),

        "cpu_model":
            get_cpu_model(),

        "cpu_count":
            psutil.cpu_count(),

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

        "collected_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }


if __name__ == "__main__":

    info = get_server_info()

    print("=" * 60)

    print(
        "Server Information"
    )

    print("=" * 60)

    for key, value in info.items():

        print(
            f"{key:20}: {value}"
        )

    print("=" * 60)
