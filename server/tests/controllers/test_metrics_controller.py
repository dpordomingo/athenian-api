# coding: utf-8

import pytest
import json
from aiohttp import web

from athenian.api.models.calculated_metrics import CalculatedMetrics
from athenian.api.models.invalid_request_error import InvalidRequestError
from athenian.api.models.metrics_request import MetricsRequest
from athenian.api.models.no_source_data_error import NoSourceDataError


async def test_calc_metrics_line_smoke(client):
    """Test case for calc_metrics

    Calculate metrics.
    """
    body = {
        "for": [
            {
                "developers": ["github.com/vmarkovtsev", "github.com/mcuadros"],
                "repositories": [
                    "github.com/src-d/go-git",
                    "github.com/athenianco/athenian-api",
                ],
            },
            {
                "developers": ["github.com/vmarkovtsev", "github.com/mcuadros"],
                "repositories": [
                    "github.com/src-d/go-git",
                    "github.com/athenianco/athenian-api",
                ],
            },
        ],
        "metrics": ["pr-lead-time", "pr-wip-time"],
        "date_from": "2015-10-13",
        "date_to": "2020-01-23",
        "granularity": "week",
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = await client.request(
        method="POST", path="/v1/metrics_line", headers=headers, json=body,
    )
    body = (await response.read()).decode("utf-8")
    assert response.status == 200, "Response body is : " + body