from utils import load_config
from modes import back2back, improvvisazione, intervista

CONFIG = load_config()

def main_menu():
    while True:
        print(CONFIG["COLORS"]["title"] + "\n=== SPEAKER CHALLENGE TERMINAL ===")
        print(CONFIG["COLORS"]["menu"] + "[1] Modalità Back2Back")
        print(CONFIG["COLORS"]["menu"] + "[2] Modalità Improvvisazione")
        print(CONFIG["COLORS"]["menu"] + "[3] Modalità Intervista")
        print(CONFIG["COLORS"]["menu"] + "[Q] Esci")

        choice = input("Seleziona una modalità: ").strip().lower()

        if choice == "1":
            back2back.run(CONFIG)
        elif choice == "2":
            improvvisazione.run(CONFIG)
        elif choice == "3":
            intervista.run(CONFIG)
        elif choice == "q":
            print(CONFIG["COLORS"]["success"] + "Uscita dal programma. Ciao!")
            break
        else:
            print(CONFIG["COLORS"]["warning"] + "Scelta non valida. Riprova.\n")
