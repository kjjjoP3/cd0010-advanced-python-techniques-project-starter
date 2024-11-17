"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains auxiliary data structures to
    quickly retrieve NEOs by primary designation or name and to facilitate
    filtering close approaches based on user-defined criteria.
    """

    def __init__(self, neos, approaches):
        """Initialize the `NEODatabase` with NEOs and close approaches.

        Links the provided NEOs and close approaches, ensuring that the
        `.approaches` attribute of each `NearEarthObject` includes the
        relevant close approaches, and each `CloseApproach` is linked to its
        corresponding `NearEarthObject`.

        :param neos: A list of `NearEarthObject` instances.
        :param approaches: A list of `CloseApproach` instances.
        """
        self._neos = neos
        self._approaches = approaches

        # Create dictionaries for quick lookup by designation and name
        self.neos_dict = {neo.designation: neo for neo in self._neos}
        self.neos_dict_name = {neo.name: neo for neo in self._neos if neo.name}

        # Establish links between close approaches and NEOs
        for approach in self._approaches:
            neo = self.neos_dict.get(approach._designation)
            if neo:
                approach.neo = neo
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Retrieve an NEO using its primary designation.

        :param designation: The primary designation of the desired NEO.
        :return: The `NearEarthObject` with the specified designation, or `None`.
        """
        return self.neos_dict.get(designation)

    def get_neo_by_name(self, _name):
        """Retrieve an NEO using its name.

        :param _name: The name of the desired NEO.
        :return: The `NearEarthObject` with the specified name, or `None`.
        """
        return self.neos_dict_name.get(_name)

    def query(self, filters=()):
        """Generate a stream of close approaches that satisfy the given filters.

        :param filters: A sequence of filter functions to apply to the close approaches.
        :return: A generator yielding `CloseApproach` objects that meet all criteria.
        """
        for approach in self._approaches:
            if all(filter_func(approach) for filter_func in filters):
                yield approach