# -*- coding: utf-8 -*-
"""Search views."""
from flask import Blueprint, request

from wordfor.api.v1.search.models import Search
from wordfor.api.v1.search.schema import SearchSchema

blueprint = Blueprint('search', __name__, url_prefix='/api/v1/searches')
SEARCH_SCHEMA = SearchSchema()


@blueprint.route('/', methods=['POST'], strict_slashes=False)
def search():
    """Create a new search."""
    search_data = SEARCH_SCHEMA.load(request.json)
    search = Search(**search_data.data)
    return SEARCH_SCHEMA.dumps(search)
