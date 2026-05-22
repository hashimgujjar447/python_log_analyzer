import random
import json
from datetime import datetime, timedelta,UTC
from pathlib import Path

OUTPUT_FILE="sample_logs/generated_logs.log"

IPS=[
     "192.168.1.42",
    "10.0.0.7",
    "172.16.0.4",
    "192.168.0.9",
]

METHODS=[
    "GET",
    "POST",
    "PUT",
    "DELETE",

]

PATHS = [
    "/api/users",
    "/api/login",
    "/api/orders",
    "/api/search",
    "/health",
]

STATUS_CODES = [200, 201, 204, 400, 401, 403, 404, 500]


USER_AGENTS = [
    "Mozilla/5.0",
    "curl/8.0",
    "PostmanRuntime/7.32",
]

STACK_TRACE = [
    "java.lang.NullPointerException",
    "at com.example.auth.LoginService.login(LoginService.java:42)",
    "at com.example.api.AuthController.handle(AuthController.java:18)",
]



def random_timestamp():
    now=datetime.now(UTC)-timedelta(seconds=random.randint(0,100000))

   
    format_type = random.choice([
        "iso",
        "slash",
        "apache",
        "epoch"
    ])

    if format_type=="iso":
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    if format_type=="slash":
        return now.strftime("%Y/%m/%d %H:%M:%S")
    
    if format_type == "apache":
        return now.strftime("%d-%b-%Y %H:%M:%S")
    
    if format_type=="epoch":
        return str(int(now.timestamp()))
    



def generate_standard_line():
    timestamp=random_timestamp()
    ip=random.choice(IPS)
    method=random.choice(METHODS)
    path=random.choice(PATHS)
    status=random.choice(STATUS_CODES)


    response_time=random.choice([
        f"{random.randint(10,500)}ms",
        f"{round(random.uniform(0.01, 2.0), 3)}s",
        str(random.randint(1,500)),
    ])


    return (
        f"{timestamp} {ip} {method} "
        f"{path} {status} {response_time}"
    )

def generate_json_line():
    payload={
        "timestamp":random_timestamp(),
        "ip":random.choice(IPS),
        "method":random.choice(METHODS),
        "path":random.choice(PATHS),
        "status":random.choice(STATUS_CODES),
        "response_time":f"{random.randint(1,500)}ms",

    }

    return json.dumps(payload)



def generate_missing_fields_line():
    timestamp=random_timestamp()
    ip=random.choice(IPS)
    method=random.choice(METHODS)
    path=random.choice(PATHS)

    return (
        f"{timestamp} {ip} {method} {path}"
        
    )


def generate_malformed_line():
    malformed=[
        "This is not a valid log line",
        "2024-06-01T12:00:00Z - Missing fields",
        "XXX.XXX.XXX.XXX GET /api/users 200ms",  # Malformed IP
        "GET GET GET",
        "null null null",
        "",
    ]

    return random.choice(malformed)


def generate_stack_trace():
    return "\n".join(STACK_TRACE)



def generate_log_file(LINES=10000):
    Path("sample_logs").mkdir(exist_ok=True)
    with open(OUTPUT_FILE,"w") as f:
        for _ in range(LINES):
            choice=random.random()

            if choice < 0.70:
                line=generate_standard_line()
            elif choice < 0.80:
                line=generate_json_line()
            elif choice < 0.90:
                line=generate_missing_fields_line()
            elif choice < 0.95:
                line=generate_malformed_line()
            else:
                line=generate_stack_trace()

            f.write(line+"\n")
        print(f"Generated log file: {OUTPUT_FILE}")        
if __name__=="__main__":
    generate_log_file()
