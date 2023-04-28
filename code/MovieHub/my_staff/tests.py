from django.test import TestCase
from my_admin.models import Staff
from my_admin.models import Room
from my_admin.models import Movie
from my_admin.models import Announcement
from my_admin.models import Release
from my_admin.models import Order
from my_staff.models import Seat
from datetime import datetime, timedelta

#Test the model of staff
class ModelTest(TestCase):
    # test initialization

    def test_seat_model(self):
        Seat.objects.create(id=1, release_id=123123, room_id=1, row_id=3, column_id=4, is_available=0)
        result = Seat.objects.get(release_id=123123, row_id=3, column_id=4)
        self.assertEqual(result.room_id, 1)
        self.assertEqual(result.is_available, 0)

#Test the login function of staff
class StaffLoginTest(TestCase):
    def setUp(self):
        Staff.objects.create(staff_id=87654321, password_hash='b854bef1d3d0149616db267002fad7cd',
                             password_salt='7654321', name='Victor', level=0, phone=987654321,
                             email='test@361.com')

    def test_login_success(self):
        session = self.client.session
        session['verifyCode'] = '2333'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/my_staff/login',
                                    {'staffId': '87654321', 'password': '7654321', 'verifyCode': '2333'})
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):  # password is incorrect
        session = self.client.session
        session['verifyCode'] = '2333'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/my_staff/login',
                                    {'staffId': '87654321', 'password': '1234567', 'verifyCode': '2333'})
        self.assertIn(b'password is incorrect', response.content)

#Test staff's function to manage released movies.
class ReleaseManagement(TestCase):

    def setUp(self):
        Release.objects.create(release_id=12345678, movie_id=22222222, room_id=1, price=20, release_time=datetime.now(),
                               is_delete=0)
        Room.objects.create(room_id=1, row_size=9, column_size=9)

    def test_delete_release_success(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        self.client.get('/my_staff/manage/delete/12345678')
        result = Release.objects.get(release_id=12345678)
        self.assertEqual(result.is_delete, 1)

#Test staff's function to release new movie
 #(That is, to decide when a certain movie will be shown.)
class ReleaseInformation(TestCase):

    def setUp(self):
        Movie.objects.create(movie_id=12345678, movie_name="avatar", duration=120, type="adventure",
                             cast="Sam Worthington", introduction="this is a good movie")
        createTime = datetime.now()
        updateTime = createTime
        Room.objects.create(room_id=1, row_size=9, column_size=9, create_time=createTime, update_time=updateTime)

    def test_release_movie_success(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/release/insert',
                                    {'movieId': '12345678', 'roomId': '1', 'price': '2',
                                     'releaseTime': '2023-02-21T19:28'})
        self.assertIn(b'Release new movie successfully', response.content)

    def test_release_movie_fail(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/release/insert',
                                    {'movieId': '12345678', 'roomId': '155', 'price': '2',
                                     'releaseTime': '2023-02-21T19:28'})
        self.assertIn(b'Room ID dose not exist, releasing new movie fails', response.content)

#Test the staff function: add new room to the cinema.
class RoomManagementTest(TestCase):
    def setUp(self):
        Room.objects.create(room_id=1, row_size=5, column_size=5, create_time=datetime.now(),
                            update_time=datetime.now())

    def test_add_room_success(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/room/insert', {'roomId': '2', 'rowSize': '5', 'columnSize': '5'})
        self.assertIn(b'Add new room successfully', response.content)

#Test the staff's function to manage the existing movie resources of the cinema.
class MovieManagement(TestCase):
    def setUp(self):
        Movie.objects.create(movie_id=12345678, movie_name="avatar", duration=120, type="adventure",
                             cast="Sam Worthington", introduction="this is a good movie")
        releaseTime = datetime.now() + timedelta(days=7)
        Release.objects.create(release_id=12345678, movie_id=12345678, room_id=1, price=20, release_time=releaseTime,
                               is_delete=0)
        Order.objects.create(order_id=12345678, customer_username="Anthony", room_id=1, seat_content='seat1-4 seat2-4',
                             movie_name='Avatar', release_id=12345678,
                             seat_num=2, price=100, is_cancel=0, release_time=datetime.now())

    def test_add_movie_fail(self):  # no poster
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/movie/insert',
                                    {'name': 'avatar', 'duration': '5', 'type': 'Love',
                                     'cast': 'Sam Worthington', 'introduction': 'this is a good movie'})
        self.assertIn(b'Add new movie fails,no poster upload', response.content)

#Test the ajax function in the staff page
    #staff click the release ID to check how many people have booked this movie.
    def test_check_release_order(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/release/checkOrderNum/12345678')
        self.assertIn(b'{"number": 1}', response.content)

#Test staff's function about publish and manage announcements.
class AnnouncementManagement(TestCase):

    def setUp(self):
        Announcement.objects.create(announcement_id=12345678, content='Avatar is coming')
        Announcement.objects.create(announcement_id=23456789, content='Avatar is coming')

    def test_add_announcement_success(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/announcement/insert',
                                    {'content': 'Avatar is coming'})
        self.assertIn(b'Post announcement successfully', response.content)

    def test_delete_movie(self):
        session = self.client.session
        session['staffuser'] = 'staffuser'
        session.save()
        self.client.get('/my_staff/announcement/delete/23456789')
        num = Announcement.objects.all().__len__()
        self.assertEqual(num, 1)
