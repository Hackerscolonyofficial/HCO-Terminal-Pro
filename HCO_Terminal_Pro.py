#!/usr/bin/env python3
# HCO Terminal Pro — Advanced Ethical Hacking Terminal
# By Azhar (Hackers Colony)
# Single-file Termux interactive tool

import os, sys, platform, subprocess, time, random, curses, requests, json

# -------------------- Configuration --------------------
YOUTUBE_URL = "https://youtube.com/@hackers_colony_tech"
TOOL_LOCK_SECONDS = 10
DASHBOARD_SIZE = 12  # Number of commands to keep in dashboard
QUOTE_LIST = [
    "The quieter you become, the more you hear.",
    "Stay ethical, stay curious.",
    "Learn, Practice, Protect.",
    "Knowledge is power, hacking is skill.",
    "Scan only your own devices. Ethics first."
]
LEARNING_TOPICS = {
    "nmap": "Nmap discovers hosts and services. Use: scan <IP>",
    "ping": "Ping checks connectivity. Use: ping <host>",
    "whois": "WHOIS shows domain/IP info. Use: whois <domain/IP>",
    "dns": "DNS resolves domains. Use: dnslookup <domain>",
    "ethical": "Always get written permission before scanning.",
    "safeports": "Scan only safe ports like 22, 80, 443 for practice.",
}

SAFE_PORTS = [22, 80, 443, 8080, 8888]

# Global dashboard instance
dash = None

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
    print("This tool is locked 🔒")
    print("Only ethical usage allowed! Scan your own devices/networks.\n")
    
    # Countdown
    for i in range(TOOL_LOCK_SECONDS,0,-1):
        print(f"Redirecting to YouTube in {i} seconds...", end="\r")
        time.sleep(1)
    print("\n")
    
    # Try to open YouTube via Termux-open
    try:
        os.system(f'termux-open "{YOUTUBE_URL}"')
    except:
        print(f"Open YouTube manually: {YOUTUBE_URL}")
    
    input("Press Enter after returning from YouTube to unlock...")

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
        row = 5
        for ts, cmd, out in self.entries:
            stdscr.addstr(row, 0, f"[{ts}] {cmd}", curses.color_pair(3))
            row += 1
            for line in out.split("\n"):
                if row >= curses.LINES - 1:
                    break
                stdscr.addstr(row, 2, line, curses.color_pair(1))
                row += 1
            row += 1
            if row >= curses.LINES - 1:
                break
        stdscr.refresh()

# -------------------- Banner --------------------
def banner(stdscr):
    stdscr.addstr(0, 0, f"HCO Terminal Pro — by Azhar", curses.color_pair(2))
    stdscr.addstr(1, 0, "Ethical Hacking & Termux Learning", curses.color_pair(3))
    stdscr.addstr(2, 0, "-"*60, curses.color_pair(4))
    quote = random.choice(QUOTE_LIST)
    stdscr.addstr(3, 0, f"Quote: {quote}", curses.color_pair(1))

# -------------------- Commands --------------------
def cmd_help(args=None):
    return """
Available Commands:
scan <IP>        - nmap scan
ports <IP>       - quick TCP port check
ping <host>      - ping host
dnslookup <dom>  - DNS lookup
whois <dom/IP>   - WHOIS info
traceroute <host)- route packets
netinfo          - IP/interfaces/connections
checkurl <URL>   - HTTP headers/status
ipinfo <IP>      - Geolocation info
fetch <URL>      - Download file
banner <text>    - Print hacker banner
motd             - Quote of the day
learn <topic>    - Short ethical hacking explanation
examples         - Show ethical examples
tips             - Ethical hacking tips
safeports        - Safe ports to scan
osinfo           - OS, CPU, Python version
diskinfo         - Disk usage
meminfo          - RAM & swap
termuxinfo       - Termux environment info
whoami           - Current user & hostname
uptime           - System uptime
history          - Show command history
clear            - Clear dashboard
help             - This help
exit             - Quit
"""

def cmd_scan(args):
    if not args: return "Usage: scan <IP>"
    return run_cmd(f"nmap {args[0]} -Pn -sV")

def cmd_ports(args):
    if not args: return "Usage: ports <IP>"
    results=[]
    for port in SAFE_PORTS:
        res = run_cmd(f"nc -zv {args[0]} {port} 2>&1")
        results.append(res)
    return "\n".join(results)

def cmd_ping(args): 
    return run_cmd(f"ping -c 4 {args[0]}") if args else "Usage: ping <host>"

def cmd_dnslookup(args): 
    return run_cmd(f"nslookup {args[0]}") if args else "Usage: dnslookup <domain>"

