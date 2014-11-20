#!/usr/bin/env python

import argparse
import os
import psycopg2
import random
import string


def run(**kwargs):
    COMMAND = dict(
        insert=insert,
        update=update,
        delete=delete,
    )
    command = kwargs['command']
    connection = psycopg2.connect(database='test')
    COMMAND[command](connection, **kwargs)
    connection.commit()
    connection.close()


def insert(connection, table=None, files=1, **kwargs):
    cursor = connection.cursor()
    for i in range(files):
        print 'Loading file:', i + 1
        data = get_random_data(table)
        if table == 'lobj':
            obj = connection.lobject()
            obj.write(get_random_data(table))
            data = obj.oid
        sql = 'INSERT INTO %s ' % table
        cursor.execute(sql + "(data) VALUES (%s);", (data,))


def update(connection, table=None, id=1, **kwargs):
    cursor = connection.cursor()
    print 'Updating id', id
    if table == 'lobj':
        cursor.execute("SELECT data FROM lobj WHERE id = %s;", (id,))
        result = cursor.fetchone()
        if result:
            oid = result[0]
            obj = connection.lobject(oid, 'wb')
            obj.truncate()
            obj.write(get_random_data(table))
    else:
        sql = 'UPDATE %s ' % table
        cursor.execute(sql + "SET data = %s WHERE id = %s;", (get_random_data(table), id))


def delete(connection, table=None, id=1, **kwargs):
    cursor = connection.cursor()
    print 'Deleting id', id
    if table == 'lobj':
        cursor.execute("SELECT data FROM lobj WHERE id = %s;", (id,))
        result = cursor.fetchone()
        if result:
            oid = result[0]
            connection.lobject(oid).unlink()
    sql = 'DELETE FROM %s ' % table
    cursor.execute(sql + "WHERE id = %s;", (id,))


def get_random_data(table):
    size = 1024*1024
    if table == 'text':
        return ''.join(random.choice(string.printable) for _ in range(size))
    if table == 'bytea':
        return psycopg2.Binary(os.urandom(size))
    if table == 'lobj':
        return os.urandom(size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load random binary data.')
    parser.add_argument('table', metavar='TABLE', type=str,
        choices=['text', 'bytea', 'lobj'], help='Table')
    parser.add_argument('command', metavar='COMMAND', type=str,
        choices=['insert', 'update', 'delete'], help='Command to execute')
    parser.add_argument('--files', metavar='FILES', type=int, nargs='?', default=1,
       help='Number of 1 MB random files')
    parser.add_argument('--id', metavar='ID', type=int, nargs='?', default=1,
       help='Record id to delete')

    kwargs = vars(parser.parse_args())
    run(**kwargs)
