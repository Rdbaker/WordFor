# -*- coding: utf-8 -*-
"""Search views."""
from flask import Blueprint, request

from wordfor.api.v1.search.models import Search
from wordfor.api.v1.search.schema import SearchSchema
from wordfor.extensions import db

blueprint = Blueprint('search', __name__, url_prefix='/api/v1/searches')
SEARCH_SCHEMA = SearchSchema()


@blueprint.route('/<int:sid>', methods=['GET'])
def get_search_by_id(sid):
    """Get a specific search by its ID."""
    search = db.session.query(Search).get(sid)
    return SEARCH_SCHEMA.dumps(search)


@blueprint.route('/', methods=['POST'], strict_slashes=False)
def search():
    """Create a new search."""
    search_data = SEARCH_SCHEMA.load(request.json)
    search = Search(**search_data.data)
    search.save()
    return SEARCH_SCHEMA.dumps(search)
