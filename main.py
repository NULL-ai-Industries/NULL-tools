import os
import sys
import time
import random
import platform
import socket
import shutil
import subprocess
import threading
from datetime import datetime

# ==========================================
#              NULL SYSTEM V3.0
# ==========================================

VERSION = "3.0"
USERNAME = "UNKNOWN"


# ==========================================
#              RED COLOUR ENGINE
# ==========================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[38;5;196m"
DARK_RED = "\033[38;5;88m"
NEON = "\033[38;5;203m"
WHITE = "\033[97m"
ORANGE = "\033[38;5;208m"
CYAN = "\033[38;5;210m"
GREY = "\033[38;5;245m"
PURPLE = "\033[38;5;160m"

GREEN = RED
DARK_GREEN = DARK_RED

# ==========================================
#              CONFIGURATION
# ==========================================

DEV = True
FAST_BOOT = False

history = []


# ==========================================
#              TERMINAL UTILITIES
# ==========================================

def clear():
    os.system("clear")


def hide_cursor():
    print("\033[?25l", end="", flush=True)


def show_cursor():
    print("\033[?25h", end="", flush=True)


def slowprint(text, delay=0.02, colour=GREEN):

    for char in text:
        print(colour + char + RESET, end="", flush=True)
        time.sleep(delay)

    print()


def line(length=65, colour=DARK_GREEN):

    print(colour + "━" * length + RESET)


