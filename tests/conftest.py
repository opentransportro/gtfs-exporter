import os
import pytest
import tempfile

from gtfslib.dao import Dao


@pytest.fixture
def dao_fixture() -> Dao:
    dao = Dao()
    yield dao
