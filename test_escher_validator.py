import unittest
from unittest.mock import Mock, patch
import app
import escher_validator
from escherauth_go.escher_validator import EscherValidatorError


class EscherValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self._request_mock = self._mock_request()
        self._escher_validator_mock = self._mock_escher_validator()
        self._action_mock = Mock()
        self._subject = escher_validator.validate_request

    def test_validate_request_should_escher_validate_the_request(self):
        self._subject(self._request_mock)
        self._escher_validator_mock.assert_called_once_with(
            'POST',
            '/test-url?with=params',
            'TEST BODY',
            {'Host': 'test.host'})

    def test_validate_request_should_escher_validate_the_request_without_params(self):
        self._request_mock.url = 'https://test.host/test-url'
        self._request_mock.method = 'GET'
        self._request_mock.data = b''

        self._subject(self._request_mock)

        self._escher_validator_mock.assert_called_once_with(
            'GET',
            '/test-url',
            '',
            {'Host': 'test.host'})

    def test_validate_request_should_reise_validation_error_on_validation_failed(self):
        self._escher_validator_mock.side_effect = EscherValidatorError('Validation failed')
        with self.assertRaises(escher_validator.ValidationError):
            self._subject(self._request_mock)

    def _mock_request(self):
        request_mock = Mock()
        request_mock.url = 'https://test.host/test-url?with=params'
        request_mock.method = 'POST'
        request_mock.data = b'TEST BODY'
        request_mock.headers = {'Host': 'test.host'}

        return request_mock

    def _mock_escher_validator(self):
        escher_validator_patcher = patch('escher_validator.EscherValidator.validateRequest')
        escher_validator_mock = escher_validator_patcher.start()
        self.addCleanup(escher_validator_patcher.stop)

        return escher_validator_mock