def log(message, state="OK"):

    timestamp = datetime.now().strftime("%H:%M:%S")

    colours = {
        "OK": GREEN,
        "WARN": ORANGE,
        "ERROR": RED,
        "INFO": CYAN,
        "SYSTEM": PURPLE
    }

    colour = colours.get(state, GREEN)

    print(
        f"{GREY}[{timestamp}]{RESET} "
        f"{colour}[{state}]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def progress(message, duration=1.5):

    print(f"\n{NEON}{message}{RESET}")

    width = 35
    steps = 35

    for i in range(steps + 1):

        percent = int(i / steps * 100)

        filled = "█" * i
        empty = "░" * (width - i)

        print(
            f"\r{DARK_GREEN}[{NEON}{filled}{RESET}"
            f"{DARK_GREEN}{empty}]{RESET} "
            f"{WHITE}{percent:3}%{RESET}",
            end="",
            flush=True
        )

        time.sleep(duration / steps)

    print("\n")


# ==========================================
#              MATRIX EFFECT
# ==========================================

def matrix_rain(duration=3):

    characters = "01アイウエオカキクケコサシスセソ"

    width = shutil.get_terminal_size((80, 24)).columns

    end_time = time.time() + duration

    hide_cursor()

    try:
        while time.time() < end_time:

            row = ""

            for _ in range(width):

                if random.random() < 0.18:
                    row += random.choice(characters)
                else:
                    row += " "

            print(DARK_GREEN + row + RESET)

            time.sleep(0.045)

    finally:
        show_cursor()


# ==========================================
#              NULL LOGO
# ==========================================

def logo():

    print(NEON + BOLD + r"""
███╗   ██╗██╗   ██╗██╗     ██╗
████╗  ██║██║   ██║██║     ██║
██╔██╗ ██║██║   ██║██║     ██║
██║╚██╗██║██║   ██║██║     ██║
██║ ╚████║╚██████╔╝███████╗████████╗
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═══════╝
""" + RESET)

    print(GREEN + "       N E U R A L   S Y S T E M" + RESET)
    print(GREY + "       NULL CORE // VERSION " + VERSION + RESET)


# ==========================================
#              SYSTEM INFORMATION
# ==========================================

def system_info():

    print()

    log("COLLECTING SYSTEM INFORMATION", "INFO")

    print(f"{GREEN}OS:           {WHITE}{platform.system()}")
    print(f"{GREEN}OS VERSION:   {WHITE}{platform.release()}")
    print(f"{GREEN}ARCHITECTURE: {WHITE}{platform.machine()}")
    print(f"{GREEN}PROCESSOR:    {WHITE}{platform.processor()}")
    print(f"{GREEN}PYTHON:       {WHITE}{platform.python_version()}")

    print(f"{GREEN}HOSTNAME:     {WHITE}{socket.gethostname()}")

    line()


# ==========================================
#              RESOURCE MONITOR
# ==========================================

def resource_monitor():

    print()

    try:
        import psutil

        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()

        print(f"{GREEN}CPU USAGE: {WHITE}{cpu}%")
        print(f"{GREEN}RAM USAGE: {WHITE}{memory.percent}%")
        print(
            f"{GREEN}RAM TOTAL: {WHITE}"
            f"{memory.total / (1024 ** 3):.2f} GB"
        )

        battery = psutil.sensors_battery()

        if battery:
            print(
                f"{GREEN}BATTERY:   {WHITE}"
                f"{battery.percent}%"
            )

    except ImportError:

        log("Install psutil for extended monitoring.", "WARN")

    line()


# ==========================================
#              NETWORK CHECK
# ==========================================

def network_check():

    print()

    log("CHECKING NETWORK CONNECTIVITY", "INFO")

    try:

        start = time.perf_counter()

        with socket.create_connection(
            ("1.1.1.1", 53),
            timeout=3
        ):

            elapsed = (time.perf_counter() - start) * 1000

            log("Internet connectivity available")

            print(
                f"{GREEN}CONNECTION TIME: "
                f"{WHITE}{elapsed:.2f} ms"
            )

    except OSError:

        log("Network connection unavailable", "WARN")

    line()


# ==========================================
#              SYSTEM SCAN
# ==========================================

def scan():

    line()

    slowprint(
        "[NULL] INITIATING LOCAL SYSTEM SCAN...",
        0.025,
        NEON
    )

    progress("READING SYSTEM INFORMATION", 1.5)

    system_info()

    progress("ANALYSING SYSTEM RESOURCES", 1)

    resource_monitor()

    log("LOCAL SCAN COMPLETE")

    line()


# ==========================================
#              NETWORK TOOL
# ==========================================

def network():

    line()

    network_check()

    line()


# ==========================================
#              TRACKER
# ==========================================

def tracker():

    line()

    log("INITIALISING LOCAL SYSTEM MONITOR", "INFO")

    resource_monitor()

    log("MONITORING COMPLETE")

    line()


# ==========================================
#              HELP
# ==========================================

def help_menu():

    line()

    print(NEON + BOLD + "NULL COMMAND DIRECTORY" + RESET)

    commands = [
        ("help", "Display available commands"),
        ("scan", "Scan local system information"),
        ("network", "Check internet connectivity"),
        ("track", "Display resource information"),
        ("system", "Display system specifications"),
        ("clear", "Clear terminal"),
        ("history", "Display command history"),
        ("exit", "Terminate NULL")
    ]

    for command, description in commands:

        print(
            f"{GREEN}{command.ljust(12)}"
            f"{WHITE}{description}"
        )

    line()


# ==========================================
#              COMMAND PARSER
# ==========================================

def command_parser(command):

    command = command.lower().strip()

    history.append(command)

    if command == "help":
        help_menu()

    elif command == "scan":
        scan()

    elif command == "network":
        network()

    elif command == "track":
        tracker()

    elif command == "system":
        system_info()

    elif command == "clear":

        clear()
        logo()

    elif command == "history":

        line()

        for index, item in enumerate(history, 1):
            print(f"{GREY}{index:03} {GREEN}{item}")

        line()

    elif command in ("exit", "quit"):

        shutdown()

    elif command == "":

        pass

    else:

        log(f"UNKNOWN COMMAND: {command}", "ERROR")
        log("Type 'help' for available commands.", "INFO")


# ==========================================
#              SHUTDOWN
# ==========================================

def shutdown():

    print()

    progress("TERMINATING NULL SESSION", 1.5)

    slowprint("SESSION TERMINATED.", 0.04, RED)

    show_cursor()

    sys.exit(0)


# ==========================================
#              STARTUP SEQUENCE
# ==========================================

def startup():

    clear()

    if not FAST_BOOT:

        matrix_rain(2.5)

    clear()

    logo()

    line()

    print()

    boot_messages = [
        "Loading NULL kernel...",
        "Initialising core modules...",
        "Loading encryption services...",
        "Verifying system integrity...",
        "Initialising command interface...",
        "Preparing user environment..."
    ]

    for message in boot_messages:

        time.sleep(0.25)

        log(message, "SYSTEM")

    print()

    progress("INITIALISING NULL CORE", 1.8)

    log("SYSTEM INITIALISATION COMPLETE")

    line()

    print()

    slowprint("WELCOME TO NULL.", 0.06, NEON)

    print()

    connect = input(
        f"{CYAN}Connect to network? [Y/N]: {WHITE}"
    ).strip().lower()

    if connect in ("y", "yes"):

        network_check()

    else:

        log("Continuing in offline mode.", "WARN")

    line()


# ==========================================
#              USER SESSION
# ==========================================

def user_session():

    global USERNAME

    USERNAME = input(
        f"\n{ORANGE}IDENTIFY YOURSELF: {WHITE}"
    ).strip()

    if not USERNAME:
        USERNAME = "USER"

    print()

    slowprint(
        f"IDENTITY ACCEPTED. WELCOME, {USERNAME.upper()}.",
        0.035,
        NEON
    )

    progress("LOADING COMMAND ENVIRONMENT", 1)


# ==========================================
#              MAIN
# ==========================================

def main():

    try:

        startup()

        user_session()

        while True:

            print()

            command = input(
                f"{DARK_GREEN}┌──("
                f"{NEON}{USERNAME}@NULL"
                f"{DARK_GREEN})\n"
                f"└─{NEON}$ {WHITE}"
            )

            command_parser(command)

    except KeyboardInterrupt:

        shutdown()

    finally:

        show_cursor()


if __name__ == "__main__":

    main()
