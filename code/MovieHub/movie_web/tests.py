import datetime
from django.test import TestCase
from my_admin.models import Customer, Room
from my_admin.models import Movie
from my_admin.models import Announcement
from my_admin.models import Release
from my_admin.models import Customer
from my_admin.models import Order
from my_staff.models import Seat
# Create your tests here.


class CustomerLoginTest(TestCase):
    def setUp(self):
        Customer.objects.create(username="AnthonyTan", password_hash='3cceea5b8fb7d5ced3f0ea6162e83a7a',
                                password_salt='717604', name='Anthony', phone=123456789,
                                email='test@163.com', bank_card=1234)

    def test_login_success(self):
        session = self.client.session
        session['verifyCode'] = '2333'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/movie_web/login',
                                    {'username': 'AnthonyTan', 'password': '12345678', 'verifyCode': '2333'})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):  # password is incorrect
        session = self.client.session
        session['verifyCode'] = '2333'
        # session['csrfmiddlewaretoken'] = 'rg2eQEGY0Fs6LG6cgmXn6kc2NbsB4832UGkV8EXl7ms3QEDVmK0dsXrYL6BSseS4'
        session.save()
        response = self.client.post('/movie_web/login',
                                    {'username': 'AnthonyTan', 'password': '1234567', 'verifyCode': '2333'})
        self.assertIn(b'password is incorrect', response.content)


class CustomerRegisterTest(TestCase):
    def test_register_success(self):
        response = self.client.post('/movie_web/doRegister',
                                    {'username': 'AnthonyTan', 'password': '1234567', 'name': 'Tan',
                                     'email': 'hello@163.com', 'verifyCode': '2333'})
        self.assertEqual(response.status_code, 200)

    def test_register_fail(self):
        response = self.client.post('/movie_web/doRegister',
                                    {'username': 'AnthonyTan', 'password': '1234567', 'name': 'Tan',
                                     'email': 'hello', 'verifyCode': '2333'})
        self.assertIn(b'Email is invalid', response.content)


class MovieRelated(TestCase):
    # releaseId = ''
    def setUp(self):
        Movie.objects.create(movie_id=12345678, movie_name="avatar", duration=120, type="adventure",
                             cast="Sam Worthington", introduction="this is a good movie")
        Customer.objects.create(username="AnthonyTan", password_hash='3cceea5b8fb7d5ced3f0ea6162e83a7a',
                                password_salt='717604', name='Anthony', phone=123456789,
                                email='test@163.com', bank_card=1234)
        createTime = datetime.datetime.now()
        updateTime = createTime
        Room.objects.create(room_id=1, row_size=9, column_size=9,
                            create_time=createTime, update_time=updateTime)
        session = self.client.session
        ob = Customer.objects.get(username='AnthonyTan')
        session['logineduser'] = ob.toDict()
        session['staffuser'] = 'staffuser'
        session.save()
        response = self.client.post('/my_staff/release/insert',
                                    {'movieId': '12345678', 'roomId': '1', 'price': '2',
                                     'releaseTime': '2023-02-21T19:28'})

    # find all movies
    def test_browse_movie(self):
        response = self.client.get('/movie_web/movie/1')
        self.assertIn(b'avatar', response.content)

    # find release list
    def test_get_release_list(self):
        response = self.client.post('/movie_web/releaseList/1',
                                    {'movie_id': '12345678'})
        content = str(response.content)
        content = content[content.find('release_id') + 15:]
        # global releaseId
        # releaseId = content[:content.find(',')]
        # print('release_id:' + releaseId)
        self.assertIn(
            b'\\"movie_id\\": 12345678, \\"room_id\\": 1,', response.content)

    # view booking page and try to book a movie
    def test_loadBooking_and_book_movie(self):
        response = self.client.post('/movie_web/releaseList/1',
                                    {'movie_id': '12345678'})
        content = str(response.content)
        content = content[content.find('release_id') + 15:]
        releaseId = content[:content.find(',')]
        response = self.client.post('/movie_web/loadBooking/'+releaseId)
        self.assertIn(b'<span id=\'screen\'>', response.content)
        response = self.client.post('/movie_web/movie/book',
                                    {'seat_content': 'seat1-1', 'release_id': releaseId})
        self.assertIn(
            b'successfully booked, view details in the order page', response.content)
    # book a movie
    # def test_book_movie(self):
    #    param = {'roomId': 'seat1-1'}
    #   param['release_id'] = releaseId
    #    response = self.client.post('/movie_web/movie/book/',
    #                               param)
    #   self.assertIn(b'<span id=\'screen\'>', response.content)


class OrderRelated(TestCase):
    def setUp(self):
        Customer.objects.create(username="AnthonyTan", password_hash='3cceea5b8fb7d5ced3f0ea6162e83a7a',
                                password_salt='717604', name='Anthony', phone=123456789,
                                email='test@163.com', bank_card=1234)
        session = self.client.session
        ob = Customer.objects.get(username='AnthonyTan')
        session['logineduser'] = ob.toDict()
        session.save()
        createTime = datetime.datetime.now()
        updateTime = datetime.datetime.now()
        releaseTime = datetime.datetime.now()
        Order.objects.create(order_id=12345678, release_id=12345678, seat_num=1, movie_name="avatar", room_id=1, price=15, customer_username='AnthonyTan',
                             is_cancel=0,seat_content='seat1-1',create_time=createTime, update_time=updateTime, release_time=releaseTime)
        Seat.objects.create(release_id=12345678, is_available=1,
                            room_id=1, column_id=1, row_id=1)

        # find all movies
    def test_browse_order(self):
        response = self.client.get('/movie_web/order/1')
        self.assertIn(b'avatar', response.content)

    def test_cancel_order(self):
        response = self.client.post('/movie_web/order/cancel',{'order_id':12345678})
        self.assertIn(b'Successfully Canceled!', response.content)
