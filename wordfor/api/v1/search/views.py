# -*- coding: utf-8 -*-
"""Search views."""
from flask import Blueprint, request

from wordfor.api.v1.search.models import Search
from wordfor.api.v1.search.schema import SearchSchema
from wordfor.extensions import db
from wordfor.lookup.seeker import Seeker

blueprint = Blueprint('search', __name__, url_prefix='/api/v1/searches')
SEARCH_SCHEMA = SearchSchema()


@blueprint.route('/', methods=['GET'], strict_slashes=False)
def list_searches():
    """List all searches."""
    return SEARCH_SCHEMA.dumps(Search.query.all(), many=True)


@blueprint.route('/<int:sid>', methods=['GET'])
def get_search_by_id(sid):
    """Get a specific search by its ID."""
    search = db.session.query(Search).get(sid)
    return SEARCH_SCHEMA.dumps(search)


@blueprint.route('/', methods=['POST'], strict_slashes=False)
def search():
    """Create a new search."""
    existing_search = Search.query \
        .filter(Search.query_string == request.json.get('query_string', '')
                .lower()).first()
    if existing_search is not None:
        search = existing_search
    else:
        search_data = SEARCH_SCHEMA.load(request.json)
        search = Search(**search_data.data)
        search.save()
        Seeker(search.id, search.query_string)
    return SEARCH_SCHEMA.dumps(search)
