# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from athenian.api.models.base_model_ import Model
from athenian.api.models.repository_set import RepositorySet
from athenian.api import util


class NoSourceDataError(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, error: str=None, repositories: RepositorySet=None):
        """NoSourceDataError - a model defined in OpenAPI

        :param error: The error of this NoSourceDataError.
        :param repositories: The repositories of this NoSourceDataError.
        """
        self.openapi_types = {
            'error': str,
            'repositories': RepositorySet
        }

        self.attribute_map = {
            'error': 'error',
            'repositories': 'repositories'
        }

        self._error = error
        self._repositories = repositories

    @classmethod
    def from_dict(cls, dikt: dict) -> 'NoSourceDataError':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The NoSourceDataError of this NoSourceDataError.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def error(self):
        """Gets the error of this NoSourceDataError.

        Why the server cannot fulfill the request.

        :return: The error of this NoSourceDataError.
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this NoSourceDataError.

        Why the server cannot fulfill the request.

        :param error: The error of this NoSourceDataError.
        :type error: str
        """
        if error is None:
            raise ValueError("Invalid value for `error`, must not be `None`")

        self._error = error

    @property
    def repositories(self):
        """Gets the repositories of this NoSourceDataError.


        :return: The repositories of this NoSourceDataError.
        :rtype: RepositorySet
        """
        return self._repositories

    @repositories.setter
    def repositories(self, repositories):
        """Sets the repositories of this NoSourceDataError.


        :param repositories: The repositories of this NoSourceDataError.
        :type repositories: RepositorySet
        """
        if repositories is None:
            raise ValueError("Invalid value for `repositories`, must not be `None`")

        self._repositories = repositories
