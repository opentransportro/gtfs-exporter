import os
import pytest
import tempfile

from exporter.gtfs.dao import Dao


@pytest.fixture(scope="session")
def dao_fixture() -> Dao:
    dao = Dao()
    yield dao
