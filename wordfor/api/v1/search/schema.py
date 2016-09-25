# -*- coding: utf-8 -*-
"""Search schema."""
from marshmallow import Schema, fields, post_load, validates
from marshmallow.exceptions import ValidationError


class SearchSchema(Schema):
    id = fields.Integer(dump_only=True)
    query = fields.Str(required=True)
    answers = fields.Nested('AnswerSchema', many=True, dump_only=True)

    @validates('query')
    def validate_query(self, data):
        """Make sure that the query is at least two words."""
        if data.split() < 2:
            raise ValidationError('Send at least two words so we can ' +
                                  'attempt a reverse lookup')

    @post_load
    def lowercase_query(self, item):
        """Make the query lowercase."""
        item['query'] = item['query'].lower()
        return item

    class Meta:
        type_ = 'searches'
        strict = True


class AnswerSchema(Schema):
    """Read-only schema for an answer to a search query."""
    score = fields.Float(dump_only=True)
    word = fields.Nested('WordSchema', dump_only=True)

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
