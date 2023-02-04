import argparse
import logging
from fabric import Connection

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def install_postgres(c, version='latest'):
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

def setup_remote_postgres(host, user, password, user_name, user_password, db_name, version='latest'):
    try:
        with Connection(host, user=user, connect_kwargs={"password": password}) as c:
            install_postgres(c, version)
            create_user(c, user_name, user_password)
            create_database(c, db_name, user_name)
    except Exception as e:
        logging.error(f'Failed to setup remote PostgreSQL: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup remote PostgreSQL')
    parser.add_argument('host', help='Remote host address')
    parser.add_argument('user', help='Remote host username')
    parser.add_argument('password', help='Remote host password')
    parser.add_argument('--version', help='PostgreSQL version to install', default='13')
    parser.add_argument('--user_name', help='PostgreSQL user name', default='newuser')
    parser.add_argument('--user_password', help='PostgreSQL user password', default='newpassword')
    parser.add_argument('--db_name', help='PostgreSQL db name', default='newdb')
    args = parser.parse_args()

    setup_remote_postgres(args.host, args.user, args.password, args.user_name, args.user_password, args.db_name, args.version)
