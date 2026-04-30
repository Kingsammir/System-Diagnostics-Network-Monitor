#!/usr/bin/env python3
"""
System Diagnostics & Network Monitor
Author: Oyalana Samuel
Description: Generates a full system health report covering OS info,
             CPU, memory, disk, and network status. Saves report to file.
"""

import platform
import socket
import subprocess
import datetime
import os
import sys
import json


# ─────────────────────────────────────────────
#  COLOUR HELPERS
# ─────────────────────────────────────────────
class C:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def status_icon(value, warn_thresh, fail_thresh, higher_is_bad=True):
    """Return coloured icon based on thresholds."""
    if higher_is_bad:
        if value >= fail_thresh: return f"{C.RED}✘{C.RESET}"
        if value >= warn_thresh: return f"{C.YELLOW}!{C.RESET}"
        return f"{C.GREEN}✔{C.RESET}"
    else:
        if value <= fail_thresh: return f"{C.RED}✘{C.RESET}"
        if value <= warn_thresh: return f"{C.YELLOW}!{C.RESET}"
        return f"{C.GREEN}✔{C.RESET}"


# ─────────────────────────────────────────────
#  DATA COLLECTORS
# ─────────────────────────────────────────────
def get_os_info() -> dict:
    return {
        "system":    platform.system(),
        "release":   platform.release(),
        "version":   platform.version(),
        "machine":   platform.machine(),
        "processor": platform.processor(),
        "hostname":  socket.gethostname(),
        "python":    platform.python_version(),
    }


