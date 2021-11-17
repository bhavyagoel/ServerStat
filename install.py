import hashlib
import argparse
import pymongo

data = {}


def init_mongo(**kwargs):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[kwargs['db']]
    data['db'] = kwargs['db']
    return db


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help='Enter the key')
    parser.add_argument('-db', help='Enter the Database name')
    return parser


def get_key(**kwargs):
    hs = hashlib.sha256(kwargs['key'].encode('utf-8')).hexdigest()
    data['hash'] = hs
    return hs


def dump(**kwargs):
    get_key(**kwargs)
    db = init_mongo(**kwargs)
    db.data.insert_one(data)


def main():
    parser = init_parser()
    args = parser.parse_args()
    dump(**vars(args))


if __name__ == '__main__':
    main()
