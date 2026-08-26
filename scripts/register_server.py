from database import (
    init_database,
    register_server,
    list_servers
)

from server_info import get_server_info


def main():

    # 初始化数据库
    init_database()

    # 获取服务器信息
    server_info = get_server_info()

    # 注册服务器
    register_server(
        server_info
    )

    print(
        "Server registered successfully."
    )

    print()

    print(
        "Current Server:"
    )

    for key, value in server_info.items():

        print(
            f"{key:20}: {value}"
        )

    print()

    print(
        "Database Servers:"
    )

    servers = list_servers()

    for server in servers:

        print(server)


if __name__ == "__main__":

    main()
