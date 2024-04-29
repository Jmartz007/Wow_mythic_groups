import logging.handlers
from dotenv import load_dotenv
load_dotenv()
import logging
import graypy

from website import app

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)-5s] [%(module)s]-%(funcName)s: %(message)s', datefmt='%b/%d/%y %I:%M:%S %p')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

socket_handler = graypy.GELFTCPHandler(host="localhost", port=5555)
socket_handler.setLevel(logging.DEBUG)
socket_handler.setFormatter(formatter)
logger.addHandler(socket_handler)

logger.info("STARTED APP ----------")
logger.debug("DEBUG MESSAGE")
logger.debug("ANOTHER DEBUG MESSAGE -----------")

app = app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
