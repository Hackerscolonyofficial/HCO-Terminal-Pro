#!/usr/bin/env python3
# HCO Terminal Pro — Advanced Ethical Hacking Terminal
# By Azhar (Hackers Colony)
# Single-file Termux interactive tool

import os, sys, platform, subprocess, time, random, curses

# -------------------- Configuration --------------------
YOUTUBE_URL = "https://youtube.com/@hackers_colony_tech"
TOOL_LOCK_SECONDS = 10
DASHBOARD_SIZE = 10  # Number of commands to keep in dashboard

# -------------------- Colors --------------------
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# -------------------- Utilities --------------------
def run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.strip()}"

def check_install(pkg):
    if run_cmd(f"which {pkg}") == "":
        os.system(f"pkg install {pkg} -y")

def clear():
    os.system("clear")

# -------------------- Tool Lock --------------------
def tool_lock():
    clear()
    print(f"{RED}This tool is locked 🔒{RESET}")
    print(f"{YELLOW}Only ethical usage allowed! Scan your own devices/networks.{RESET}")
    for i in range(TOOL_LOCK_SECONDS,0,-1):
        print(f"{YELLOW}Redirecting to YouTube in {i} seconds...{RESET}", end="\r")
        time.sleep(1)
    print("\n")
    os.system(f'am start -a android.intent.action.VIEW -d "{YOUTUBE_URL}"')
    input(f"{GREEN}Press Enter after returning from YouTube to unlock...{RESET}")

# -------------------- Banner --------------------
def banner(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, f"HCO Terminal Pro — by Azhar", curses.color_pair(2))
    stdscr.addstr(1, 0, "Ethical Hacking & Termux Learning", curses.color_pair(3))
    stdscr.addstr(2, 0, "-"*60, curses.color_pair(4))

# -------------------- Dashboard --------------------
class Dashboard:
    def __init__(self, size=DASHBOARD_SIZE):
        self.size = size
        self.entries = []

    def add_entry(self, command, output):
        timestamp = time.strftime("%H:%M:%S")
        self.entries.append((timestamp, command, output))
        if len(self.entries) > self.size:
            self.entries.pop(0)

    def display(self, stdscr):
        row = 4
        for ts, cmd, out in self.entries:
            stdscr.addstr(row, 0, f"[{ts}] {cmd}", curses.color_pair(3))
            row += 1
            for line in out.split("\n"):
                stdscr.addstr(row, 2, line, curses.color_pair(1))
                row += 1
            row += 1
        stdscr.refresh()

# -------------------- Commands --------------------
def cmd_help(args=None):
    return """
Available Commands:
scan <IP>        - nmap scan
ports <IP>       - quick TCP port check
ping <host>      - ping host
dnslookup <dom>  - DNS lookup
whois <dom/IP>   - WHOIS info
traceroute <host>- route packets
netinfo          - IP/interfaces/connections
checkurl <URL>   - HTTP headers/status
ipinfo <IP>      - Geolocation info
fetch <URL>      - Download file
banner <text>    - Print hacker banner
motd             - Quote of the day
learn <topic>    - Short explanation
examples         - Show ethical examples
tips             - Ethical hacking tips
safeports        - Safe ports to scan
osinfo           - OS, CPU, memory
diskinfo         - Disk usage
meminfo          - RAM & swap
termuxinfo       - Termux environment
whoami           - Current user & hostname
uptime           - System uptime
clear            - Clear dashboard
help             - This help
exit             - Quit
"""

def cmd_scan(args): return run_cmd(f"nmap {' '.join(args)}") if args else "Usage: scan <IP>"
def cmd_ports(args):
    if not args: return "Usage: ports <IP>"
    ports = [21,22,23,25,53,80,110,139,143,443,445,3389]
    results=[]
    for port in ports:
        res = run_cmd(f"nc -zv {args[0]} {port}")
        results.append(res)
    return "\n".join(results)
def cmd_ping(args): return run_cmd(f"ping -c 4 {args[0]}") if args else "Usage: ping <host>"
def cmd_dnslookup(args): return run_cmd(f"nslookup {args[0]}") if args else "Usage: dnslookup <domain>"
def cmd_whois(args): return run_cmd(f"whois {args[0]}") if args else "Usage: whois <domain/IP>"
def cmd_traceroute(args): return run_cmd(f"traceroute {args[0]}") if args else "Usage: traceroute <host>"
def cmd_netinfo(args): return run_cmd("ifconfig || ip addr")
def cmd_checkurl(args): return run_cmd(f"curl -I {args[0]}") if args else "Usage: checkurl <URL>"
def cmd_ipinfo(args): return run_cmd(f"curl -s ipinfo.io/{args[0]}") if args else "Usage: ipinfo <IP>"
def cmd_fetch(args): return run_cmd(f"curl -O {args[0]}") if args else "Usage: fetch <URL>"
def cmd_banner(args): 
    text=" ".join(args)
    if run_cmd("which toilet"): os.system(f'toilet -f mono12 -F metal "{text}"')
    elif run_cmd("which figlet"): os.system(f'figlet "{text}"')
    else: return "Install toilet or figlet to use banner"
    return "Banner displayed"
