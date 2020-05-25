import os
import pytest
import tempfile

from gtfslib.dao import Dao


@pytest.fixture
def dao_fixture() -> Dao:
    with tempfile.TemporaryDirectory() as tmpdirname:
        sql_logging = False
        database_path = os.path.join(tmpdirname, "gtfs.sqlite")
        yield Dao(database_path, sql_logging=sql_logging)
