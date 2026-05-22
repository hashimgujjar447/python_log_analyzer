from collections import Counter, defaultdict


def count_status_codes(entries):

    counter = Counter()

    for entry in entries:

        if entry.malformed:
            continue

        if entry.status is not None:
            counter[entry.status] += 1

    return counter


def count_endpoints(entries):

    counter = Counter()

    for entry in entries:

        if entry.malformed:
            continue

        if entry.path:
            counter[entry.path] += 1

    return counter


def avg_response_time(entries):

    total = 0
    count = 0

    for entry in entries:

        if entry.malformed:
            continue

        if entry.response_time_ms is not None:
            total += entry.response_time_ms
            count += 1

    if count == 0:
        return 0

    return round(total / count, 2)


def slowest_path(entries):

    path_times = defaultdict(list)

    for entry in entries:

        if entry.malformed:
            continue

        if (
            entry.path
            and entry.response_time_ms is not None
        ):
            path_times[entry.path].append(
                entry.response_time_ms
            )

    averages = []

    for path, times in path_times.items():

        avg = sum(times) / len(times)

        averages.append(
            (path, round(avg, 2))
        )

    averages.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return averages[:5]