def cmd_motd(args=None): 
    quotes=["The quieter you become, the more you hear.","Stay ethical, stay curious.","Learn, Practice, Protect.","Knowledge is power, hacking is skill."]
    return random.choice(quotes)
def cmd_learn(args): 
    topics={"nmap":"Nmap discovers hosts and services.","ping":"Ping checks connectivity.","whois":"WHOIS shows domain/IP info.","dns":"DNS resolves domains.","ethical":"Always get permission before scanning."}
    return topics.get(args[0].lower(),"No info for this topic") if args else "Usage: learn <topic>"
def cmd_examples(args=None): return "scan 192.168.1.1\nports 192.168.1.1\nping 8.8.8.8\nfetch https://example.com/file.txt\ndnslookup example.com\nwhois example.com"
def cmd_tips(args=None): return "Always scan your own devices.\nNever misuse commands.\nPractice in labs.\nDocument responsibly."
def cmd_safeports(args=None): return "Safe ports: 22,80,443,8080"
def cmd_osinfo(args=None): return f"OS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}\nMachine: {platform.machine()}"
def cmd_diskinfo(args=None): return run_cmd("df -h")
def cmd_meminfo(args=None): return run_cmd("free -h")
def cmd_termuxinfo(args=None): return f"HOME={os.environ.get('HOME','N/A')}\nPATH={os.environ.get('PATH','N/A')}"
def cmd_whoami(args=None): return f"User: {run_cmd('whoami')} | Host: {run_cmd('hostname')}"
def cmd_uptime(args=None): return run_cmd("uptime")
def cmd_clear(args=None): return "clear"

COMMANDS = {
    "help": cmd_help,
    "scan": cmd_scan,
    "ports": cmd_ports,
    "ping": cmd_ping,
    "dnslookup": cmd_dnslookup,
    "whois": cmd_whois,
    "traceroute": cmd_traceroute,
    "netinfo": cmd_netinfo,
    "checkurl": cmd_checkurl,
    "ipinfo": cmd_ipinfo,
    "fetch": cmd_fetch,
    "banner": cmd_banner,
    "motd": cmd_motd,
    "learn": cmd_learn,
    "examples": cmd_examples,
    "tips": cmd_tips,
    "safeports": cmd_safeports,
    "osinfo": cmd_osinfo,
    "diskinfo": cmd_diskinfo,
    "meminfo": cmd_meminfo,
    "termuxinfo": cmd_termuxinfo,
    "whoami": cmd_whoami,
    "uptime": cmd_uptime,
    "clear": cmd_clear,
    "exit": lambda args=None: sys.exit(0)
}

# -------------------- Dependencies --------------------
def install_dependencies():
    pkgs=["nmap","curl","wget","figlet","toilet","whois","dnsutils","netcat","git","python"]
    for pkg in pkgs: check_install(pkg)

# -------------------- Main curses loop --------------------
def main_dashboard(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)  # output
    curses.init_pair(2, curses.COLOR_CYAN, -1)   # banner title
    curses.init_pair(3, curses.COLOR_YELLOW, -1) # command
    curses.init_pair(4, curses.COLOR_MAGENTA, -1) # separator

    tool_lock()
    install_dependencies()
    dash = Dashboard()
    banner(stdscr)

    while True:
        stdscr.addstr(3,0,f"{GREEN}[HCO-Terminal]> {RESET}")
        stdscr.refresh()
        curses.echo()
        try:
            cmd_input = stdscr.getstr(3,17).decode("utf-8").strip()
        except:
            continue
        curses.noecho()
        if not cmd_input: continue
        parts=cmd_input.split()
        cmd = parts[0].lower()
        args = parts[1:]
        func = COMMANDS.get(cmd, None)
        if func:
            output = func(args)
        else:
            output = f"Unknown command: {cmd}"
        dash.add_entry(cmd_input, output)
        stdscr.clear()
        banner(stdscr)
        dash.display(stdscr)

# -------------------- Dashboard Class --------------------
class Dashboard:
    def __init__(self, size=DASHBOARD_SIZE):
        self.size = size
        self.entries = []

    def add_entry(self, command, output):
        timestamp = time.strftime("%H:%M:%S")
        self.entries.append((timestamp, command, output))
        if len(self.entries) > self.size:
            self.entries.pop(0)

    def display(self, stdscr):
        row = 4
        for ts, cmd, out in self.entries:
            stdscr.addstr(row, 0, f"[{ts}] {cmd}", curses.color_pair(3))
            row += 1
            for line in out.split("\n"):
                stdscr.addstr(row, 2, line, curses.color_pair(1))
                row += 1
            row += 1
        stdscr.refresh()

# -------------------- Main --------------------
if __name__=="__main__":
    curses.wrapper(main_dashboard)
