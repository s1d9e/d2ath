STYLES = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
    "inverse": "\033[7m",
}

BG_COLORS = {
    "black": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
}

BG_STRONG = {
    "black": "\033[100m",
    "red": "\033[101m",
    "green": "\033[102m",
    "yellow": "\033[103m",
    "blue": "\033[104m",
    "magenta": "\033[105m",
    "cyan": "\033[106m",
    "white": "\033[107m",
}

FG_DARK = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

FG_STRONG = {
    "white": "\033[90m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}

R = "\033[0m"


def section(title):
    print(f"{BG_STRONG['red']}{FG_DARK['yellow']} {title} {R}")


def demo():
    section("STYLES")
    print(f"{STYLES['reset']}Reset")
    print(f"{STYLES['bold']}Bold{R}")
    print(f"{STYLES['underline']}Underline{R}")
    print(f"{STYLES['inverse']}Inverse{R}")
    print()

    section("NORMAL BACKGROUND COLORS")
    for name, code in BG_COLORS.items():
        print(f"{code}{name}{R}" + (" (white)" if name == "white" else ""))
    print()

    section("STRONG BACKGROUND COLORS")
    for name, code in BG_STRONG.items():
        print(f"{code}{name}{R}")
    print()

    section("DARK FOREGROUND COLORS")
    for name, code in FG_DARK.items():
        suffix = " (black)" if name == "black" else ""
        print(f"{code}{name}{R}{suffix}")
    print()

    section("STRONG FOREGROUND COLORS")
    for name, code in FG_STRONG.items():
        print(f"{code}{name}{R}")
    print()

    section("NORMAL FOREGROUND COLORS")
    for name, code in FG_DARK.items():
        suffix = " (black)" if name == "black" else ""
        print(f"{code}{name}{R}{suffix}")
    print()

    section("COMBINATIONS")
    print(f"{FG_DARK['red']}red foreground color{R}")
    print(f"{STYLES['inverse']}inverse foreground <-> background{R}")
    print(f"{STYLES['inverse']}{FG_DARK['red']}inverse red foreground color{R}")
    print(f"{STYLES['inverse']}before {FG_DARK['red']}nested{R}")
    print(f"{FG_DARK['red']}before {STYLES['inverse']}nested{R}")

    input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    demo()
