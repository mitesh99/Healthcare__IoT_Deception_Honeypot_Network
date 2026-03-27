#!/usr/bin/env python3
import json, os, pandas as pd
from datetime import datetime, timedelta
from collections import Counter

class CowrieThreatIntelParser:
    def __init__(self, log_dir="./data/logs/cowrie", output_dir="./data/processed"):
        self.log_dir = log_dir
        self.output_dir = output_dir
        self.iocs = {
            "ip_addresses": [], "usernames": [],
            "passwords": [], "commands": [], "malware_hashes": []
        }
        os.makedirs(output_dir, exist_ok=True)

    def parse_logs(self, hours=24):
        print(f"[*] Last {hours}h ke logs parse ho rahe hain...")
        cutoff = datetime.now() - timedelta(hours=hours)
        for fname in os.listdir(self.log_dir):
            if not fname.endswith(".json"): continue
            fpath = os.path.join(self.log_dir, fname)
            if datetime.fromtimestamp(os.path.getmtime(fpath)) < cutoff: continue
            print(f"    -> {fname}")
            with open(fpath) as f:
                for line in f:
                    try: self._extract(json.loads(line.strip()))
                    except: continue
        return self.iocs

    def _extract(self, e):
        event = e.get("eventid", "")
        src = e.get("src_ip")
        ts = e.get("timestamp")
        if src:
            self.iocs["ip_addresses"].append({"ip": src, "ts": ts, "event": event})
        if "login" in event:
            u = e.get("username", "")
            p = e.get("password", "")
            if u: self.iocs["usernames"].append({"username": u, "ts": ts, "src_ip": src})
            if p: self.iocs["passwords"].append({"password": p, "ts": ts, "src_ip": src})
        elif event == "cowrie.command.input":
            cmd = e.get("input", "")
            if cmd: self.iocs["commands"].append({"command": cmd, "ts": ts, "src_ip": src})
        elif event == "cowrie.session.file_download":
            h = e.get("shasum", "")
            if h: self.iocs["malware_hashes"].append({
                "hash": h, "filename": e.get("filename", ""), "ts": ts, "src_ip": src
            })

    def generate_report(self):
        ips = [i["ip"] for i in self.iocs["ip_addresses"]]
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "unique_ips": len(set(ips)),
                "unique_usernames": len(self.iocs["usernames"]),
                "unique_passwords": len(self.iocs["passwords"]),
                "total_commands": len(self.iocs["commands"]),
                "malware_samples": len(self.iocs["malware_hashes"]),
            },
            "top_attackers": Counter(ips).most_common(10),
            "top_usernames": Counter([u["username"] for u in self.iocs["usernames"]]).most_common(10),
            "top_passwords": Counter([p["password"] for p in self.iocs["passwords"]]).most_common(10),
            "recent_commands": self.iocs["commands"][-20:],
            "malware_hashes": self.iocs["malware_hashes"],
        }
        out = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(out, "w") as f: json.dump(report, f, indent=2)
        print(f"✅ Report saved -> {out}")
        return report

    def export_csv(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for key, fname in [
            ("ip_addresses", f"ips_{ts}.csv"),
            ("usernames", f"usernames_{ts}.csv"),
            ("passwords", f"passwords_{ts}.csv"),
            ("commands", f"commands_{ts}.csv")
        ]:
            if self.iocs[key]:
                pd.DataFrame(self.iocs[key]).to_csv(
                    os.path.join(self.output_dir, fname), index=False
                )
        print(f"✅ CSV exports -> {self.output_dir}")

if __name__ == "__main__":
    p = CowrieThreatIntelParser()
    p.parse_logs(hours=24)
    r = p.generate_report()
    print("\n========== SUMMARY ==========")
    s = r["summary"]
    print(f"Unique Attackers  : {s['unique_ips']}")
    print(f"Usernames Tried   : {s['unique_usernames']}")
    print(f"Passwords Tried   : {s['unique_passwords']}")
    print(f"Commands Executed : {s['total_commands']}")
    print(f"Malware Samples   : {s['malware_samples']}")
    print("==============================")
    for ip, cnt in r["top_attackers"][:5]:
        print(f"  {ip} -> {cnt} attempts")
    p.export_csv()
