from bs4 import BeautifulSoup as BS
import requests

from wordfor.ingest.base_source import BaseSource


class OxfordLearnerSource(BaseSource):
    base_url = 'http://www.oxfordlearnersdictionaries.com/browse/english/'

    def crawl_letter_links(self, text):
        """Given the page:
        http://www.oxfordlearnersdictionaries.com/browse/english/
        get the links to each letter page (e.g. a, b, c, etc.) so that we can
        crawl those pages.

        :param string: text -- the base text from the base_url HTML response."""
        return [a['href'] for a in
                BS(text, 'html.parser').find(id='letters').find_all('a')]

    def crawl_word_group_links_from_word_groups(self, group_text):
        """Given a raw html page of a word group page, return all the links to
        the individual words on the page.

        :param string: group_text -- the base text from the word group HTML
            response.
        """
        return [a['href'] for a in
                BS(group_text, 'html.parser').find(id='groupResult')
                .find_all('a')]

    def crawl_word_group_for_word_links(self, words_text):
        """Given a raw html page of a list of words (with their links), return
        all the links for each individual word."""
        return [a['href'] for a in
                BS(words_text, 'html.parser').find(id='result')
                .find_all('a')]

    def crawl(self):
        res = requests.get(self.base_url)
        full_word_links = []
        for link in self.crawl_letter_links(res.text):
            res = requests.get(link)
            word_group_links = \
                self.crawl_word_group_links_from_word_groups(res.text)
            for word_group_link in word_group_links:
                res = requests.get(word_group_link)
                word_links = self.crawl_word_group_for_word_links(res.text)
                full_word_links += word_links
        return full_word_links

    def extract(self, word_links):
        """Given a set of word links, extract the data from the page, then
        format and return it.

        :param list: word_links -- a list of URLs to request and extract data
            from
        """
        full_words = []
        for link in word_links:
            res = requests.get(link)
            soup = BS(res.text, 'html.parser')
            word_name = soup.find('h2', class_='h')
            description = soup.find('span', class_='def')
            word_class = soup.find('span', class_='pos')
            if all([x is not None
                    for x in [word_name, description, word_class]]):
                # TODO: change print to log
                print('Extracting {}'.format(word_name.text))
                full_words.append({
                    'name': word_name.text,
                    'definitions': [
                        {
                            'description': description.text,
                            'word_class': word_class.text,
                        }
                    ]
                })
            else:
                print('Skipping word extraction, something is None')
        return full_words
