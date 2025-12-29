from src.config import get_settings


def main():
    settings = get_settings()

    print(f"Connecting to {settings.db.name}")

















if __name__ == "__main__":
    main()