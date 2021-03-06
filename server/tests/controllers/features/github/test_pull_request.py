from datetime import datetime, timedelta, timezone
import itertools

import faker
import numpy as np
import pandas as pd
import pytest

from athenian.api.controllers.features.github.pull_request import mean_confidence_interval, \
    median_confidence_interval, PullRequestAverageMetricCalculator, \
    PullRequestMedianMetricCalculator
from athenian.api.controllers.miners.github.pull_request import Fallback, PullRequestTimes


@pytest.fixture
def square_centered_samples():
    data = (10 - np.arange(0, 21, dtype=int)) ** 2
    data[11:] *= -1
    return data


def test_mean_confidence_interval_positive():
    np.random.seed(8)
    data = np.random.lognormal(1, 2, 1000).astype(np.float32)
    mean, conf_min, conf_max = mean_confidence_interval(data, False)
    assert isinstance(mean, np.float32)
    assert isinstance(conf_min, np.float32)
    assert isinstance(conf_max, np.float32)
    assert 20.7 < mean < 20.8
    assert 18.93 < conf_min < 18.94
    assert 29.5 < conf_max < 29.6


def test_mean_confidence_interval_negative(square_centered_samples):
    mean, conf_min, conf_max = mean_confidence_interval(square_centered_samples, True)
    assert isinstance(mean, np.int64)
    assert isinstance(conf_min, np.int64)
    assert isinstance(conf_max, np.int64)
    assert mean == 0
    assert conf_min == -22
    assert conf_max == 22


def test_mean_confidence_interval_timedelta_positive():
    np.random.seed(8)
    data = pd.Series(
        (np.random.lognormal(1, 2, 1000) * 1_000_000_000 * 3600).astype(np.timedelta64))
    mean, conf_min, conf_max = mean_confidence_interval(data, False)
    assert isinstance(mean, pd.Timedelta)
    assert isinstance(conf_min, pd.Timedelta)
    assert isinstance(conf_max, pd.Timedelta)
    assert pd.Timedelta(hours=20) < mean < pd.Timedelta(hours=21)
    assert pd.Timedelta(hours=18) < conf_min < pd.Timedelta(hours=19)
    assert pd.Timedelta(hours=29) < conf_max < pd.Timedelta(hours=30)


def test_mean_confidence_interval_timedelta_negative(square_centered_samples):
    data = pd.Series((square_centered_samples * 1_000_000_000).astype(np.timedelta64))
    mean, conf_min, conf_max = mean_confidence_interval(data, True)
    assert isinstance(mean, pd.Timedelta)
    assert isinstance(conf_min, pd.Timedelta)
    assert isinstance(conf_max, pd.Timedelta)
    assert mean == pd.Timedelta(0)
    assert abs((conf_min - pd.Timedelta(seconds=-22)).total_seconds()) < 1
    assert abs((conf_max - pd.Timedelta(seconds=22)).total_seconds()) < 1


def test_mean_confidence_interval_empty():
    with pytest.raises(AssertionError):
        mean_confidence_interval([], True)


def test_mean_confidence_interval_negative_list(square_centered_samples):
    mean, conf_min, conf_max = mean_confidence_interval(list(square_centered_samples), True)
    assert isinstance(mean, np.int64)
    assert isinstance(conf_min, np.int64)
    assert isinstance(conf_max, np.int64)
    assert mean == 0
    assert conf_min == -22
    assert conf_max == 22


def test_median_confidence_interval_int(square_centered_samples):
    mean, conf_min, conf_max = median_confidence_interval(square_centered_samples)
    assert isinstance(mean, np.int64)
    assert isinstance(conf_min, np.int64)
    assert isinstance(conf_max, np.int64)
    assert mean == 0
    assert conf_min == -16
    assert conf_max == 16


def test_median_confidence_interval_timedelta(square_centered_samples):
    data = pd.Series((square_centered_samples * 1_000_000_000).astype(np.timedelta64))
    mean, conf_min, conf_max = median_confidence_interval(data)
    assert isinstance(mean, pd.Timedelta)
    assert isinstance(conf_min, pd.Timedelta)
    assert isinstance(conf_max, pd.Timedelta)
    assert mean == pd.Timedelta(0)
    assert conf_min == pd.Timedelta(seconds=-16)
    assert conf_max == pd.Timedelta(seconds=16)


