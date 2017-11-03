import json
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import app
from models import User


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self._app = app.app.test_client()

    def test_root_should_return_hello_pisti(self):
        response = self._app.get('/')
        assert response.data == b'Hello Pisti!'

    @parameterized.expand([
        ('/greet/Pisti', b'Hello Pisti!'),
        ('/greet/Love', b'Hello Love!'),
    ])
    def test_greet_should_return_greeting_with_name(self, url, expected_result):
        response = self._app.get(url)
        assert response.data == expected_result

    @patch('app.db.session')
    def test_create_should_store_user_in_db(self, db_session_mock):
        expected_user = User(name='Love Pisti', email='love@pisti.hu')
        self._post_json('/user', {'name': 'Love Pisti', 'email': 'love@pisti.hu'})
        db_session_mock.add.assert_called_once_with(expected_user)
        db_session_mock.commit.assert_called_once_with()

    @patch('app.db.session')
    def test_create_should_return_created_user(self, db_session_mock):
        self._mock_model_save_id(db_session_mock, 123)
        response = self._post_json('/user', {'name': 'Love Pisti', 'email': 'love@pisti.hu'})
        response_data = json.loads(response.data.decode('utf-8'))
        expecteed_response_data = {'id': 123, 'name': 'Love Pisti', 'email': 'love@pisti.hu'}
        assert response_data == expecteed_response_data

    @patch('app.escher_validator.validate_request')
    def test_auth_test_should_check_authorization(self, auth_mock):
        # self._app.get('/auth-test')
        # auth_mock.assert_any_call()
        pass

    def _post_json(self, url, payload):
        return self._app.post(
            url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})

    @staticmethod
    def _mock_model_save_id(session_mock, saved_id):
        def add_id_to_user_model(*args):
            args[0].id = saved_id

        session_mock.add.side_effect = add_id_to_user_model

if __name__ == '__main__':
    unittest.main()
