import os
import pytest
import tempfile

from gtfslib.dao import Dao


@pytest.fixture(scope="session")
def dao_fixture() -> Dao:
    dao = Dao()
    yield dao
