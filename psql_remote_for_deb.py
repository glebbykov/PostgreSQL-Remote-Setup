import argparse
import logging
import json
from fabric import Connection

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def install_postgres(c, version='13'):
    try:
        c.run('sudo apt-get update')
        c.run(f'sudo apt-get install -y postgresql-{version}')
        logging.info(f'Successfully installed PostgreSQL version {version}')
    except:
        logging.error('Failed to install PostgreSQL')

def create_user(c, username, password):
    try:
        c.run(f'sudo -u postgres createuser {username}')
        c.run("sudo -u postgres psql -c \"ALTER USER {} WITH ENCRYPTED PASSWORD '{}';\"".format(username, password))
        logging.info(f'Successfully created user {username}')
    except:
        logging.error(f'Failed to create user {username}')

def create_database(c, dbname, owner):
    try:
        c.run(f'sudo -u postgres createdb {dbname} -O {owner}')
        logging.info(f'Successfully created database {dbname}')
    except:
        logging.error(f'Failed to create database {dbname}')

def setup_remote_postgres(input_data):
    host = input_data['host']
    user = input_data['user']
    version = input_data.get('version', 'latest')
    user_name = input_data.get('user_name', 'newuser')
    user_password = input_data.get('user_password', 'newpassword')
    db_name = input_data.get('db_name', 'newdb')
    try:
        with Connection(host, user) as c:
            install_postgres(c, version)
            create_user(c, user_name, user_password)
            create_database(c, db_name, user_name)
    except Exception as e:
        logging.error(f'Failed to setup remote PostgreSQL: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup remote PostgreSQL')
    parser.add_argument('input_file', help='Input JSON file')
    args = parser.parse_args()


    with open(args.input_file) as f:
        input_data = json.load(f)

    setup_remote_postgres(input_data)
