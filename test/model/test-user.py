import os
import sys
import unittest
from hashlib import sha256
from flask import g
from sqlalchemy.exc import *

top_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(os.path.join(top_path))
import unittest
from flaskr import *
from flaskr.model.user import *

class UserTestCase(unittest.TestCase):
    def initdb(self):
        config = "flaskr.config.TestingConfig"
        app.config.from_object(config)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../flaskr/database/flaskr.db'

        db.metadata.drop_all(bind=db.engine)
        db.metadata.create_all(bind=db.engine)

    def setUp(self):
        self.initdb()

        self.tuser = {
            'u0':{'name':'user0','passwd':'user123','email':'user0@user0.com'},
            'u1':{'name':('user1'*10),'passwd':'user123','email':'user1@user1.com'},
            'u2':{'name':'','passwd':'user123','email':'user2@user2.com'},
            'u3':{'name':'user0','passwd':'user123','email':'user3@user3.com'},
            'u4':{'name':'user4','passwd':('user123'*10),'email':'user4@user4.com'},
            'u5':{'name':'user5','passwd':'','email':'user5@user5.com'},
            'u6':{'name':'user6','passwd':'user123','email':('user6@user6.com'*10)},
            'u7':{'name':'user7','passwd':'user123','email':'user0@user0.com'},
            'u8':{'name':'user8','passwd':'user123','email':''},
            }

    def test_create_user(self):
        self.initdb()

        tuser = self.tuser
        # user0
        user0 = User(tuser['u0']['name'],tuser['u0']['passwd'],tuser['u0']['email'])
        self.assertEqual(user0.name, tuser['u0']['name'])
        self.assertEqual(user0.password, sha256(tuser['u0']['passwd']).hexdigest())
        self.assertEqual(user0.email, tuser['u0']['email'])
        self.assertEqual(user0.delflag, False)
        self.assertEqual(user0.entries,[])
        self.assertEqual(user0.store_to_db(), None)
        self.assertEqual(User.get_from_username(tuser['u0']['name']),user0)

        # # user1 Too long...
        # user1 = User(tuser['u1']['name'],tuser['u1']['passwd'],tuser['u1']['email'])
        # self.assertEqual(user1.name, tuser['u1']['name'])
        # self.assertEqual(user1.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u1']['name']),user1)

        # # user2 None
        # user2 = User(tuser['u2']['name'],tuser['u2']['passwd'],tuser['u2']['email'])
        # self.assertEqual(user2.name, tuser['u2']['name'])
        # self.assertEqual(user2.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u2']['name']),user2)

        # user3 Not unique
        user3 = User(tuser['u3']['name'],tuser['u3']['passwd'],tuser['u3']['email'])
        self.assertEqual(user3.name, tuser['u3']['name'])
        self.assertRaises(SQLAlchemyError, user3.store_to_db)
        self.assertNotEqual(User.get_from_username(tuser['u3']['name']),user3)
        db.session.rollback()

        # # user4 Too long...
        # user4 = User(tuser['u4']['name'],tuser['u4']['passwd'],tuser['u4']['email'])
        # self.assertEqual(user4.password, sha256(tuser['u4']['passwd']).hexdigest())
        # self.assertEqual(user4.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u4']['name']),user4)

        # # user5 None...
        # user5 = User(tuser['u5']['name'],tuser['u5']['passwd'],tuser['u5']['email'])
        # self.assertEqual(user5.password, sha256(tuser['u5']['passwd']).hexdigest())
        # self.assertEqual(user5.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u5']['name']),user5)

        # # user6 Too long...
        # user6 = User(tuser['u6']['name'],tuser['u6']['passwd'],tuser['u6']['email'])
        # self.assertEqual(user6.email, tuser['u6']['email'])
        # self.assertEqual(user6.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u6']['name']),user6)

        # user7 Not unique
        user7 = User(tuser['u7']['name'],tuser['u7']['passwd'],tuser['u7']['email'])
        self.assertEqual(user7.email, tuser['u7']['email'])
        self.assertRaises(SQLAlchemyError, user7.store_to_db)
        self.assertNotEqual(User.get_from_username(tuser['u7']['name']),user7)
        db.session.rollback()

        # # user8 None
        # user8 = User(tuser['u8']['name'],tuser['u8']['passwd'],tuser['u8']['email'])
        # self.assertEqual(user8.email, tuser['u8']['email'])
        # self.assertEqual(user8.store_to_db(), None)
        # self.assertEqual(User.get_from_username(tuser['u8']['name']),user8)

    def test_delete_user(self):
        self.initdb()

        tuser = self.tuser

        # user0 Right
        user0 = User(tuser['u0']['name'],tuser['u0']['passwd'],tuser['u0']['email'])
        user0.store_to_db()
        self.assertEqual(user0.delflag, False)
        user0.delete_from_db()
        self.assertEqual(user0.delflag, True)

        # user3 Not unique
        user3 = User('user3',tuser['u3']['passwd'],tuser['u3']['email'])
        user3.store_to_db()
        user3.name = tuser['u3']['name']
        self.assertRaises(SQLAlchemyError, user3.delete_from_db)
        db.session.rollback()

        # user7 Not unique
        user7 = User(tuser['u7']['name'],tuser['u7']['passwd'],'user7@user7.com')
        user7.store_to_db()
        user7.email = tuser['u7']['email']
        self.assertRaises(SQLAlchemyError, user7.delete_from_db)
        db.session.rollback()

    def test_update_user(self):
        pass

    def tearDown(self):
        self.initdb()
        admin = User("admin", "admin123", "admin@example.com")
        admin.store_to_db()
        db.session.close()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UserTestCase))
    return suite

if __name__=='__main__':
    unittest.main(defaultTest='suite')

