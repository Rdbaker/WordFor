#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
from flask_script.commands import Clean, ShowUrls

from wordfor.app import create_app
from wordfor.database import db
from wordfor.settings import DevConfig, ProdConfig, TestConfig
import wordfor.models as models

ENV_CONFIG_MAP = {
    'prd': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig
}
CONFIG = ENV_CONFIG_MAP[os.environ.get('WORDFOR_ENV', 'dev')]
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')
CREATE_DB = 'create database %s'
DEFAULT_DB = 'postgres'

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and
    models by default."""
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@manager.command
def ingest():
    """Ingest data from remote sources."""
    from wordfor.ingest.oxford_learner import OxfordLearnerSource
    ol_src = OxfordLearnerSource()
    ol_src.run()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
