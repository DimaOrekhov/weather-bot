def get_token() -> str:
    with open("../tg_token.txt") as istream:
        return istream.read()


API_KEY = get_token()
