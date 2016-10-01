class BaseSource(object):
    def __init__(self):
        self.parse(self.extract(self.crawl()))

    def crawl(self):
        """A 'crawl' will, given some data source, find where the data lives
        and return it to be sent to the extract method."""
        raise NotImplementedError

    def extract(self):
        """An 'extract' will, take the data from the source it is pointed to
        and put it into a format that we can understand. Namely, it will put
        words into a list of dicts that take the form:

            {
                'name': <word name>,
                'definitions': [
                    {
                        'description': <definition of word>,
                        'word_class': <word class>
                    }
                ]
            }
        """
        raise NotImplementedError

    def parse(self, extraced_data):
        """A 'parse' will, given some list that is returned by an extract, take
        the list and turn them into models that exist in the database, trying
        its best to resolve any conflicts that may arise from the already
        existing words or their definitions.

        :param list: extracted_data -- a list of dicts with keys:
            ['name', 'definitions']. Where 'name' is a string value and
            'definitions' is a list of dicts that have 'word_class' and
            'description' keys from which a word and definition may be eaily
            constructed."""
        for word in extracted_data:
            new_word = Word.find_or_create_by_name(word['name'])
            for definition in word['definitions']:
                pass  # TODO: come back to this
