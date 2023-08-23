from dotenv import load_dotenv
load_dotenv()

from website import app

# db = init_connection_pool()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
