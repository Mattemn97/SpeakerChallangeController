import colorama

colorama.init(autoreset=True)

COLOR_MAP = {
    "black": colorama.Fore.BLACK,
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "yellow": colorama.Fore.YELLOW,
    "blue": colorama.Fore.BLUE,
    "magenta": colorama.Fore.MAGENTA,
    "cyan": colorama.Fore.CYAN,
    "white": colorama.Fore.WHITE,
}

def load_config(file_path="config.txt"):
    config = {
        "COLORS": {}
    }
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip()

                    if key.startswith("COLOR_"):
                        config["COLORS"][key.replace("COLOR_", "").lower()] = COLOR_MAP.get(value.lower(), "")

                    elif key.endswith("_FOLDER") or key.endswith("_FILE"):
                        config[key] = str(value)
                    
                    elif key.endswith("VOL_AUDIO"):
                        config[key] = float(value)

                    else:
                        config[key] = int(value)
                        
    except FileNotFoundError:
        print("File di configurazione non trovato, uso valori di default.")
    return config
