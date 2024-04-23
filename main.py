from dotenv import load_dotenv
load_dotenv()
import logging

from website import app

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)-5s] [%(module)s]-%(funcName)s: %(message)s', datefmt='%b/%d/%y %I:%M:%S %p')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.info("STARTED APP ----------")

app = app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