def cmd_whois(args): 
    return run_cmd(f"whois {args[0]}") if args else "Usage: whois <domain/IP>"

def cmd_traceroute(args): 
    return run_cmd(f"traceroute {args[0]}") if args else "Usage: traceroute <host>"

def cmd_netinfo(args): 
    return run_cmd("ifconfig || ip addr")

def cmd_checkurl(args): 
    return run_cmd(f"curl -I {args[0]}") if args else "Usage: checkurl <URL>"

def cmd_ipinfo(args):
    if not args: return "Usage: ipinfo <IP>"
    try:
        res = requests.get(f"https://ipinfo.io/{args[0]}/json", timeout=5)
        data = res.json()
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Failed to fetch IP info: {str(e)}"

def cmd_fetch(args): 
    return run_cmd(f"curl -O {args[0]}") if args else "Usage: fetch <URL>"

def cmd_banner(args): 
    if not args: return "Usage: banner <text>"
    text=" ".join(args)
    if run_cmd("which toilet") != "": 
        os.system(f'toilet -f mono12 -F metal "{text}"')
    elif run_cmd("which figlet") != "": 
        os.system(f'figlet "{text}"')
    else: 
        return "Install toilet or figlet to use banner"
    return "Banner displayed"

def cmd_motd(args=None): 
    return random.choice(QUOTE_LIST)

def cmd_learn(args): 
    if not args: return "Usage: learn <topic>"
    return LEARNING_TOPICS.get(args[0].lower(), "No info for this topic")

def cmd_examples(args=None):
    return "Example usage:\nscan 192.168.1.1\nports 192.168.1.1\nping 8.8.8.8\nfetch https://example.com/file.txt"

def cmd_tips(args=None):
    return "Tips:\n- Always scan your own devices.\n- Never misuse commands.\n- Practice in labs.\n- Document responsibly."

def cmd_safeports(args=None): 
    return f"Safe ports: {', '.join(map(str, SAFE_PORTS))}"

def cmd_osinfo(args=None): 
    return f"OS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}\nMachine: {platform.machine()}"

def cmd_diskinfo(args=None): 
    return run_cmd("df -h")

def cmd_meminfo(args=None): 
    return run_cmd("free -h")

def cmd_termuxinfo(args=None): 
    return f"HOME={os.environ.get('HOME','N/A')}\nPATH={os.environ.get('PATH','N/A')}"

def cmd_whoami(args=None): 
    return f"User: {run_cmd('whoami')} | Host: {run_cmd('hostname')}"

def cmd_uptime(args=None): 
    return run_cmd("uptime")

def cmd_clear(args=None): 
    return "clear"

def cmd_history(args=None): 
    return "\n".join([f"{i+1}. {c[1]}" for i,c in enumerate(dash.entries)])

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
    "history": cmd_history,
    "exit": lambda args=None: sys.exit(0)
}

# -------------------- Dependencies --------------------
def install_dependencies():
    pkgs=["nmap","curl","wget","figlet","toilet","whois","dnsutils","netcat","git","python"]
    for pkg in pkgs: 
        check_install(pkg)

# -------------------- Main curses loop --------------------
def main_dashboard(stdscr):
    global dash
    dash = Dashboard()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # output
    curses.init_pair(2, curses.COLOR_CYAN, -1)    # banner title
    curses.init_pair(3, curses.COLOR_YELLOW, -1)  # command
    curses.init_pair(4, curses.COLOR_MAGENTA, -1) # separator

    banner(stdscr)

    while True:
        stdscr.addstr(4, 0, "[HCO-Terminal]> ", curses.color_pair(1))
        stdscr.refresh()
        curses.echo()
        try:
            cmd_input = stdscr.getstr(4, 17).decode("utf-8").strip()
        except:
            continue
        curses.noecho()
        if not cmd_input: 
            continue
        parts = cmd_input.split()
        cmd = parts[0].lower()
        args = parts[1:]
        func = COMMANDS.get(cmd, None)
        if func:
            try:
                output = func(args)
            except Exception as e:
                output = f"Error executing command: {str(e)}"
        else:
            output = f"Unknown command: {cmd}"
            
        if output == "clear":
            stdscr.clear()
            dash.entries.clear()
            banner(stdscr)
        else:
            dash.add_entry(cmd_input, output)
            stdscr.clear()
            banner(stdscr)
            dash.display(stdscr)

# -------------------- Main --------------------
if __name__ == "__main__":
    tool_lock()            # Tool lock + YouTube redirect
    install_dependencies()  # Ensure all packages installed
    curses.wrapper(main_dashboard)
