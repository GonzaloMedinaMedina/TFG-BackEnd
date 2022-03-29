from distutils.log import debug
import sys
import pytest
sys.path.append("../TFG-BACKEND/")
from tweetevalController import create_app

app = create_app(False)

@pytest.fixture()
def app():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner():
    return app.test_cli_runner()



#python -m pytest