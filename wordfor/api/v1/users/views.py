# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from flask_login import current_user, login_required

from wordfor.api.v1.users.models import User
from wordfor.api.v1.users.schema import UserSchema

blueprint = Blueprint('user', __name__, url_prefix='/api/v1/users')
USER_SCHEMA = UserSchema()


@blueprint.route('/')
@login_required
def users():
    """List members."""
    return USER_SCHEMA.dumps(User.query.all(), many=True).data


@blueprint.route('/me')
@login_required
def me():
    """List members."""
    return USER_SCHEMA.dumps(current_user).data
