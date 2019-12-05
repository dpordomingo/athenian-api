# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from athenian.api.models.base_model_ import Model
from athenian.api.models.calculated_metric_values import CalculatedMetricValues
from athenian.api.models.for_set import ForSet
from athenian.api import util


class CalculatedMetric(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, _for: ForSet=None, values: List[CalculatedMetricValues]=None):
        """CalculatedMetric - a model defined in OpenAPI

        :param _for: The _for of this CalculatedMetric.
        :param values: The values of this CalculatedMetric.
        """
        self.openapi_types = {
            '_for': ForSet,
            'values': List[CalculatedMetricValues]
        }

        self.attribute_map = {
            '_for': 'for',
            'values': 'values'
        }

        self.__for = _for
        self._values = values

    @classmethod
    def from_dict(cls, dikt: dict) -> 'CalculatedMetric':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The CalculatedMetric of this CalculatedMetric.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _for(self):
        """Gets the _for of this CalculatedMetric.


        :return: The _for of this CalculatedMetric.
        :rtype: ForSet
        """
        return self.__for

    @_for.setter
    def _for(self, _for):
        """Sets the _for of this CalculatedMetric.


        :param _for: The _for of this CalculatedMetric.
        :type _for: ForSet
        """
        if _for is None:
            raise ValueError("Invalid value for `_for`, must not be `None`")

        self.__for = _for

    @property
    def values(self):
        """Gets the values of this CalculatedMetric.


        :return: The values of this CalculatedMetric.
        :rtype: List[CalculatedMetricValues]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this CalculatedMetric.


        :param values: The values of this CalculatedMetric.
        :type values: List[CalculatedMetricValues]
        """
        if values is None:
            raise ValueError("Invalid value for `values`, must not be `None`")

        self._values = values
