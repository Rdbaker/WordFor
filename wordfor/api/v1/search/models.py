# -*- coding: utf-8 -*-
"""Search models."""
from sqlalchemy.orm import validates

from wordfor.api.errors import UnprocessableEntityError
from wordfor.database import (Column, Model, db, SurrogatePK, reference_col,
                              relationship)


class Search(SurrogatePK, Model):
    """A search from a user."""

    __tablename__ = 'searches'
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='searches')
    query_string = Column(db.String(length=200), nullable=False)
    answers = relationship("Answer")

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Search({id})>'.format(id=self.id)


class Answer(Model):
    """Acts as a search <-> word join table with a score (float)."""

    __tablename__ = 'answers'
    score = Column(db.Float)
    word_id = Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
    word = relationship("Word", cascade="delete")
    search_id = Column(db.Integer,
                       db.ForeignKey('searches.id'),
                       primary_key=True)
    search = relationship("Search", cascade="delete")
    # how long did it take to compute this answer?
    runtime = Column(db.Interval)

    @property
    def rating(self):
        return self.score

    def __repr__(self):
        return "<Answer({word})".format(word=self.word.name)


class Word(SurrogatePK, Model):
    """A word that may be one of the answers to a search."""

    __tablename__ = 'words'
    name = Column(db.String, nullable=False)
    definitions = relationship("Definition")

    def __repr__(self):
        return "<Word({name})".format(name=self.name)


class Definition(SurrogatePK, Model):
    """A definition for a word."""

    word_classes = set([
        'noun',
        'verb',
        'adjective',
        'adverb',
        'pronoun',
        'preposition',
        'conjunction',
        'determiner',
        'exclamation'
    ])

    __tablename__ = 'definitions'
    description = Column(db.Text, nullable=False)
    word_class = Column(db.String, nullable=False)
    word_id = Column(db.Integer, db.ForeignKey('words.id'))
    word = relationship("Word", cascade="delete")

    @validates('word_class')
    def validate_word_class(self, key, word_class):
        """Ensures that a word class is valid as defined by the Oxford
        Dictionary at:
        https://en.oxforddictionaries.com/grammar/word-classes-or-parts-of-speech
        (retrieved 2016)
        """
        if word_class.lower() not in self.word_classes:
            raise UnprocessableEntityError(description='Word class {} is ' +
                                           'not an acceptable word class ' +
                                           'must be one of: {}'
                                           .format(word_class,
                                                   self.word_classes))
        return word_class

    def __repr__(self):
        """Return a string representing a word definition as a dictionary would

        example usage:

            >>> empathy = Word.get(empathy_id)
            >>> empathy.definitions[0]
            <Definition(empathy n.)>
        """
        return "<Definition({name} {word_class}.)" \
            .format(word_class=self.word_class[:1], name=self.word.name)

    @property
    def part_of_speech(self):
        return self.word_class
