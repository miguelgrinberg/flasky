import unittest
import time
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='kissa')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='kissa')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='kissa')
        self.assertTrue(u.verify_password('kissa'))
        self.assertFalse(u.verify_password('koira'))

    def test_password_salts_are_random(self):
        u = User(password='kissa')
        u2 = User(password='kissa')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='kissa')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='kissa')
        u2 = User(password='koira')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='kissa')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
