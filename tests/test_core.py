import pytest
from unittest.mock import patch, MagicMock
from nmcli import core


def test_validate_host_valid():
    from nmcli.utils import validate_host
    assert validate_host("google.com") is True


def test_validate_host_invalid():
    from nmcli.utils import validate_host
    assert validate_host("thishostdoesnotexist.invalid") is False


def test_port_scan_returns_dict():
    result = core.port_scan("127.0.0.1", ports=[80, 443])
    assert "open" in result
    assert "closed" in result


def test_dns_lookup_returns_dict():
    result = core.dns_lookup("google.com")
    assert isinstance(result, dict)
    assert "A" in result


@patch("nmcli.aws.boto3.client")
def test_get_vpc_info_no_credentials(mock_client):
    from botocore.exceptions import NoCredentialsError
    mock_client.side_effect = NoCredentialsError()
    from nmcli import aws
    result = aws.get_vpc_info()
    assert result == []
