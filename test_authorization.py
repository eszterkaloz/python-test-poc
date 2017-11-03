import unittest
from unittest.mock import Mock, patch
import app
import authorization


class EscherAuthTestCase(unittest.TestCase):

    def setUp(self):
        self._validator_mock = Mock()
        self._action_mock = Mock()
        self._subject = authorization.authorize(self._validator_mock)(self._action_mock)

    def test_wrapper_should_call_original_action(self):
        self._subject()
        self._action_mock.assert_called_once_with()

    def test_wrapper_should_call_original_action_with_aruments(self):
        self._subject("arg1")
        self._action_mock.assert_called_once_with("arg1")

    def test_wrapper_should_return_the_action_result(self):
        self._action_mock.return_value = 'TEST RESPONSE'
        response = self._subject()
        assert response == 'TEST RESPONSE'

    # def test_wrapper_should_respond_with_401_on_validation_error(self):
    #     self._escher_validator_mock.side_effect = EscherValidatorError('Validation failed')
    #     response = self._subject()
    #     assert response.status_code == 401
    #     assert response.data == b'Authorization required'