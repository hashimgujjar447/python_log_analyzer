from analyzer.parser import parse_line



def main():

    entries = []

    parsed_count = 0
    malformed_count = 0

    with open(
        "sample_logs/generated_logs.log",
        "r"
    ) as file:

        for line in file:

            entry = parse_line(line)

            entries.append(entry)

            if entry.malformed:
                malformed_count += 1
            else:
                parsed_count += 1

    print(f"\nParsed lines: {parsed_count}")
    print(f"Malformed lines: {malformed_count}")

    

if __name__ == "__main__":
    main()