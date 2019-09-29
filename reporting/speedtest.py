import sys

import yaml
import json

from speedtest import Speedtest
from mysql import connector as mysql


def main():
    upload, download, server = get_speeds()
    record_results(upload, download, server)


def get_speeds():
    s = Speedtest()
    s.get_servers()
    server = json.dumps(s.get_best_server())
    upload = s.upload()
    download = s.download()
    return upload, download, server


def record_results(upload, download, server):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO hist.internet_speed_test
        (test_ts, upload_speed, download_speed, test_server) VALUES
        (CURRENT_TIMESTAMP, %(upload)s, %(download)s, %(server)s);
    """
    cursor.execute(query, {
        'upload': upload,
        'download': download,
        'server': server
    })
    conn.commit()
    cursor.close()
    conn.close()


def get_mysql_connection():
    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return mysql.connect(**config['database'])


if __name__ == '__main__':
    main()
