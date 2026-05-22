# ANSWERS.md

## 1. How to run

### Requirements

- Python 3.11+

No external libraries are required for this project.

---

### Generate sample logs

```bash
python scripts/generate_logs.py
```

This will create:

```txt
sample_logs/generated_logs.log
```

---

### Run the analyzer

```bash
python main.py sample_logs/generated_logs.log
```

---

## 2. Stack choice

I chose Python because I think it is very good for tasks related to file handling, parsing, regex, and data processing. Python also has many built-in modules that helped me keep the project simple without adding external dependencies.

Another reason was readability. Since the project involved handling different log formats and malformed lines, Python made it easier to write and debug the parser quickly.

I think JavaScript would have been a worse choice for this task because for backend file processing and parsing, it would require more setup and extra code compared to Python.

---

## 3. One real edge case

One edge case my code handles is malformed log lines or stack trace lines mixed inside the logs.

Examples:

```txt
GET GET GET
```

or:

```txt
java.lang.NullPointerException
```

This is handled inside:

```txt
analyzer/parser.py
```

in the `parse_line()` function.

Instead of crashing when a bad line appears, the parser creates a malformed `LogEntry` object and continues processing the rest of the file.

Without this handling, one invalid line could stop the entire analysis process.

The tool also keeps count of malformed lines separately so they are not silently ignored.

---

## 4. AI usage

I used AI during development mainly for brainstorming ideas, discussing project structure, improving regex logic, and reviewing parts of the parser implementation.

I also used AI to better understand:
- timestamp parsing
- malformed log handling
- regex groups
- cleaner project structure

One thing I changed from the AI-generated suggestions was timestamp handling. Initially, the suggested code used older UTC handling methods. I updated it to use:

```python
datetime.now(UTC)
```

and improved some of the parsing flow after testing it with generated logs.

I also simplified some parts of the generated code because I wanted the project to stay readable and easier to debug.

---

## 5. Honest gap

One thing I would improve with more time is reducing repeated logic in some places.

For example, both the JSON parser and standard parser repeat similar field extraction code like:

```python
timestamp=parse_timestamp(...)
ip=data.get("ip")
method=data.get("method")
```

The log generator also repeats some random field generation logic.

With another day, I would refactor these parts into reusable helper functions to reduce duplication and make the code cleaner.

I would also improve support for extra fields appended at the end of log lines, like user agents or referrer strings.