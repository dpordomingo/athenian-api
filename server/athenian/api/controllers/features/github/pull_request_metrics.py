from datetime import datetime, timedelta
from typing import Optional

from athenian.api.controllers.features.github.pull_request import \
    PullRequestCounter, PullRequestMedianMetricCalculator, PullRequestMetricCalculator, \
    PullRequestSumMetricCalculator, register
from athenian.api.controllers.features.metric import Metric
from athenian.api.controllers.miners.github.pull_request import PullRequestTimes
from athenian.api.models.web import MetricID


@register(MetricID.PR_WIP_TIME)
class WorkInProgressTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Time of work in progress metric."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        if times.first_review_request and min_time < times.first_review_request.best < max_time:
            return times.first_review_request.best - times.work_began.best
        return None


@register(MetricID.PR_WIP_COUNT)
class WorkInProgressCounter(PullRequestCounter):
    """Count the number of PRs that were used to calculate PR_WIP_TIME."""

    calc_cls = WorkInProgressTimeCalculator


@register(MetricID.PR_REVIEW_TIME)
class ReviewTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Time of the review process metric."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        # We cannot be sure that the approvals finished unless the PR is closed.
        if times.first_review_request and times.closed and (
                (times.approved    and min_time < times.approved.best    < max_time) or  # noqa
                (times.last_review and min_time < times.last_review.best < max_time)):
            if times.approved:
                return times.approved.best - times.first_review_request.best
            elif times.last_review:
                return times.last_review.best - times.first_review_request.best
            else:
                assert False  # noqa
        return None


@register(MetricID.PR_REVIEW_COUNT)
class ReviewCounter(PullRequestCounter):
    """Count the number of PRs that were used to calculate PR_REVIEW_TIME."""

    calc_cls = ReviewTimeCalculator


@register(MetricID.PR_MERGING_TIME)
class MergingTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Time to merge after finishing the review metric."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        if times.closed and min_time < times.closed.best < max_time:
            # closed may mean either merged or not merged
            if times.approved:
                return times.closed.best - times.approved.best
            elif times.last_review:
                return times.closed.best - times.last_review.best
            elif times.last_commit:
                return times.closed.best - times.last_commit.best
        return None


@register(MetricID.PR_MERGING_COUNT)
class MergingCounter(PullRequestCounter):
    """Count the number of PRs that were used to calculate PR_MERGING_TIME."""

    calc_cls = MergingTimeCalculator


@register(MetricID.PR_RELEASE_TIME)
class ReleaseTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Time to appear in a release after merging metric."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        if times.merged and times.released and min_time < times.released.best < max_time:
            return times.released.best - times.merged.best
        return None


@register(MetricID.PR_RELEASE_COUNT)
class ReleaseCounter(PullRequestCounter):
    """Count the number of PRs that were used to calculate PR_RELEASE_TIME."""

    calc_cls = ReleaseTimeCalculator


@register(MetricID.PR_LEAD_TIME)
class LeadTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Time to appear in a release since starting working on the PR."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        if times.released and min_time < times.released.best < max_time:
            return times.released.best - times.work_began.best
        return None


@register(MetricID.PR_LEAD_COUNT)
class LeadCounter(PullRequestCounter):
    """Count the number of PRs that were used to calculate PR_LEAD_TIME."""

    calc_cls = LeadTimeCalculator


@register(MetricID.PR_WAIT_FIRST_REVIEW_TIME)
class WaitFirstReviewTimeCalculator(PullRequestMedianMetricCalculator[timedelta]):
    """Elapsed time between requesting the review for the first time and getting it."""

    may_have_negative_values = False

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[timedelta]:
        """Calculate the actual state update."""
        if times.first_review_request and times.first_comment_on_first_review and \
                min_time < times.first_comment_on_first_review.best < max_time:
            return times.first_comment_on_first_review.best - times.first_review_request.best
        return None


@register(MetricID.PR_OPENED)
class OpenedCalculator(PullRequestSumMetricCalculator[int]):
    """Number of open PRs."""

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[int]:
        """Calculate the actual state update."""
        if times.created.best < max_time and ((not times.closed) or times.closed.best > max_time):
            return 1
        return None


@register(MetricID.PR_MERGED)
class MergedCalculator(PullRequestSumMetricCalculator[int]):
    """Number of merged PRs."""

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[int]:
        """Calculate the actual state update."""
        if times.merged and min_time < times.merged.best < max_time:
            return 1
        return None


@register(MetricID.PR_CLOSED)
class ClosedCalculator(PullRequestSumMetricCalculator[int]):
    """Number of closed PRs."""

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[int]:
        """Calculate the actual state update."""
        if times.closed and min_time < times.closed.best < max_time:
            return 1
        return None


@register(MetricID.PR_FLOW_RATIO)
class FlowRatioCalculator(PullRequestMetricCalculator[float]):
    """PR flow ratio - opened / closed - calculator."""

    def __init__(self):
        """Initialize a new instance of FlowRatioCalculator."""
        super().__init__()
        self._opened = OpenedCalculator()
        self._closed = ClosedCalculator()

    def value(self) -> Metric[float]:
        """Calculate the current metric value."""
        opened = self._opened.value()
        closed = self._closed.value()
        if not closed.exists:
            return Metric(False, None, None, None)
        if not opened.exists:
            return Metric(True, 0, None, None)  # yes, it is True, not False as above
        val = opened.value / closed.value
        return Metric(True, val, None, None)

    def analyze(self, times: PullRequestTimes, min_time: datetime, max_time: datetime,
                ) -> Optional[float]:
        """Calculate the actual state update."""
        self._opened(times, min_time, max_time)
        self._closed(times, min_time, max_time)
        return None
