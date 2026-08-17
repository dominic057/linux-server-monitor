import multiprocessing
import time


def cpu_stress():
    while True:
        pass


if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()

    print(f"Detected {cpu_count} CPU cores.")
    print("Starting CPU stress test...")

    processes = []

    for _ in range(cpu_count):
        process = multiprocessing.Process(target=cpu_stress)
        process.start()
        processes.append(process)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping CPU stress test...")

        for process in processes:
            process.terminate()

        for process in processes:
            process.join()
