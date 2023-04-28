from django.test import TestCase
from my_admin.models import Staff
from my_admin.models import Room
from my_admin.models import Movie
from my_admin.models import Announcement
from my_admin.models import Release
from my_admin.models import Customer
from my_admin.models import Order
from datetime import datetime, timedelta

#Test the model of Admin
class ModelTest(TestCase):
    # test initialization
    def test_staff_model(self):
        Staff.objects.create(staff_id=23452345, password_hash='b965bef1d3d0149616db267002fad7cd',
                             password_salt='1234567', name='Tony', level=0, phone=123456789,
                             email='test@163.com')
        result = Staff.objects.get(staff_id=23452345)
        self.assertEqual(result.staff_id, 23452345)
        self.assertEqual(result.level, 0)

    def test_room_model(self):
        Room.objects.create(room_id=1, row_size=5, column_size=5)
        result = Room.objects.get(room_id=1)
        self.assertEqual(result.row_size, 5)
        self.assertEqual(result.column_size, 5)

    def test_movie_model(self):
        Movie.objects.create(movie_id=12345678, movie_name="avatar", duration=120, type="adventure",
                             cast="Sam Worthington", introduction="this is a good movie")
        result = Movie.objects.get(movie_id=12345678)
        self.assertEqual(result.movie_name, 'avatar')
        self.assertEqual(result.duration, 120)

    def test_announcement_model(self):
        Announcement.objects.create(announcement_id=12345678, content='Avatar is coming')
        result = Announcement.objects.get(announcement_id=12345678)
        self.assertEqual(result.content, 'Avatar is coming')

    def test_release_mode(self):
        Release.objects.create(release_id=12345678, movie_id=22222222, room_id=1, price=20, release_time=datetime.now(),
                               is_delete=0)
        result = Release.objects.get(release_id=12345678)
        self.assertEqual(result.movie_id, 22222222)
        self.assertEqual(result.price, 20)

    def test_customer_model(self):
        Customer.objects.create(username="AnthonyTan", password_hash='b965bef1d3d0149616db267002fad7cd',
                                password_salt='1234567', name='Anthony', phone=123456789,
                                email='test@163.com', bank_card=1234)
        result = Customer.objects.get(username='AnthonyTan')
        self.assertEqual(result.name, 'Anthony')
        self.assertEqual(result.email, 'test@163.com')
        self.assertEqual(result.bank_card, 1234)

    def test_order_model(self):
        Order.objects.create(order_id=12345678, customer_username="Anthony", room_id=1, seat_content='seat1-4 seat2-4',
                             movie_name='Avatar', release_id=22222222,
                             seat_num=2, price=100, is_cancel=0, release_time=datetime.now())
        result = Order.objects.get(order_id=12345678)
        self.assertEqual(result.customer_username, 'Anthony')
        self.assertEqual(result.price, 100)
        self.assertEqual(result.seat_num, 2)
        self.assertEqual(result.release_id, 22222222)

#Test the admin login function
class StaffLoginTest(TestCase):
    def setUp(self):
        Staff.objects.create(staff_id=12345678, password_hash='b965bef1d3d0149616db267002fad7cd',
                             password_salt='1234567', name='Anthony', level=2, phone=123456789,
                             email='test@163.com')

    def test_login_success(self):
        session = self.client.session
        session['verifyCode'] = '2332'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/my_admin/login',
                                    {'staffId': '12345678', 'password': '12345678', 'verifyCode': '2332'})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):  # password is incorrect
        session = self.client.session
        session['verifyCode'] = '2332'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/my_admin/login',
                                    {'staffId': '12345678', 'password': '1234567', 'verifyCode': '2332'})
        self.assertIn(b'password is incorrect', response.content)


    def test_update_info(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/staff/update/',
                                    {'staffId': '12345678', 'name': 'Anthony', 'password':'12345678','level': 'manager', 'phone': '13332323',
                                     'email': 'test@163.com'})
        self.assertIn(b'Update Successfully', response.content)

#Test the admin function: add new room to the cinema.
class RoomManagementTest(TestCase):
    def setUp(self):
        Room.objects.create(room_id=1, row_size=5, column_size=5, create_time=datetime.now(),
                            update_time=datetime.now())

    def test_add_room_success(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/room/insert', {'roomId': '2', 'rowSize': '5', 'columnSize': '5'})
        self.assertIn(b'Add new room successfully', response.content)

    def test_add_room_fail(self):  # existed room Id
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/room/insert', {'roomId': '1', 'rowSize': '5', 'columnSize': '5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add new room fails', response.content)

#Test the admin's function to manage the existing movie resources of the cinema.
class MovieManagement(TestCase):
    def setUp(self):
        Movie.objects.create(movie_id=12345678, movie_name="avatar", duration=120, type="adventure",
                             cast="Sam Worthington", introduction="this is a good movie")
        releaseTime = datetime.now() + timedelta(days=7)
        Release.objects.create(release_id=12345678, movie_id=12345678, room_id=1, price=20, release_time=releaseTime,
                               is_delete=0)

    def test_add_movie_fail(self):  # no poster
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/movie/insert',
                                    {'name': 'avatar', 'duration': '5', 'type': 'Love',
                                     'cast': 'Sam Worthington', 'introduction': 'this is a good movie'})
        self.assertIn(b'Add new movie fails,no poster upload', response.content)

    def test_update_movie_info_success(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/movie/update',
                                    {'movieId': '12345678', 'name': 'avatar', 'duration': '5', 'type': 'Love',
                                     'cast': 'Sam Worthington', 'introduction': 'this is a good movie'})
        self.assertIn(b'Update Successfully', response.content)
        result = Movie.objects.get(movie_id=12345678)
        self.assertEqual(result.type, 'Love')

    def test_check_release_movie(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/movie/checkReleaseNum/12345678')
        self.assertIn(b'{"number": 1}', response.content)

#Test admin's function about publish and manage announcements.
class AnnouncementManagement(TestCase):

    def setUp(self):
        Announcement.objects.create(announcement_id=12345678, content='Avatar is coming')
        Announcement.objects.create(announcement_id=23456789, content='Avatar is coming')

    def test_add_announcement_success(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        response = self.client.post('/my_admin/announcement/insert',
                                    {'content': 'Avatar is coming'})
        self.assertIn(b'Post announcement successfully', response.content)

    def test_delete_movie(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        self.client.get('/my_admin/announcement/delete/23456789')
        num = Announcement.objects.all().__len__()
        self.assertEqual(num, 1)

#Test admin's function to manage released movies.
class ReleaseManagement(TestCase):

    def setUp(self):
        Release.objects.create(release_id=12345678, movie_id=22222222, room_id=1, price=20, release_time=datetime.now(),
                               is_delete=0)

    def test_delete_release_success(self):
        session = self.client.session
        session['adminuser'] = 'adminuser'
        session.save()
        self.client.get('/my_admin/release/delete/12345678')
        result = Release.objects.get(release_id=12345678)
        self.assertEqual(result.is_delete, 1)

