import os
os.environ["INSTANCE_CONNECTION_NAME"] = "wowmythicgroups:us-west3:myth-db"
os.environ["DB_USER"] = "programuser"
os.environ["DB_PASS"] = "123456"
os.environ["DB_NAME"] = "wowmythics"

from website import init_connection_pool
from website import app



db = init_connection_pool()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)