import sys

from analyzer.parser import parse_line

from analyzer.stats import (
    slowest_path,
    count_status_codes,
    count_endpoints,
    avg_response_time,
)


def main():

    # Check CLI argument
    if len(sys.argv) < 2:

        print(
            "Usage: python main.py <log_file>"
        )

        return

    log_file = sys.argv[1]

    entries = []

    parsed_count = 0
    malformed_count = 0

    try:

        with open(
            log_file,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                entry = parse_line(line)

                entries.append(entry)

                if entry.malformed:
                    malformed_count += 1
                else:
                    parsed_count += 1

    except FileNotFoundError:

        print(
            f"Error: File not found -> {log_file}"
        )

        return

    print("\n===== LOG ANALYSIS =====")

    print(
        f"\nParsed lines: {parsed_count}"
    )

    print(
        f"Malformed lines: {malformed_count}"
    )

    print(
        f"\nStatus code counts:\n"
        f"{count_status_codes(entries)}"
    )

    print(
        f"\nEndpoint counts:\n"
        f"{count_endpoints(entries)}"
    )

    print(
        f"\nAverage response time:"
        f" {avg_response_time(entries)} ms"
    )

    print(
        f"\nTop 5 slowest endpoints:"
    )

    for path, avg in slowest_path(entries):

        print(
            f"{path} -> {avg} ms"
        )


if __name__ == "__main__":
    main()