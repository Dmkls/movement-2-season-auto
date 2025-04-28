PROXIES_PATH = "./data/proxies.txt"
TOKENS_PATH = "./data/tokens.txt"

def read_file(path: str, add=""):
    with open(path, encoding='utf-8') as file:
        return [f"{add}{line.strip()}" for line in file]

def read_proxies() -> list[str]:
    return read_file(PROXIES_PATH, add="http://")

def read_tokens() -> list[str]:
    return read_file(TOKENS_PATH, add="Bearer ")