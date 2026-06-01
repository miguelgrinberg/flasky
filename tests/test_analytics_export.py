import unittest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Role, Post, Comment
from app.services import PostService
from app.services import ExportContext, JSONExportStrategy, CSVExportStrategy


class AnalyticsAndExportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

        self.user1 = User(email='user1@example.com', username='user1', password='cat', confirmed=True)
        self.user2 = User(email='user2@example.com', username='user2', password='dog', confirmed=True)
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        now = datetime.utcnow()
        self.post_old = Post(body='Old post about Python Flask development', author=self.user1,
                             timestamp=now - timedelta(days=2))
        self.post_new = Post(body='New post about architectural patterns in programming', author=self.user2,
                             timestamp=now)
        self.post_popular = Post(body='Popular post: SQL database discussion', author=self.user1,
                                 timestamp=now - timedelta(days=1))

        db.session.add_all([self.post_old, self.post_new, self.post_popular])
        db.session.commit()

        comment1 = Comment(body='Agreed with author', post=self.post_popular, author=self.user2, timestamp=now)
        comment2 = Comment(body='Interesting thought', post=self.post_popular, author=self.user2,
                           timestamp=now + timedelta(minutes=5))
        db.session.add_all([comment1, comment2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_keyword(self):
        """Test post filtering by keyword."""
        query = PostService.get_filtered_posts(search_query='Python')
        posts = query.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].body, 'Old post about Python Flask development')

        query_all = PostService.get_filtered_posts(search_query='post')
        self.assertEqual(query_all.count(), 3)

    def test_sorting_latest_and_oldest(self):
        """Test sorting by timestamp (latest / oldest)."""
        query_latest = PostService.get_filtered_posts(sort_by='latest')
        posts_latest = query_latest.all()
        self.assertEqual(posts_latest[0].id, self.post_new.id)
        self.assertEqual(posts_latest[2].id, self.post_old.id)

        query_oldest = PostService.get_filtered_posts(sort_by='oldest')
        posts_oldest = query_oldest.all()
        self.assertEqual(posts_oldest[0].id, self.post_old.id)
        self.assertEqual(posts_oldest[2].id, self.post_new.id)

    def test_sorting_by_popularity(self):
        """Test sorting by comments count."""
        query_popular = PostService.get_filtered_posts(sort_by='popular')
        posts_popular = query_popular.all()
        self.assertEqual(posts_popular[0].id, self.post_popular.id)

    def test_json_export_multiple_posts_without_comments(self):
        """Test that bulk JSON export excludes comments for performance scaling."""
        posts = [self.post_new, self.post_popular]
        context = ExportContext(JSONExportStrategy())
        json_bytes = context.execute_export(posts)

        data = json.loads(json_bytes.decode('utf-8'))
        self.assertEqual(len(data), 2)
        self.assertNotIn('comments', data[0])
        self.assertNotIn('comments', data[1])

    def test_json_export_single_post_with_nested_comments(self):
        """Test hierarchical JSON structure with nested comments for a single post."""
        posts = [self.post_popular]
        context = ExportContext(JSONExportStrategy())
        json_bytes = context.execute_export(posts)

        data = json.loads(json_bytes.decode('utf-8'))
        self.assertEqual(len(data), 1)
        self.assertIn('comments', data[0])
        self.assertEqual(len(data[0]['comments']), 2)
        self.assertEqual(data[0]['comments'][0]['body'], 'Agreed with author')
        self.assertEqual(data[0]['comments'][1]['body'], 'Interesting thought')

    def test_csv_export_format(self):
        """Test header format and CSV exporter structure."""
        posts = [self.post_new]
        context = ExportContext(CSVExportStrategy())
        csv_bytes = context.execute_export(posts)

        csv_text = csv_bytes.decode('utf-8')
        lines = csv_text.strip().split('\n')

        self.assertIn('ID,Author,Timestamp,Body', lines[0])
        self.assertIn('user2', lines[1])
        self.assertIn('New post about architectural patterns', lines[1])