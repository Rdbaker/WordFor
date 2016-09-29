# -*- encoding: utf-8 -*-
"""Search models tests."""
import pytest

from wordfor.api.v1.search import models


@pytest.mark.usefixtures('db')
class TestSearchModel():
    def test_over_200_char_query_not_acceptable(self):
        """Test that the limit for the query is 200 characters."""
        char_201_len = ('1234567890' * 21)[:201]
        char_200_len = char_201_len[:-1]

        # this should simply not raise an error
        search = models.Search(query_string=char_200_len)
        search.save()

        from sqlalchemy.exc import DataError
        with pytest.raises(DataError):
            search = models.Search(query_string=char_201_len)
            search.save()

    def test_query_required_for_search(self):
        """Test that the 'query' attribute is required to create a search."""
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            search = models.Search()
            search.save()


@pytest.mark.usefixtures('db')
class TestAnswerModel():
    def test_rating_is_score(self):
        """Test that the answer.rating is just an alias for its score."""
        score = 0.02201
        answer = models.Answer(score=score)
        assert(answer.rating == score)


@pytest.mark.usefixtures('db')
class TestWordModel():
    def test_trivial(self):
        """This is a trivial test just as a placeholder for something more
        substantial once there is logic in the word model to test."""
        assert models.Word(name='blah')


@pytest.mark.usefixtures('db')
class TestDefinitionModel():
    @pytest.mark.parametrize('wordclass,', models.Definition.word_classes)
    def test_word_class_validation_passing(self, wordclass):
        """Test that proper word classes are accepted."""
        definition = models.Definition(
            description='not nullable', word_class=wordclass)
        # make sure no errors are raised
        assert definition.save()

    def test_word_class_validation_failure(self):
        """Test that an improper word class fails validation."""
        from wordfor.api.errors import UnprocessableEntityError
        with pytest.raises(UnprocessableEntityError):
            definition = models.Definition(description='not nullable',
                                           word_class='improper')
            definition.save()

    def test_definition_requires_word_class(self):
        """Test that the word class is not nullable."""
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            definition = models.Definition(description='not nullable')
            definition.save()

    def test_definition_requires_description(self):
        """Test that the description is not nullable."""
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            definition = models.Definition(word_class='noun')
            definition.save()
