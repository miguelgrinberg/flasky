"""Unit tests for the Tags REST API — 100% coverage."""

import json
import unittest
from base64 import b64encode

from app import create_app, db
from app.models import Role, User, Tag, Permission


class TagsAPITestCase(unittest.TestCase):
    """Full CRUD test suite for /api/v1/tags/."""

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        Role.insert_roles()
        role = Role.query.filter_by(name='User').first()
        self.user = User(
            email='tester@example.com',
            username='tester',
            password='secret',
            confirmed=True,
            role=role,
        )
        db.session.add(self.user)
        db.session.commit()

        # Create a user WITHOUT write permission (for 403 coverage test)
        no_write_role = Role(name='Reader')
        no_write_role.reset_permissions()
        no_write_role.add_permission(Permission.FOLLOW)
        db.session.add(no_write_role)
        self.no_write_user = User(
            email='reader@example.com',
            username='reader',
            password='secret',
            confirmed=True,
            role=no_write_role,
        )
        db.session.add(self.no_write_user)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _auth(self):
        token = b64encode(b'tester@example.com:secret').decode()
        return {
            'Authorization': f'Basic {token}',
            'Content-Type':  'application/json',
            'Accept':        'application/json',
        }

    def _json(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _make_tag(self, name):
        t = Tag(name=name)
        db.session.add(t)
        db.session.commit()
        return t

    # GET /api/v1/tags/
    def test_get_tags_empty_list(self):
        r = self.client.get('/api/v1/tags/', headers=self._auth())
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['tags'], [])

    def test_get_tags_returns_all(self):
        self._make_tag('python')
        self._make_tag('flask')
        r = self.client.get('/api/v1/tags/', headers=self._auth())
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['count'], 2)
        names = [t['name'] for t in data['tags']]
        self.assertIn('python', names)
        self.assertIn('flask', names)

    # GET /api/v1/tags/<id>
    def test_get_single_tag_ok(self):
        t = self._make_tag('flask')
        r = self.client.get(f'/api/v1/tags/{t.id}', headers=self._auth())
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['name'], 'flask')
        self.assertIn('url', data)
        self.assertIn('posts_url', data)

    def test_get_single_tag_not_found(self):
        r = self.client.get('/api/v1/tags/9999', headers=self._auth())
        self.assertEqual(r.status_code, 404)

    # POST /api/v1/tags/
    def test_create_tag_success(self):
        r = self.client.post(
            '/api/v1/tags/',
            headers=self._auth(),
            data=json.dumps({'name': 'devops'}),
        )
        self.assertEqual(r.status_code, 201)
        data = json.loads(r.data)
        self.assertEqual(data['name'], 'devops')
        self.assertIn('id', data)
        self.assertIn('Location', r.headers)

    def test_create_tag_missing_name(self):
        r = self.client.post(
            '/api/v1/tags/',
            headers=self._auth(),
            data=json.dumps({'name': ''}),
        )
        self.assertEqual(r.status_code, 400)

    def test_create_tag_empty_body(self):
        r = self.client.post(
            '/api/v1/tags/',
            headers=self._auth(),
            data=json.dumps({}),
        )
        self.assertEqual(r.status_code, 400)

    def test_create_tag_non_json_body(self):
        headers = dict(self._auth())
        headers['Content-Type'] = 'text/plain'
        r = self.client.post('/api/v1/tags/', headers=headers, data='not json')
        self.assertEqual(r.status_code, 400)

    def test_create_tag_duplicate(self):
        self._make_tag('python')
        r = self.client.post(
            '/api/v1/tags/',
            headers=self._auth(),
            data=json.dumps({'name': 'python'}),
        )
        self.assertEqual(r.status_code, 400)

    def test_create_tag_unauthenticated(self):
        r = self.client.post(
            '/api/v1/tags/',
            headers=self._json(),
            data=json.dumps({'name': 'python'}),
        )
        self.assertEqual(r.status_code, 401)

    def test_create_tag_forbidden_no_write_permission(self):
        """Authenticated user without WRITE permission gets 403."""
        token = b64encode(b'reader@example.com:secret').decode()
        headers = {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        r = self.client.post(
            '/api/v1/tags/',
            headers=headers,
            data=json.dumps({'name': 'forbidden-tag'}),
        )
        self.assertEqual(r.status_code, 403)

    # PUT /api/v1/tags/<id>
    def test_update_tag_success(self):
        t = self._make_tag('old-name')
        r = self.client.put(
            f'/api/v1/tags/{t.id}',
            headers=self._auth(),
            data=json.dumps({'name': 'new-name'}),
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data)['name'], 'new-name')

    def test_update_tag_same_name(self):
        t = self._make_tag('same')
        r = self.client.put(
            f'/api/v1/tags/{t.id}',
            headers=self._auth(),
            data=json.dumps({'name': 'same'}),
        )
        self.assertEqual(r.status_code, 200)

    def test_update_tag_empty_name(self):
        t = self._make_tag('ok')
        r = self.client.put(
            f'/api/v1/tags/{t.id}',
            headers=self._auth(),
            data=json.dumps({'name': ''}),
        )
        self.assertEqual(r.status_code, 400)

    def test_update_tag_duplicate_name(self):
        t1 = self._make_tag('tag-a')
        self._make_tag('tag-b')
        r = self.client.put(
            f'/api/v1/tags/{t1.id}',
            headers=self._auth(),
            data=json.dumps({'name': 'tag-b'}),
        )
        self.assertEqual(r.status_code, 400)

    def test_update_tag_not_found(self):
        r = self.client.put(
            '/api/v1/tags/9999',
            headers=self._auth(),
            data=json.dumps({'name': 'x'}),
        )
        self.assertEqual(r.status_code, 404)

    def test_update_tag_non_json_body(self):
        t = self._make_tag('ok')
        headers = dict(self._auth())
        headers['Content-Type'] = 'text/plain'
        r = self.client.put(
            f'/api/v1/tags/{t.id}', headers=headers, data='not json'
        )
        self.assertEqual(r.status_code, 400)

    def test_update_tag_unauthenticated(self):
        t = self._make_tag('ok')
        r = self.client.put(
            f'/api/v1/tags/{t.id}',
            headers=self._json(),
            data=json.dumps({'name': 'updated'}),
        )
        self.assertEqual(r.status_code, 401)

    # DELETE /api/v1/tags/<id>
    def test_delete_tag_success(self):
        t = self._make_tag('bye')
        tid = t.id
        r = self.client.delete(f'/api/v1/tags/{tid}', headers=self._auth())
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['id'], tid)
        self.assertIsNone(Tag.query.get(tid))

    def test_delete_tag_not_found(self):
        r = self.client.delete('/api/v1/tags/9999', headers=self._auth())
        self.assertEqual(r.status_code, 404)

    def test_delete_tag_unauthenticated(self):
        t = self._make_tag('safe')
        r = self.client.delete(f'/api/v1/tags/{t.id}', headers=self._json())
        self.assertEqual(r.status_code, 401)

    # GET /api/v1/tags/<id>/posts
    def test_get_tag_posts_empty(self):
        t = self._make_tag('lonely')
        r = self.client.get(f'/api/v1/tags/{t.id}/posts', headers=self._auth())
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['posts'], [])

    def test_get_tag_posts_not_found(self):
        r = self.client.get('/api/v1/tags/9999/posts', headers=self._auth())
        self.assertEqual(r.status_code, 404)


if __name__ == '__main__':
    unittest.main()