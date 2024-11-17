from operator import eq, ge, le
import itertools

class UnsupportedCriterionError(NotImplementedError):
    """Raised when an unsupported criterion is used in filtering."""


class AttributeFilter:
    """A base class for filters that compare an attribute against a reference value.

    Filters are callable objects. When invoked, they compare a specific attribute
    of a `CloseApproach` instance with a reference value using a comparison operator.

    Subclasses should override `get` to specify which attribute to fetch.
    """

    def __init__(self, comparator, reference):
        """
        Initialize the filter with a comparator and reference value.

        :param comparator: A function for comparison, e.g., operator.le.
        :param reference: The value to compare the attribute against.
        """
        self.comparator = comparator
        self.reference = reference

    def __call__(self, approach):
        """Evaluate whether the approach satisfies the filter."""
        return self.comparator(self.get(approach), self.reference)

    @classmethod
    def get(cls, approach):
        """Fetch the attribute of interest from the `CloseApproach` instance."""
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return a string representation of the filter."""
        op_name = self.comparator.__name__
        return f"{self.__class__.__name__}(comparator=operator.{op_name}, reference={self.reference})"


class DateFilter(AttributeFilter):
    """Filter for `CloseApproach` date."""

    @classmethod
    def get(cls, approach):
        """Fetch the approach date."""
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """Filter for approach distance."""

    @classmethod
    def get(cls, approach):
        """Fetch the approach distance."""
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Filter for approach velocity."""

    @classmethod
    def get(cls, approach):
        """Fetch the approach velocity."""
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Filter for NEO diameter."""

    @classmethod
    def get(cls, approach):
        """Fetch the diameter of the NEO."""
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """Filter for hazardous status."""

    @classmethod
    def get(cls, approach):
        """Fetch whether the NEO is hazardous."""
        return approach.neo.hazardous


def create_filters(
    date=None, start_date=None, end_date=None,
    distance_min=None, distance_max=None,
    velocity_min=None, velocity_max=None,
    diameter_min=None, diameter_max=None,
    hazardous=None
):
    """Generate a list of filters based on user-defined criteria."""
    criteria = []

    if date is not None:
        criteria.append(DateFilter(eq, date))
    if start_date is not None:
        criteria.append(DateFilter(ge, start_date))
    if end_date is not None:
        criteria.append(DateFilter(le, end_date))
    if distance_min is not None:
        criteria.append(DistanceFilter(ge, distance_min))
    if distance_max is not None:
        criteria.append(DistanceFilter(le, distance_max))
    if velocity_min is not None:
        criteria.append(VelocityFilter(ge, velocity_min))
    if velocity_max is not None:
        criteria.append(VelocityFilter(le, velocity_max))
    if diameter_min is not None:
        criteria.append(DiameterFilter(ge, diameter_min))
    if diameter_max is not None:
        criteria.append(DiameterFilter(le, diameter_max))
    if hazardous is not None:
        criteria.append(HazardousFilter(eq, hazardous))

    return criteria


def limit(iterator, n=None):
    """Restrict the number of items generated by the iterator.

    :param iterator: An iterator providing values.
    :param n: Maximum number of items to generate (no limit if None or 0).
    :yield: Items from the iterator, up to the specified limit.
    """
    return itertools.islice(iterator, n) if n else iterator