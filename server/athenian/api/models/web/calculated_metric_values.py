import datetime
from typing import List, Optional

from athenian.api.models.web.base_model_ import Model


class CalculatedMetricValues(Model):
    """Calculated metrics: date, values, confidences."""

    def __init__(self, date: Optional[datetime.date] = None,
                 values: Optional[List[object]] = None,
                 confidence_scores: Optional[List[int]] = None,
                 confidence_mins: Optional[List[object]] = None,
                 confidence_maxs: Optional[List[object]] = None,
                 ):
        """Initialize CalculatedMetricValues - a model defined in OpenAPI.

        :param date: The date of this CalculatedMetricValues.
        :param values: The values of this CalculatedMetricValues.
        :param confidence_mins: The left boundaries of the 95% confidence interval of this \
                               CalculatedMetricValues.
        :param confidence_maxs: The right boundaries of the 95% confidence interval of this \
                               CalculatedMetricValues.
        :param confidence_scores: The confidence scores of this CalculatedMetricValues.
        """
        self.openapi_types = {"date": datetime.date,
                              "values": List[object],
                              "confidence_scores": List[int],
                              "confidence_mins": List[object],
                              "confidence_maxs": List[object],
                              }
        self.attribute_map = {"date": "date",
                              "values": "values",
                              "confidence_scores": "confidence_scores",
                              "confidence_mins": "confidence_mins",
                              "confidence_maxs": "confidence_maxs",
                              }
        self._date = date
        self._values = values
        self._confidence_mins = confidence_mins
        self._confidence_maxs = confidence_maxs
        self._confidence_scores = confidence_scores

    @property
    def date(self) -> datetime.date:
        """Gets the date of this CalculatedMetricValues.

        Where you should relate the metric value to on the time axis.

        :return: The date of this CalculatedMetricValues.
        """
        return self._date

    @date.setter
    def date(self, date: datetime.date):
        """Sets the date of this CalculatedMetricValues.

        Where you should relate the metric value to on the time axis.

        :param date: The date of this CalculatedMetricValues.
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")

        self._date = date

    @property
    def values(self) -> List[object]:
        """Gets the values of this CalculatedMetricValues.

        The same order as `metrics`.

        :return: The values of this CalculatedMetricValues.
        """
        return self._values

    @values.setter
    def values(self, values: List[object]):
        """Sets the values of this CalculatedMetricValues.

        The same order as `metrics`.

        :param values: The values of this CalculatedMetricValues.
        """
        if values is None:
            raise ValueError("Invalid value for `values`, must not be `None`")

        self._values = values

    @property
    def confidence_mins(self) -> List[object]:
        """Gets the left boundaries of the 95% confidence interval of this CalculatedMetricValues.

        Confidence interval @ p=0.95, minimum. The same order as `metrics`.

        :return: The left boundaries of the 95% confidence interval of this CalculatedMetricValues.
        """
        return self._confidence_mins

    @confidence_mins.setter
    def confidence_mins(self, confidence_mins: List[object]):
        """Sets the left boundaries of the 95% confidence interval of this CalculatedMetricValues.

        Confidence interval @ p=0.95, minimum. he same order as `metrics`.

        :param confidence_mins: The left boundaries of the 95% confidence interval of this \
                               CalculatedMetricValues.
        """
        self._confidence_mins = confidence_mins

    @property
    def confidence_maxs(self) -> List[object]:
        """Gets the right boundaries of the 95% confidence interval of this CalculatedMetricValues.

        Confidence interval @ p=0.95, maximum. The same order as `metrics`.

        :return: The right boundaries of the 95% confidence interval of this \
                 CalculatedMetricValues.
        """
        return self._confidence_maxs

    @confidence_maxs.setter
    def confidence_maxs(self, confidence_maxs: List[object]):
        """Sets the right boundaries of the 95% confidence interval of this CalculatedMetricValues.

        Confidence interval @ p=0.95, maximum. he same order as `metrics`.

        :param confidence_maxs: The right boundaries of the 95% confidence interval of this \
                               CalculatedMetricValues.
        """
        self._confidence_maxs = confidence_maxs

    @property
    def confidence_scores(self) -> List[int]:
        """Gets the confidence scores of this CalculatedMetricValues.

        The same order as `metrics`.

        :return: The values of this CalculatedMetricValues.
        """
        return self._confidence_scores

    @confidence_scores.setter
    def confidence_scores(self, confidence_scores: List[int]):
        """Sets the confidence scores of this CalculatedMetricValues.

        Confidence score from 0 (no idea) to 100 (very confident). The same order as `metrics`.

        :param confidence_scores: The confidence scores of this CalculatedMetricValues.
        """
        self._confidence_scores = confidence_scores
