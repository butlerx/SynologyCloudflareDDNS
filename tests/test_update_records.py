"""End-to-end tests of update_records against an in-memory Cloudflare API."""

from __future__ import annotations

from typing import Any

import pytest

import synology_cloudflare_ddns.__main__ as cli


class FakeDnsRecords:
    """Records endpoint backed by a list; records writes for assertions."""

    def __init__(self, records: list) -> None:
        self.records = records
        self.puts: list = []
        self.posts: list = []

    def get(self, zone_id: str, params: dict) -> list:
        return [
            r
            for r in self.records
            if r["zone_id"] == zone_id and r["name"] == params["name"] and r["type"] == params["type"]
        ]

    def put(self, zone_id: str, record_id: str, data: dict) -> None:
        self.puts.append((zone_id, record_id, data))

    def post(self, zone_id: str, data: dict) -> None:
        self.posts.append((zone_id, data))


class FakeZones:
    """Zones endpoint that matches on exact name."""

    def __init__(self, zones: list, records: list) -> None:
        self.zones = zones
        self.dns_records = FakeDnsRecords(records)

    def get(self, params: dict) -> list:
        return [z for z in self.zones if z["name"] == params["name"]]


class FakeCloudFlare:
    """Just enough of the CloudFlare client for update_records."""

    def __init__(self, zones: list, records: list) -> None:
        self.zones = FakeZones(zones, records)


ZONE = {"id": "z1", "name": "example.com"}


def record(name: str, content: str, *, rid: str = "r1", proxied: bool = False, rtype: str = "A") -> dict:
    return {
        "id": rid,
        "zone_id": "z1",
        "name": name,
        "type": rtype,
        "content": content,
        "proxied": proxied,
        "ttl": 300,
    }


@pytest.fixture
def fake(monkeypatch: pytest.MonkeyPatch) -> Any:
    holder: dict = {}

    def install(records: list) -> FakeCloudFlare:
        holder["cf"] = FakeCloudFlare([ZONE], records)
        return holder["cf"]

    monkeypatch.setattr(cli, "CloudFlare", lambda token: holder["cf"])  # noqa: ARG005
    return install


def test_updates_only_the_named_record(fake: Any) -> None:
    cf = fake([record("nas.example.com", "1.1.1.1"), record("www.example.com", "9.9.9.9", rid="r2")])
    assert cli.update_records("key", "nas.example.com", "2.2.2.2") == 0
    assert [(rid, data["name"], data["content"]) for _, rid, data in cf.zones.dns_records.puts] == [
        ("r1", "nas.example.com", "2.2.2.2")
    ]


def test_keeps_proxied_and_ttl(fake: Any) -> None:
    cf = fake([record("nas.example.com", "1.1.1.1", proxied=False)])
    cli.update_records("key", "nas.example.com", "2.2.2.2")
    (_, _, data) = cf.zones.dns_records.puts[0]
    assert data["proxied"] is False
    assert data["ttl"] == 300


def test_unchanged_address_makes_no_calls(fake: Any) -> None:
    cf = fake([record("nas.example.com", "1.1.1.1")])
    assert cli.update_records("key", "nas.example.com", "1.1.1.1") == 0
    assert cf.zones.dns_records.puts == []
    assert cf.zones.dns_records.posts == []


def test_creates_missing_record_for_hostname_not_apex(fake: Any) -> None:
    cf = fake([])
    assert cli.update_records("key", "a.b.example.com", "2.2.2.2") == 0
    assert cf.zones.dns_records.posts == [
        ("z1", {"name": "a.b.example.com", "type": "A", "content": "2.2.2.2"})
    ]


def test_ipv6_uses_aaaa(fake: Any) -> None:
    cf = fake([])
    cli.update_records("key", "nas.example.com", "2001:db8::1")
    assert cf.zones.dns_records.posts[0][1]["type"] == "AAAA"


def test_unknown_zone_fails(fake: Any) -> None:
    fake([])
    assert cli.update_records("key", "nas.example.org", "2.2.2.2") == 2
