COMMON_SERVICES = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MYSQL",
    5432: "POSTGRESQL",
    8080: "HTTP-ALT"
}

def get_service(port):
    return COMMON_SERVICES.get(port, "UNKNOWN")