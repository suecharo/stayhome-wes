#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from time import sleep

from flask import Flask
from flask.testing import FlaskClient
from flask.wrappers import Response
from py._path.local import LocalPath

from genpei.app import create_app
from genpei.type import RunId, RunListResponse


def get_runs(client: FlaskClient) -> Response:  # type: ignore
    response: Response = client.get(f"/runs")

    return response


def test_get_runs(tmpdir: LocalPath) -> None:
    app: Flask = create_app(Path(tmpdir))
    app.testing = True
    client: FlaskClient[Response] = app.test_client()
    from .post_runs_tests.test_access_remote_files import access_remote_files
    posts_res: Response = access_remote_files(client)
    posts_res_data: RunId = posts_res.get_json()

    assert posts_res.status_code == 200

    run_id: str = posts_res_data["run_id"]
    sleep(3)
    res: Response = get_runs(client)
    res_data: RunListResponse = res.get_json()

    assert res.status_code == 200
    assert "runs" in res_data
    assert len(res_data["runs"]) == 1
    assert "run_id" in res_data["runs"][0]
    assert "state" in res_data["runs"][0]
    assert run_id == res_data["runs"][0]["run_id"]
