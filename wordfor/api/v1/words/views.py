# -*- coding: utf-8 -*-
"""Word views."""
from flask import Blueprint

from wordfor.api.errors import NotFoundError
from wordfor.api.v1.search.models import Word
from wordfor.api.v1.search.schema import WordSchema

blueprint = Blueprint('word', __name__, url_prefix='/api/v1/words')
WORD_SCHEMA = WordSchema()


@blueprint.route('/', methods=['GET'], strict_slashes=False)
def list_words():
    """List words."""
    return WORD_SCHEMA.dumps(Word.query.all(), many=True)


@blueprint.route('/<string:word_name>', methods=['GET'], strict_slashes=False)
def find_word(word_name):
    """Find a specific word."""
    word = Word.query.filter(Word.name == word_name).first()
    if word is not None:
        return WORD_SCHEMA.dumps(word)
    else:
        raise NotFoundError