def get_network_info() -> dict:
    results = {}

    # Local IP
    try:
        results["local_ip"] = socket.gethostbyname(socket.gethostname())
    except Exception:
        results["local_ip"] = "Unavailable"

    # Connectivity checks
    hosts = {
        "gateway_8.8.8.8":  "8.8.8.8",
        "dns_google.com":    "google.com",
        "cloudflare.com":    "cloudflare.com",
    }
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    for label, host in hosts.items():
        r = subprocess.run(
            ["ping", flag, "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        results[label] = r.returncode == 0

    # DNS resolution
    try:
        socket.gethostbyname("google.com")
        results["dns_resolution"] = True
    except socket.gaierror:
        results["dns_resolution"] = False

    return results


def get_performance_info() -> dict:
    data = {}
    try:
        import psutil

        # CPU
        data["cpu_percent"]  = psutil.cpu_percent(interval=1)
        data["cpu_count"]    = psutil.cpu_count(logical=True)
        data["cpu_freq_mhz"] = round(psutil.cpu_freq().current) if psutil.cpu_freq() else "N/A"

        # Memory
        mem = psutil.virtual_memory()
        data["mem_total_mb"] = round(mem.total / 1024**2)
        data["mem_used_mb"]  = round(mem.used  / 1024**2)
        data["mem_percent"]  = mem.percent

        # Disk
        disk = psutil.disk_usage("/")
        data["disk_total_gb"] = round(disk.total / 1024**3, 1)
        data["disk_used_gb"]  = round(disk.used  / 1024**3, 1)
        data["disk_percent"]  = disk.percent

        data["psutil"] = True

    except ImportError:
        data["psutil"] = False

    return data


# ─────────────────────────────────────────────
#  REPORT RENDERER
# ─────────────────────────────────────────────
def render_report(os_info: dict, net_info: dict, perf_info: dict) -> str:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []

    def sep(title=""):
        lines.append(f"\n{'─'*52}")
        if title:
            lines.append(f"  {title}")
            lines.append(f"{'─'*52}")

    lines.append(f"\n{'═'*52}")
    lines.append(f"  SYSTEM DIAGNOSTICS REPORT")
    lines.append(f"  Generated: {ts}")
    lines.append(f"{'═'*52}")

    # OS
    sep("OPERATING SYSTEM")
    lines.append(f"  System    : {os_info['system']} {os_info['release']}")
    lines.append(f"  Version   : {os_info['version'][:60]}")
    lines.append(f"  Machine   : {os_info['machine']}")
    lines.append(f"  Processor : {os_info['processor'][:50] or 'N/A'}")
    lines.append(f"  Hostname  : {os_info['hostname']}")
    lines.append(f"  Python    : {os_info['python']}")

    # Network
    sep("NETWORK STATUS")
    lines.append(f"  Local IP        : {net_info.get('local_ip', 'N/A')}")

    checks = [
        ("Gateway (8.8.8.8)",  net_info.get("gateway_8.8.8.8")),
        ("DNS Resolution",      net_info.get("dns_resolution")),
        ("Google.com",          net_info.get("dns_google.com")),
        ("Cloudflare.com",      net_info.get("cloudflare.com")),
    ]
    for label, result in checks:
        icon = "✔  PASS" if result else "✘  FAIL"
        lines.append(f"  {label:<22}: {icon}")

    overall_net = all(v for k, v in net_info.items() if isinstance(v, bool))
    lines.append(f"\n  Overall Network : {'✔  HEALTHY' if overall_net else '✘  ISSUES DETECTED'}")

    # Performance
    sep("SYSTEM PERFORMANCE")
    if perf_info.get("psutil"):
        cpu = perf_info["cpu_percent"]
        mem = perf_info["mem_percent"]
        disk = perf_info["disk_percent"]

        cpu_status  = "HIGH"   if cpu  > 80 else ("MODERATE" if cpu  > 50 else "NORMAL")
        mem_status  = "HIGH"   if mem  > 85 else ("MODERATE" if mem  > 65 else "NORMAL")
        disk_status = "FULL"   if disk > 90 else ("WARNING"  if disk > 75 else "NORMAL")

        lines.append(f"  CPU Usage   : {cpu:.1f}%  [{cpu_status}]  | Cores: {perf_info['cpu_count']} | {perf_info['cpu_freq_mhz']} MHz")
        lines.append(f"  Memory      : {perf_info['mem_used_mb']} MB / {perf_info['mem_total_mb']} MB  ({mem:.1f}%)  [{mem_status}]")
        lines.append(f"  Disk (/)    : {perf_info['disk_used_gb']} GB / {perf_info['disk_total_gb']} GB  ({disk:.1f}%)  [{disk_status}]")
    else:
        lines.append("  Performance metrics unavailable.")
        lines.append("  Install psutil:  pip install psutil")

    # Recommendations
    sep("RECOMMENDATIONS")
    recs = []
    if perf_info.get("psutil"):
        if perf_info["cpu_percent"] > 80:
            recs.append("⚠  High CPU — close unused applications or check for malware.")
        if perf_info["mem_percent"] > 85:
            recs.append("⚠  High memory — close browser tabs; consider a RAM upgrade.")
        if perf_info["disk_percent"] > 90:
            recs.append("⚠  Disk nearly full — delete old files or move to external storage.")
    if not net_info.get("dns_resolution"):
        recs.append("⚠  DNS failure — try changing DNS to 8.8.8.8 / 1.1.1.1.")
    if not net_info.get("gateway_8.8.8.8"):
        recs.append("⚠  No gateway — restart your router/modem.")
    if not recs:
        recs.append("✔  All systems look healthy. No immediate action needed.")

    for r in recs:
        lines.append(f"  {r}")

    lines.append(f"\n{'═'*52}")
    lines.append(f"  End of Report — Oyalana Samuel")
    lines.append(f"{'═'*52}\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────
#  SAVE TO FILE
# ─────────────────────────────────────────────
def save_report(report_text: str) -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnostics_report_{ts}.txt"
    with open(filename, "w") as f:
        f.write(report_text)
    return filename


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    print(f"\n{C.BOLD}{C.CYAN}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║    SYSTEM DIAGNOSTICS & NETWORK MONITOR  ║")
    print("  ║          by Oyalana Samuel               ║")
    print("  ╚══════════════════════════════════════════╝")
    print(f"{C.RESET}")
    print(f"  {C.YELLOW}Running diagnostics — please wait…{C.RESET}\n")

    os_info   = get_os_info()
    net_info  = get_network_info()
    perf_info = get_performance_info()

    report = render_report(os_info, net_info, perf_info)
    print(report)

    save = input(f"  {C.CYAN}Save report to file? (y/n): {C.RESET}").strip().lower()
    if save == "y":
        fname = save_report(report)
        print(f"\n  {C.GREEN}✔ Report saved → {fname}{C.RESET}\n")
    else:
        print(f"\n  {C.GREEN}Done. Goodbye!{C.RESET}\n")


if __name__ == "__main__":
    main()
