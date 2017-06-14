#!/usr/bin/env python
"""
Module for dealing with postgres database tables.
"""
__author__ = "Alex Drlica-Wagner"
import os
from os.path import dirname, abspath
import logging
import tempfile
from collections import OrderedDict as odict
import copy
import getpass

import numpy as np
import pandas as pd
import yaml
import dateutil.parser
import datetime
import fitsio
import healpy
import numpy.lib.recfunctions as recfn

from lvdb.database import Database

class Table(object):
    """Base class for postgres table objects."""
    _filename  = os.path.join(get_datadir(),'tables.yaml')
    _section   = None
    
    def __init__(self,config=None,section=None):
        if config is None: config = self._filename
        if section is None: section = self._section
        self.db = Database()
        self.load_config(config,section)

    def load_config(self,config, section=None):
        if config is None: return config

        if isinstance(config,basestring):
            logging.debug("Loading configuration file: %s..."%config)
            config = yaml.load(open(config,'r'))
        elif isinstance(config,dict):
            config = copy.deepcopy(config)
        else:
            msg = "Unrecognized type for table configuration: %s"
            raise TypeError(msg)

        if section is None:
            self.config = config
        else:
            self.config = config[section]
        self.tablename = self.config['table']

        # Check the config
        self.check_config()

        return config

    def check_config(self):
        assert 'columns' in self.config

        # Check that the columns match
        if self.exists():
            cfgcol = sorted(map(str.upper,self.config['columns'].keys()))
            dbcol = sorted(map(str.upper,self.get_columns()))
            if not np.all(cfgcol==dbcol):
                msg = "Config columns do not match database."
                raise ValueError(msg)

    def exists(self):
        return self.db.table_exists(self.tablename)
        
    def get_columns(self):
        query = "select * from %s limit 0;"%self.tablename
        return self.db.get_columns(query)

    def create_table(self):
        return self.db.create_table(**self.config)

    def drop_table(self):
        self.db.drop_table(self.tablename)

    def grant_table(self):
        query = "grant select on %s to public;"%self.tablename
        self.db.execute(query)

    def create_indexes(self):
        self.db.create_indexes(**self.config)
        
    def build_table(self,force=True):
        if force: self.drop_table()
        self.create_table()
        self.create_indexes()
        self.grant_table()

    def load_table(self,data,option=None):
        self.db.load_data(self.tablename,data,option)

    def get_description(self):
        return self.db.get_description("select * from %s limit 0;"%self.tablename)

    def get_dtypes(self):
        return self.db.get_dtypes("select * from %s limit 0;"%self.tablename)

