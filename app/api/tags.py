"""
REST API endpoints for the Tags resource.

Endpoints
---------
GET    /api/v1/tags/           – list all tags
POST   /api/v1/tags/           – create a tag  (auth required)
GET    /api/v1/tags/<id>       – get one tag
PUT    /api/v1/tags/<id>       – update a tag  (auth required)
DELETE /api/v1/tags/<id>       – delete a tag  (auth required)
GET    /api/v1/tags/<id>/posts – list posts for a tag
"""

from flask import jsonify, request, url_for, current_app
from .. import db
from ..models import Tag, Post, Permission
from . import api
from .errors import bad_request
from functools import wraps
from flask import g, abort
from .authentication import auth

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@api.route('/tags/', methods=['GET'])
def get_tags():
    """Return all tags as a JSON list."""
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify({'tags': [t.to_json() for t in tags], 'count': len(tags)})


@api.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    """Return a single tag by its ID. Returns 404 if not found."""
    tag = Tag.query.get_or_404(id)
    return jsonify(tag.to_json())


@api.route('/tags/<int:id>/posts', methods=['GET'])
def get_tag_posts(id):
    """Return all posts that carry this tag (paginated)."""
    tag  = Tag.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per  = current_app.config.get('FLASKY_POSTS_PER_PAGE', 20)
    pag  = tag.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per, error_out=False
    )
    prev = url_for('api.get_tag_posts', id=id, page=page - 1, _external=True) \
           if pag.has_prev else None
    nxt  = url_for('api.get_tag_posts', id=id, page=page + 1, _external=True) \
           if pag.has_next else None
    return jsonify({
        'posts': [p.to_json() for p in pag.items],
        'prev':  prev,
        'next':  nxt,
        'count': pag.total,
    })


@api.route('/tags/', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def new_tag():
    """Create a new tag. Returns 201 on success, 400 on bad input."""
    data = request.get_json(silent=True)
    if data is None:
        return bad_request('Request body must be JSON.')
    name = (data.get('name') or '').strip()
    if not name:
        return bad_request('Tag must have a name.')
    if Tag.query.filter_by(name=name).first():
        return bad_request('A tag with that name already exists.')
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return (
        jsonify(tag.to_json()),
        201,
        {'Location': url_for('api.get_tag', id=tag.id, _external=True)},
    )


@api.route('/tags/<int:id>', methods=['PUT'])
@auth.login_required
@permission_required(Permission.WRITE)
def edit_tag(id):
    """Update a tag's name. Returns 200, 400, or 404."""
    tag  = Tag.query.get_or_404(id)
    data = request.get_json(silent=True)
    if data is None:
        return bad_request('Request body must be JSON.')
    name = (data.get('name') or '').strip()
    if not name:
        return bad_request('Tag must have a name.')
    clash = Tag.query.filter_by(name=name).first()
    if clash and clash.id != id:
        return bad_request('A tag with that name already exists.')
    tag.name = name
    db.session.commit()
    return jsonify(tag.to_json())


@api.route('/tags/<int:id>', methods=['DELETE'])
@auth.login_required
@permission_required(Permission.WRITE)
def delete_tag(id):
    """Delete a tag. Returns 200 or 404."""
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted successfully.', 'id': id})