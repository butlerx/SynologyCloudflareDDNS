"""Tests for both log formats, including fields passed via extra=."""

import json
import logging

import pytest

from synology_cloudflare_ddns.utils.logger import get_logger, setup_logger


@pytest.mark.parametrize("log_format", ["kv", "json"])
def test_logs_extra_fields(log_format: str, capsys: pytest.CaptureFixture) -> None:
    setup_logger(logging.INFO, log_format=log_format)
    get_logger("t").info("DNS record updated", extra={"dns_name": "nas.example.com", "note": 'say "hi"'})
    err = capsys.readouterr().err.strip()
    if log_format == "json":
        line = json.loads(err)
        assert line["message"] == "DNS record updated"
        assert line["dns_name"] == "nas.example.com"
    else:
        assert "DNS record updated" in err
        assert "dns_name=nas.example.com" in err
        assert 'note="say \\"hi\\""' in err
        assert "lineno=" not in err
