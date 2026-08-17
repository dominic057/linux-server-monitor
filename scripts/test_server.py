import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from database import (
    init_database,
    register_server,
    list_servers
)

from server_info import (
    get_server_info
)


def main():

    # 初始化数据库
    init_database()

    # 获取服务器信息
    info = get_server_info()

    print(
        "Registering server..."
    )

    # 注册服务器
    register_server(info)

    print(
        "Server registered successfully."
    )

    print()

    print(
        "Server Records:"
    )

    servers = list_servers()

    for server in servers:

        print(server)


if __name__ == "__main__":

    main()
