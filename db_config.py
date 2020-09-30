#!/usr/bin/python3

from configparser import ConfigParser


def config(filename=r'./database.ini', section='parameters'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}.')

    return db

