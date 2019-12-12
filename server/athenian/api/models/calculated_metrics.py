# coding: utf-8

from datetime import date
from typing import List

from athenian.api import util
from athenian.api.models.base_model_ import Model
from athenian.api.models.calculated_metric import CalculatedMetric
from athenian.api.models.granularity import Granularity
from athenian.api.models.metric_id import MetricID


class CalculatedMetrics(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(
        self,
        calculated: List[CalculatedMetric] = None,
        metrics: List[MetricID] = None,
        date_from: date = None,
        date_to: date = None,
        granularity: Granularity = None,
    ):
        """CalculatedMetrics - a model defined in OpenAPI

        :param calculated: The calculated of this CalculatedMetrics.
        :param metrics: The metrics of this CalculatedMetrics.
        :param date_from: The date_from of this CalculatedMetrics.
        :param date_to: The date_to of this CalculatedMetrics.
        :param granularity: The granularity of this CalculatedMetrics.
        """
        self.openapi_types = {
            "calculated": List[CalculatedMetric],
            "metrics": List[MetricID],
            "date_from": date,
            "date_to": date,
            "granularity": Granularity,
        }

        self.attribute_map = {
            "calculated": "calculated",
            "metrics": "metrics",
            "date_from": "date_from",
            "date_to": "date_to",
            "granularity": "granularity",
        }

        self._calculated = calculated
        self._metrics = metrics
        self._date_from = date_from
        self._date_to = date_to
        self._granularity = granularity

    @classmethod
    def from_dict(cls, dikt: dict) -> "CalculatedMetrics":
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The CalculatedMetrics of this CalculatedMetrics.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def calculated(self):
        """Gets the calculated of this CalculatedMetrics.

        The values of the requested metrics through time.

        :return: The calculated of this CalculatedMetrics.
        :rtype: List[CalculatedMetric]
        """
        return self._calculated

    @calculated.setter
    def calculated(self, calculated):
        """Sets the calculated of this CalculatedMetrics.

        The values of the requested metrics through time.

        :param calculated: The calculated of this CalculatedMetrics.
        :type calculated: List[CalculatedMetric]
        """
        if calculated is None:
            raise ValueError("Invalid value for `calculated`, must not be `None`")

        self._calculated = calculated

    @property
    def metrics(self):
        """Gets the metrics of this CalculatedMetrics.

        Repeats `MetricsRequest.metrics`.

        :return: The metrics of this CalculatedMetrics.
        :rtype: List[MetricID]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """Sets the metrics of this CalculatedMetrics.

        Repeats `MetricsRequest.metrics`.

        :param metrics: The metrics of this CalculatedMetrics.
        :type metrics: List[MetricID]
        """
        if metrics is None:
            raise ValueError("Invalid value for `metrics`, must not be `None`")

        self._metrics = metrics

    @property
    def date_from(self):
        """Gets the date_from of this CalculatedMetrics.

        Repeats `MetricsRequest.date_from`.

        :return: The date_from of this CalculatedMetrics.
        :rtype: date
        """
        return self._date_from

    @date_from.setter
    def date_from(self, date_from):
        """Sets the date_from of this CalculatedMetrics.

        Repeats `MetricsRequest.date_from`.

        :param date_from: The date_from of this CalculatedMetrics.
        :type date_from: date
        """
        if date_from is None:
            raise ValueError("Invalid value for `date_from`, must not be `None`")

        self._date_from = date_from

    @property
    def date_to(self):
        """Gets the date_to of this CalculatedMetrics.

        Repeats `MetricsRequest.date_to`.

        :return: The date_to of this CalculatedMetrics.
        :rtype: date
        """
        return self._date_to

    @date_to.setter
    def date_to(self, date_to):
        """Sets the date_to of this CalculatedMetrics.

        Repeats `MetricsRequest.date_to`.

        :param date_to: The date_to of this CalculatedMetrics.
        :type date_to: date
        """
        if date_to is None:
            raise ValueError("Invalid value for `date_to`, must not be `None`")

        self._date_to = date_to

    @property
    def granularity(self):
        """Gets the granularity of this CalculatedMetrics.

        :return: The granularity of this CalculatedMetrics.
        :rtype: Granularity
        """
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """Sets the granularity of this CalculatedMetrics.

        :param granularity: The granularity of this CalculatedMetrics.
        :type granularity: Granularity
        """
        if granularity is None:
            raise ValueError("Invalid value for `granularity`, must not be `None`")

        self._granularity = granularity
