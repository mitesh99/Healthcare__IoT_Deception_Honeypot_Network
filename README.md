[README.md](https://github.com/user-attachments/files/26225295/README.md)
# 🏥 Healthcare IoT Honeypot Network

> **Advanced Deception Technology for Medical IoT Security Research**

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Docker](https://img.shields.io/badge/docker-required-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Project Overview

This project implements a **Healthcare IoT Deception Honeypot Network** that simulates vulnerable medical devices (patient monitors, infusion pumps) to attract, log, and analyze real-world cyberattacks targeting healthcare infrastructure.

**Organization:** Infotact Solutions & Co.  
**Domain:** Cybersecurity — IoT Deception Technology  
**Stack:** Python + Flask + Docker + ELK Stack  
**Duration:** 4 Weeks  

---

## 🏗️ Architecture

```
Internet Attackers
        │
        ▼
┌─────────────────────────────────────────┐
│         Cowrie SSH Honeypot             │
│   Fake: CareFusion Patient Monitor v2   │
│   Ports: 2222 (SSH) | 2223 (Telnet)    │
└──────────────┬──────────────────────────┘
               │ JSON Logs
               ▼
┌─────────────────────────────────────────┐
│    Filebeat → Logstash → Elasticsearch  │
│    GeoIP Enrichment + Attack Classification
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
  ┌─────────┐    ┌─────────────┐
  │ Kibana  │    │   Flask     │
  │ :5601   │    │  Dashboard  │
  │         │    │   :5000     │
  └─────────┘    └─────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Ubuntu 20.04+ / Debian 11+
- Docker Engine 24.x+
- Docker Compose v2.x+
- Python 3.10+
- 4GB RAM minimum (8GB recommended)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/healthcare-iot-honeypot.git
cd healthcare-iot-honeypot
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

### 3. Start All Services
```bash
docker compose up -d --build
```

### 4. Verify Everything is Running
```bash
docker compose ps
```

Expected output:
```
NAME                STATUS
cowrie_honeypot     Up
elasticsearch       Up
logstash            Up
kibana              Up
filebeat            Up
attack_dashboard    Up
```

### 5. Access Services
| Service | URL | Credentials |
|---------|-----|-------------|
| Custom Dashboard | http://localhost:5000 | None |
| Kibana | http://localhost:5601 | None |
| Grafana | http://localhost:3000 | admin / admin123 |
| Elasticsearch | http://localhost:9200 | None |

---

## 📁 Project Structure

```
healthcare-iot-honeypot/
├── honeypot/
│   └── cowrie/
│       ├── Dockerfile
│       ├── cowrie.cfg          # Honeypot configuration
│       ├── userdb.txt          # Fake credentials
│       └── filesystem/         # Fake medical device filesystem
│           ├── etc/hostname
│           ├── home/nurse/patient_records.txt
│           └── var/log/vitals.log
├── logging/
│   ├── filebeat/
│   │   └── filebeat.yml
│   ├── logstash/
│   │   └── pipeline/
│   │       ├── 01_input.conf
│   │       ├── 02_filter.conf
│   │       └── 03_output.conf
│   └── parsers/
│       └── cowrie_parser.py
├── dashboard/
│   ├── Dockerfile
│   ├── app.py                  # Flask backend
│   ├── requirements.txt
│   └── templates/
│       └── dashboard.html      # Dark theme UI
├── analysis/
│   └── reports/
│       └── generate_final_report.py
├── data/
│   ├── logs/cowrie/            # Cowrie JSON logs
│   ├── processed/              # Parsed reports + CSVs
│   └── GeoLite2-City.mmdb     # GeoIP database
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Elasticsearch
ES_JAVA_OPTS=-Xms512m -Xmx512m

# Dashboard
SECRET_KEY=your-secret-key-here
ELASTICSEARCH_HOST=http://elasticsearch:9200

# Grafana
GF_SECURITY_ADMIN_PASSWORD=admin123
```

### Cowrie Honeypot Config
The honeypot simulates `CareFusion Patient Monitor v2.3.1`:
- **Hostname:** `patient-monitor-03`
- **SSH Port:** 2222
- **Telnet Port:** 2223
- **Banner:** `CareFusion Patient Monitor v2.3.1`

---

## 📊 Attack Classification

| Event ID | Attack Type | Description |
|----------|-------------|-------------|
| `cowrie.login.failed` | `bruteforce` | Wrong password attempt |
| `cowrie.login.success` | `credential_theft` | Successful unauthorized login |
| `cowrie.command.input` | `command_injection` | Command execution inside honeypot |
| `cowrie.session.file_download` | `malware_delivery` | File download attempt |

---

## 🐍 IoC Parser Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run parser (last 24 hours)
python3 logging/parsers/cowrie_parser.py

# Generate final report
python3 analysis/reports/generate_final_report.py
```

---

## 🛑 Security Warning

> ⚠️ **This honeypot is for research and educational purposes only.**  
> Deploy only in isolated network environments.  
> Never expose to production networks without proper network segmentation.  
> All captured credentials are fake — never use real patient data.

---

## 📈 Findings Summary (30-Day Period)

| Metric | Value |
|--------|-------|
| Total Attack Attempts | 500+ |
| Unique Attacking IPs | 25+ |
| Successful Breaches | 18 |
| Malware Samples Captured | 3 |
| Countries of Origin | 12+ |
| Most Common Username | admin, root |
| Most Common Password | admin, 123456 |

---

## 🔒 Security Recommendations

1. **Network Segmentation** — Isolate all IoT medical devices on dedicated VLANs
2. **Disable Default Credentials** — Change all factory passwords immediately
3. **Firewall Rules** — Block top attacking IP ranges at perimeter
4. **Multi-Factor Authentication** — Enforce MFA for all remote access
5. **Vulnerability Scanning** — Quarterly scans of all IoT devices
6. **Threat Intelligence Sharing** — Share IOCs with Healthcare-ISAC

---

## 👥 Team

| # | Name | Role |
|---|------|------|
| 1 | Mitesh | Lead Developer / Security Engineer |
| 2 | Minakshi | Backend Developer |
| 3 | Mahek | Frontend Developer / Dashboard |
| 4 | Arkadip | DevOps / Documentation |

---

## 📄 License

MIT License — For educational and research purposes only.

---

*Healthcare IoT Honeypot Network — Infotact Solutions & Co. — Cybersecurity Track*
