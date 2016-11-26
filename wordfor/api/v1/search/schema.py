# -*- coding: utf-8 -*-
"""Search schema."""
from marshmallow import Schema, fields, post_load, validates, post_dump
from marshmallow.exceptions import ValidationError


class SearchSchema(Schema):
    """API schema for a search (also called a query). This is both consumed and
    produced by the API."""

    id = fields.UUID(dump_only=True)
    query_string = fields.Str(required=True)
    answers = fields.Nested('AnswerSchema', many=True, dump_only=True)

    @validates('query_string')
    def validate_query(self, data):
        """Make sure that the query is at least two words."""
        if len(data.split()) < 2:
            raise ValidationError('Send at least two words so we can '
                                  'attempt a reverse lookup')

    @post_load
    def lowercase_query(self, item):
        """Make the query lowercase."""
        item['query_string'] = item['query_string'].lower()
        return item

    @post_dump(pass_many=True)
    def nullify_empty_answers(self, data, many):
        """Set the "answers" field to None instead of an empty list."""
        def nullify_if_necessary(data):
            if not data['answers']:
                data['answers'] = None

        if not many:
            nullify_if_necessary(data)
        else:
            map(nullify_if_necessary, data)
        return data

    class Meta:
        type_ = 'searches'
        strict = True


class AnswerSchema(Schema):
    """Read-only schema for an answer to a search query."""

    score = fields.Float(dump_only=True)
    word = fields.Nested('WordSchema', dump_only=True)
    runtime = fields.TimeDelta(precision='microseconds',
                               dump_to='runtime_microseconds', dump_only=True)

    class Meta:
        type_ = 'answers'


class WordSchema(Schema):
    """Read-only schema for a word model."""

    name = fields.Str(dump_only=True)
    definitions = fields.Nested('DefinitionSchema', dump_only=True, many=True)

    class Meta:
        type_ = 'words'


class DefinitionSchema(Schema):
    """Read-only schema for a definition to a word model."""

    word_class = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)

    class Meta:
        type_ = 'definitions'
