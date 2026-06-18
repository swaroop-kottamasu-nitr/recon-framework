from datetime import datetime
import json

def save_report(target, open_ports, services, os_result):
    filename = (f"reports/{target}_report.txt")
    with open(filename, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("         FULL RECON REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated on: {datetime.now()}\n")
        f.write(f"Target: {target}\n")
        f.write(f"OPEN PORTS\n")
        f.write("-" * 20 + "\n")
        for service in services:
            f.write(f"\nPort: {service['port']}\n")
            f.write(f"Service: {service['service']}\n")
            if service["banner"]:
                f.write(f"Version: {service['banner'].splitlines()[0]}\n")
        f.write(f"\nTotal Open Ports: {len(open_ports)}\n")
        f.write("\nOS FINGERPRINT\n")
        f.write("-" * 20 + "\n")
        f.write(f"Likely OS: {os_result['os']}\n")
        f.write(f"Confidence: {os_result['confidence']}\n")
        f.write(f"\nTTL: {os_result['ttl']}\n")
        f.write(f"Window size: {os_result['window']}\n")
        
        f.write(f"\nEvidence:\n")
        for item in os_result["evidence"]:
            f.write(f"- {item}\n")        
    return filename    
def save_json_report(target, open_ports, services, os_result):
    filename = (f"reports/{target}_report.json")
    data = {"target": target, "open_ports": open_ports, "services": services, "os_fingerprint": os_result}

    with open(filename, "w") as file:
        json.dump(data,file,indent=4)
    return filename