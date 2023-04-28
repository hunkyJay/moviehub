# MovieHub

This is a  booking system of Movie ticket.  This system can always provide ticket of the latest and hottest movie for you to enjoy.
You can choose to login in the system as different roles including Customer, staff and administrator in the home page.

![welcome to moviehub](./imgs/welcome_to_moviehub.png)
## Login as a Customer
In the login page you can input your user name and password to login the system. If you do not have an account, you can click the register button and create your own account!!!
Then you enter the home page of Customer, where you can check the number of movies, your orders, your notification as well as Personal Profile. And on the right side of your page you, the menu bar will help to find what you want quickly.
![moviehub user](./imgs/moviehub_user.png)
##### Book your favorate movie
 In the movie booking page, you can find out what movies are showing and book the movie ticket. Click the "book" button and then choose the seat. 
![movie ticket bookinbg](./imgs/movie_ticket_booking.png)
You can reserve up to four seats at a time. Be sure that you have **bind your bank account** in your Profile page before you pay the bill. And you can check the order in Order History.
![select seats](./imgs/select_seats.png)



## Login as an administrator
##### Insert a staff
As an administrator, you can not only check the staff list but can also insert new staff in your system.
 ![add staff](./imgs/add_staff.png)
The system will automatically create the staff account number and password. Please remember them, and the staff can change the password in Profile. 
##### Insert a movie
In the page of movie information Manangement you can find out what movie are showing and add new movie.
![add movie](./imgs/add_movie.png)
You just need to need input the basic information including the name, duration, cast and so on, and then you can insert a new movie.<br>**Be careful: The maximum duration is 3 hours.**
![add movie info](./imgs/add_movie_info.png)






## Login as a Staff
As a staff, you can insert movie.

##### Release a new movie
In the release information page you can release a new session.![release movie](./imgs/release_movie.png)
Before that, you need to **create a new room**. In the Room management page, you can insert the room id and room size, and then insert a new room.![room management](./imgs/room_management.png)
To release a new movie, just insert the movie name, room ID, price and release time.<br> **Be careful: Release Time cannot be previous time.  There can be no other films in the three hours before and three hours after the release of the film**
![release show](./imgs/release_show.png)
##### Post an Announcement 
To inform your clients the latest release or other information, you can post an announcement. This announcement will be sent to all clients.
![post announcement](./imgs/post_announcement.png)
 
<br><br>
You can also check the list of the staff and orders, however as a staff, you do not have right to modify them.

##  How to run
##### Create table in your database.
Firstly in settings.py check the database name and the password, change that to your password and account.<br>
There are two way to init the database.<br>
The first way is: running the sql code in sql file.<br><br>
The second way is: <br>
<kbd>python manage.py makemigrations</kbd> <br>
<kbd>python manage.py migrate </kbd>


###### Install Dependency
Please ensure that you has install python3 and have upated your pip to the latest version.

<kbd>pip install django</kbd> <br>
<kbd>pip install pymysql</kbd> <br>
<kbd>pip install PIL</kbd> <br>
<kbd>pip install pillow</kbd> <br>

##### Running code
Run  <kbd>python manage.py migrate</kbd> in your terminal.<kbd>cmd</kbd> 

## Contributing


## Current contributors
- Renjie He
- Dong Tan
- Victor Guo
- Wizard Cheng
- Peddy Zong

If you would like to make improvements to the project, please contact us for permission to contribute. Feel free to dive in!
