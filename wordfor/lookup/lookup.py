from wordfor.api.v1.search.models import Answer, Word, Search


class Lookup(object):
    """This is it. This is the heavy lifting of the algorithm. Every subclass
    of this will implment one main method: run. The run method will take a full
    search_query as a string, do some "big data" magic and return a list of two
    tuples which are (Word, float) pairs."""

    """WARNING: this class is made to be run OUTSIDE of the application
    process. This is made to be a long running task and spinning this up
    inside the application process will cause a significant drop in the
    overall throughput of the web service."""

    def __init__(self, search_id, search_query):
        self.search = Search.query.get(search_id)
        if self.search is None:
            raise TypeError('Argument search_id does not correspond to an '
                            'existing search\'s ID.')
        self.report_answers(self.run(search_query))

    def run(self, search_query):
        """Run the algorithm. Find the search query with self.search_query and
        return a list of tuples as (Word, float) that represent the word and
        score match, respectively. The list of tuples is to be returned to be
        associated with the search via the self.search_id."""
        raise NotImplementedError('This lookup did not create a "run" method')

    def report_answers(self, answers):
        """Receive the list of (Word, float) tuples and create Answers out of
        them and the self.search_id."""
        for word, score in answers:
            Answer.create(search=self.search,
                          word=word,
                          score=score,
                          runtime=None)


class TrivialLookup(Lookup):
    """My first lookup algorithm! Wow, look at me go! Big data and all that.
    Some people trivialize machine learning to the phrase "counting stuff".
    I think that this is a kind of nicely manifested code version of that
    phrase (even though it's not even counting anything)."""

    def run(self, search_query):
        """Eh, let's just return a single word with a 100% score."""
        return [(Word.query.first(), 1.0)]
