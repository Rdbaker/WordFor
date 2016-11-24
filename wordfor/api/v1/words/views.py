# -*- coding: utf-8 -*-
"""Word views."""
from flask import Blueprint, request, jsonify

from wordfor.api.errors import NotFoundError
from wordfor.api.v1.search.models import Word
from wordfor.api.v1.search.schema import WordSchema

blueprint = Blueprint('word', __name__, url_prefix='/api/v1/words')
WORD_SCHEMA = WordSchema()


@blueprint.route('/', methods=['GET'], strict_slashes=False)
def list_words():
    """List words."""
    page = Word.query.paginate(page=int(request.args.get('page', 1)),
                               per_page=int(request.args.get('per_page', 10)))
    meta_pagination = {
        'first': request.path + '?page={page}&per_page={per_page}'.format(
            page=1, per_page=page.per_page),
        'next': request.path + '?page={page}&per_page={per_page}'.format(
            page=page.next_num, per_page=page.per_page),
        'last': request.path + '?page={page}&per_page={per_page}'.format(
            page=page.pages, per_page=page.per_page),
        'prev': request.path + '?page={page}&per_page={per_page}'.format(
            page=page.prev_num, per_page=page.per_page),
        'total': page.pages
    }
    if not page.has_next:
        meta_pagination.pop('next')
    if not page.has_prev:
        meta_pagination.pop('prev')
    return jsonify(data=WORD_SCHEMA.dump(page.items, many=True).data,
                   meta={'pagination': meta_pagination})


@blueprint.route('/<string:word_name>', methods=['GET'], strict_slashes=False)
def find_word(word_name):
    """Find a specific word."""
    word = Word.query.filter(Word.name == word_name).first()
    if word is not None:
        return jsonify(WORD_SCHEMA.dump(word).data)
    else:
        raise NotFoundError
