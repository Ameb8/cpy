import pytest
import logging

@pytest.fixture(autouse=True)
def debug(request):
    logging.getLogger().setLevel(logging.DEBUG)

