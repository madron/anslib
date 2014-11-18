#!/usr/bin/env python

import argparse
import os
import psycopg2



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load random binary data.')
    parser.add_argument('files', metavar='N', type=int, nargs='?', default=1,
                       help='Number of 1 MB random files to load')

    kwargs = vars(parser.parse_args())

    conn = psycopg2.connect(database='test')
    cursor = conn.cursor()
    for i in range(kwargs['files']):
        print 'Loading file:', i
        cursor.execute("INSERT INTO bytea (bytea) VALUES (%s);" % psycopg2.Binary(os.urandom(1024*1024)))
