from sqlalchemy import func
from app.models import Post, Comment

class PostService:
    @staticmethod
    def get_filtered_posts(search_query=None, sort_by='latest'):
        """Service method for filtering and sorting posts."""
        query = Post.query

        if search_query:
            query = query.filter(Post.body.ilike(f'%{search_query}%'))

        if sort_by == 'oldest':
            query = query.order_by(Post.timestamp.asc())
        elif sort_by == 'popular':
            # Perform outerjoin to preserve posts with 0 comments
            query = query.outerjoin(Comment).group_by(Post.id).order_by(func.count(Comment.id).desc())
        else:
            query = query.order_by(Post.timestamp.desc())

        return query