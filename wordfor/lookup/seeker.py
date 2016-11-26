import multiprocessing as mp

from wordfor.lookup.lookup import ExactLookup


class Seeker(object):
    """This class is the abstraction layer between the webapp and the lookup
    logic. This class will choose a lookup algorithm to run and spin it off in
    a separate process to contain the work outside of the web server process
    and let the OS handle the context switching that needs to happen."""

    """This is the class that will be used to create a new lookup attempt."""
    lookup_class = ExactLookup

    def __init__(self, search_id, query_string):
        """Create a new seeker. This is the class that spawns a new process to
        search for the answer to a query."""
        p = mp.Process(target=self.lookup_class,
                       args=(search_id, query_string,))
        p.start()
