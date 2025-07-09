import os
import tempfile
import pytest
import glob

@pytest.fixture(scope="session", autouse=True)
def clean_test_db():
    # Create temp file for db path
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test_user_vars")

    # Set the env var for db path
    os.environ["CPY_DP_PATH"] = db_path

    # Ensure no previous dbm files exist
    for path in glob.glob(db_path + "*"):
        os.remove(path)

    yield # Run tests

    # Remove dbm files
    for path in glob.glob(db_path + "*"):
        os.remove(path)