def test_median_confidence_interval_empty():
    with pytest.raises(AssertionError):
        median_confidence_interval([])


@pytest.fixture
def pr_samples():
    def generate(n):
        fake = faker.Faker()

        def random_pr():
            created_at = fake.date_time_between(
                start_date="-3y", end_date="-6M", tzinfo=timezone.utc)
            first_commit = fake.date_time_between(
                start_date="-3y1M", end_date=created_at, tzinfo=timezone.utc)
            last_commit_before_first_review = fake.date_time_between(
                start_date=created_at, end_date=created_at + timedelta(days=30),
                tzinfo=timezone.utc)
            first_comment_on_first_review = fake.date_time_between(
                start_date=last_commit_before_first_review, end_date=timedelta(days=2),
                tzinfo=timezone.utc)
            first_review_request = fake.date_time_between(
                start_date=last_commit_before_first_review, end_date=first_comment_on_first_review,
                tzinfo=timezone.utc)
            first_passed_checks = fake.date_time_between(
                start_date=created_at, end_date=first_review_request, tzinfo=timezone.utc)
            approved_at = fake.date_time_between(
                start_date=first_comment_on_first_review + timedelta(days=1),
                end_date=first_comment_on_first_review + timedelta(days=30),
                tzinfo=timezone.utc)
            last_commit = fake.date_time_between(
                start_date=first_comment_on_first_review + timedelta(days=1),
                end_date=approved_at,
                tzinfo=timezone.utc)
            last_passed_checks = fake.date_time_between(
                last_commit, last_commit + timedelta(days=1), tzinfo=timezone.utc)
            merged_at = fake.date_time_between(
                approved_at, approved_at + timedelta(days=2), tzinfo=timezone.utc)
            closed_at = merged_at
            last_review = fake.date_time_between(approved_at, closed_at, tzinfo=timezone.utc)
            released_at = fake.date_time_between(
                merged_at, merged_at + timedelta(days=30), tzinfo=timezone.utc)
            return PullRequestTimes(
                created=Fallback(created_at, None),
                first_commit=Fallback(first_commit, created_at),
                last_commit_before_first_review=Fallback(last_commit_before_first_review, None),
                last_commit=Fallback(last_commit, None),
                merged=Fallback(merged_at, None),
                first_comment_on_first_review=Fallback(first_comment_on_first_review, None),
                first_review_request=Fallback(first_review_request, None),
                last_review=Fallback(last_review, None),
                approved=Fallback(approved_at, None),
                first_passed_checks=Fallback(first_passed_checks, None),
                last_passed_checks=Fallback(last_passed_checks, None),
                finalized=Fallback(min(max(approved_at, last_passed_checks, last_commit),
                                       closed_at), None),
                released=Fallback(released_at, None),
                closed=Fallback(closed_at, None),
            )

        return [random_pr() for _ in range(n)]
    return generate


def ensure_dtype(pr, dtype):
    if not isinstance(pr.created.value, dtype):
        pr = PullRequestTimes(**{k: Fallback(dtype(v.value), None) for k, v in vars(pr).items()})
    return pr


@pytest.mark.parametrize(
    "cls, negative, dtype",
    ((*t[0], t[1]) for t in itertools.product(
        [(PullRequestAverageMetricCalculator, False),
         (PullRequestAverageMetricCalculator, True),
         (PullRequestMedianMetricCalculator, False)],
        [datetime, pd.Timestamp])))
def test_pull_request_metric_calculator(pr_samples, cls, negative, dtype):
    class LeadTimeCalculator(cls):
        may_have_negative_values = negative

        def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                    ) -> timedelta:
            return times.released.value - times.work_began.best

    calc = LeadTimeCalculator()
    for pr in pr_samples(100):
        calc(ensure_dtype(pr, dtype), datetime.now(), datetime.now())
    m = calc.value()
    assert m.exists
    assert isinstance(m.value, timedelta)
    assert isinstance(m.confidence_min, timedelta)
    assert isinstance(m.confidence_max, timedelta)
    assert m.confidence_score() > 50
    assert timedelta() < m.value < timedelta(days=365 * 3 + 32)
    assert m.confidence_min < m.value < m.confidence_max
    calc.reset()
    m = calc.value()
    assert not m.exists
    assert m.value is None
    assert m.confidence_min is None
    assert m.confidence_max is None
