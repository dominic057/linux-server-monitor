from database import (
    get_metric_summary,
    get_incident_summary
)


SERVER_ID = "LINUX-WSL-001"


def main():

    metric_summary = get_metric_summary(
        SERVER_ID
    )

    incident_summary = get_incident_summary(
        SERVER_ID
    )

    (
        sample_count,
        avg_cpu,
        max_cpu,
        min_cpu,
        avg_memory,
        max_memory,
        avg_disk,
        max_disk
    ) = metric_summary

    (
        total_incidents,
        resolved_incidents,
        open_incidents
    ) = incident_summary

    print()
    print("=" * 60)
    print("           Linux Server Health Summary")
    print("=" * 60)

    print(
        f"Server ID:          {SERVER_ID}"
    )

    print(
        f"Monitoring Samples: {sample_count}"
    )

    print()

    print("CPU")
    print("-" * 60)

    print(
        f"Average CPU:        {avg_cpu:.2f}%"
    )

    print(
        f"Maximum CPU:        {max_cpu:.2f}%"
    )

    print(
        f"Minimum CPU:        {min_cpu:.2f}%"
    )

    print()

    print("Memory")
    print("-" * 60)

    print(
        f"Average Memory:     {avg_memory:.2f}%"
    )

    print(
        f"Maximum Memory:     {max_memory:.2f}%"
    )

    print()

    print("Disk")
    print("-" * 60)

    print(
        f"Average Disk:       {avg_disk:.2f}%"
    )

    print(
        f"Maximum Disk:       {max_disk:.2f}%"
    )

    print()

    print("Incident Statistics")
    print("-" * 60)

    print(
        f"Total Incidents:    {total_incidents}"
    )

    print(
        f"Resolved:           {resolved_incidents}"
    )

    print(
        f"Open:               {open_incidents}"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()
