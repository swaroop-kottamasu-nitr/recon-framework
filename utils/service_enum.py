from utils.version_detector import detect_version


COMMON_SERVICES = {
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
    8080: "HTTP-ALT"
}


def enumerate_service(target, port):

    service = COMMON_SERVICES.get(
        port,
        "UNKNOWN"
    )

    banner = detect_version(
        target,
        port
    )
    if banner:

        banner_lower = banner.lower()

        if "vsftpd" in banner_lower:
            service = "vsFTPd FTP"

        elif "proftpd" in banner_lower:
            service = "ProFTPD FTP"

        elif "filezilla" in banner_lower:
            service = "FileZilla FTP"

        elif "pure-ftpd" in banner_lower:
            service = "Pure-FTPd FTP"
    return {
        "port": port,
        "service": service,
        "banner": banner
    }