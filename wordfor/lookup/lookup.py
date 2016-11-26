"""This file contains the lookup algorithm classes. They may not necessarily
contain all lookup logic."""

from datetime import datetime as dt

from wordfor.api.v1.search.models import Answer, Word, Search, Definition


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
        lookup_start = dt.now()
        answers = self.run(search_query)
        self.report_answers(answers, dt.now() - lookup_start)

    def run(self, search_query):
        """Run the algorithm. Find the search query with self.search_query and
        return a list of tuples as (Word, float) that represent the word and
        score match, respectively. The list of tuples is to be returned to be
        associated with the search via the self.search_id.

        :param string: search_query -- this is the query string for the search
            that will be used to compute the answers that the input was likely
            looking for.

        :return: [tuple(Word, float)] -- the return value is a list of
            (Word, float) tuples that will be coerced into answers for the
            given search."""
        raise NotImplementedError('This lookup did not create a "run" method')

    def report_answers(self, answers, runtime):
        """Create the answers for the search query.

        :param [tuple(Word, float)]: answers -- the list of (Word, float)
            tuples that will be used to create an answer. The word is the
            answer.word association and the float is the answer.score
            association.
        :param timedelta: runtime -- the timedelta that is recorded as the
            runtime for the computed answer.

        :return: None
        """
        for word, score in answers:
            Answer.create(search=self.search,
                          word=word,
                          score=score,
                          runtime=runtime)


class ExactLookup(Lookup):
    """My first lookup algorithm! Wow, look at me go! Big data and all that.
    I'm going to keep this one simple, then add more bells and whistles and
    smarter strategies to later lookup algorithms."""

    def run(self, search_query):
        """Eh, let's just return all the words that have the exact lookup
        definition."""
        return [(defin.word, 1.0)
                for defin in Definition.query.filter(
                    Definition.description == search_query).all()]
