"""The test suit for console mod."""

from unittest.mock import Mock

from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern import console


@pytest.fixture
def runner() -> CliRunner:
    """Runner fixture."""
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    """Mock random page wikipedia."""
    return mocker.patch("hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exits with a status code of zero in production."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It returns a title."""
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It invokes requests get."""
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits call to en.wikipedia.org."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """It calls with passed parameter language."""
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It fails on request error."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It prints message on request error."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
