# 🖥️ System Diagnostics & Network Monitor

A Python script that generates a complete system health report — covering OS info, CPU, memory, disk usage, and network connectivity — and optionally saves it to a `.txt` file.

Built by **Oyalana Samuel** | [LinkedIn](https://linkedin.com) | [Portfolio](https://notion.so)

---

## 📋 What It Checks

| Category | Details |
|----------|---------|
| **OS** | System, release, version, hostname, Python version |
| **Network** | Local IP, gateway ping, DNS resolution, internet connectivity |
| **CPU** | Usage %, core count, clock speed |
| **Memory** | Used / Total MB, usage % |
| **Disk** | Used / Total GB, usage % |
| **Recommendations** | Auto-generated based on findings |

---

## 🚀 Getting Started

### Requirements
- Python 3.7+
- `psutil` (for CPU/memory/disk metrics)

```bash
pip install psutil
```

### Run

```bash
python diagnostics.py
```

---

## 📸 Sample Output

```
════════════════════════════════════════════════════
  SYSTEM DIAGNOSTICS REPORT
  Generated: 2026-04-15 10:32:44
════════════════════════════════════════════════════

──────────────────────────────────────────────────
  OPERATING SYSTEM
──────────────────────────────────────────────────
  System    : Windows 11
  Hostname  : SAMUEL-PC
  Python    : 3.11.2

──────────────────────────────────────────────────
  NETWORK STATUS
──────────────────────────────────────────────────
  Local IP        : 192.168.1.105
  Gateway (8.8.8.8)      : ✔  PASS
  DNS Resolution         : ✔  PASS
  Google.com             : ✔  PASS
  Cloudflare.com         : ✔  PASS
  Overall Network        : ✔  HEALTHY

──────────────────────────────────────────────────
  SYSTEM PERFORMANCE
──────────────────────────────────────────────────
  CPU Usage   : 23.4%  [NORMAL]  | Cores: 8 | 2400 MHz
  Memory      : 5120 MB / 16384 MB  (31.2%)  [NORMAL]
  Disk (/)    : 120.3 GB / 500.0 GB  (24.1%)  [NORMAL]

──────────────────────────────────────────────────
  RECOMMENDATIONS
──────────────────────────────────────────────────
  ✔  All systems look healthy. No immediate action needed.
```

---

## 💾 Save to File

At the end of the run, you'll be prompted:
```
Save report to file? (y/n):
```
Choosing `y` saves a timestamped `.txt` file like `diagnostics_report_20260415_103244.txt`.

---

## 🎮 Usage Walkthrough

### Step 1 — Run the script
```bash
python diagnostics.py
```

You'll see the banner and a loading message:
```
  ╔══════════════════════════════════════════╗
  ║    SYSTEM DIAGNOSTICS & NETWORK MONITOR  ║
  ║          by Oyalana Samuel               ║
  ╚══════════════════════════════════════════╝

  Running diagnostics — please wait…
```

---

### Step 2 — Read your report

The full report prints automatically. No input needed during the run:

```
════════════════════════════════════════════════════
  SYSTEM DIAGNOSTICS REPORT
  Generated: 2026-04-15 10:32:44
════════════════════════════════════════════════════

──────────────────────────────────────────────────
  OPERATING SYSTEM
──────────────────────────────────────────────────
  System    : Windows 11
  Release   : 10.0.22621
  Machine   : AMD64
  Processor : Intel Core i5-1135G7
  Hostname  : SAMUEL-PC
  Python    : 3.11.2

──────────────────────────────────────────────────
  NETWORK STATUS
──────────────────────────────────────────────────
  Local IP              : 192.168.1.105
  Gateway (8.8.8.8)     : ✔  PASS
  DNS Resolution        : ✔  PASS
  Google.com            : ✔  PASS
  Cloudflare.com        : ✔  PASS

  Overall Network       : ✔  HEALTHY

──────────────────────────────────────────────────
  SYSTEM PERFORMANCE
──────────────────────────────────────────────────
  CPU Usage   : 23.4%  [NORMAL]  | Cores: 8 | 2400 MHz
  Memory      : 5120 MB / 16384 MB  (31.2%)  [NORMAL]
  Disk (/)    : 120.3 GB / 500.0 GB  (24.1%)  [NORMAL]

──────────────────────────────────────────────────
  RECOMMENDATIONS
──────────────────────────────────────────────────
  ✔  All systems look healthy. No immediate action needed.
```

---

### Step 3 — Save the report (optional)

At the end you're asked:
```
  Save report to file? (y/n):
```

Type `y` and a timestamped `.txt` file is saved to the same folder:
```
  ✔ Report saved → diagnostics_report_20260415_103244.txt
```

Type `n` to exit without saving.

---

### What the status labels mean

| Label | Meaning |
|-------|---------|
| `NORMAL` | Within healthy operating range |
| `MODERATE` | Worth monitoring, not urgent |
| `HIGH / FULL` | Action recommended |
| `PASS` | Network check succeeded |
| `FAIL` | Network check failed — see Recommendations |

---

## 🧠 Skills Demonstrated

- System monitoring (psutil)
- Network diagnostics (ping, DNS, socket)
- Structured reporting & documentation
- Python scripting best practices
- IT support methodology

---

## 📬 Contact

**Oyalana Samuel** — oyalanasam@gmail.com  
Open to IT Support, Technical Operations, and AI-related roles.
