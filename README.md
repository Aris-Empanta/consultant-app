# User's Guide

A platform for booking appointments with registered lawyers and legal advisors, built in Django.

[View Live Web App](https://lawyer-appointment-app.onrender.com)

|Front Page|
|:-:|
|![front page](screenshots/front-page.webp)|

## Main Technologies

- Python
- Django
- PostgreSQL
- Redis (message broker)
- Django channels (websockets)
- Vanilla JavaScript

## Features

### Shortcuts

&nbsp;&nbsp;&nbsp;&nbsp;[Search Lawyers](#search-lawyers)\
&nbsp;&nbsp;&nbsp;&nbsp;[Login/Register](#loginregister)\
&nbsp;&nbsp;&nbsp;&nbsp;[Reset Password](#reset-password)\
&nbsp;&nbsp;&nbsp;&nbsp;[Lawyer's Info](#lawyers-info)\
&nbsp;&nbsp;&nbsp;&nbsp;[Lawyer's Available Hours](#lawyers-available-hours)\
&nbsp;&nbsp;&nbsp;&nbsp;[User Profile](#user-profile)\
&nbsp;&nbsp;&nbsp;&nbsp;[Book an Appointment](#book-an-appointment)\
&nbsp;&nbsp;&nbsp;&nbsp;[Messaging](#messaging)\
&nbsp;&nbsp;&nbsp;&nbsp;[Cancel Appointment](#cancel-appointment)

#### Search Lawyers
&nbsp;&nbsp;&nbsp;&nbsp;Any visitor of the app, authenticated or not, can browse through all the registered lawyers via a search bar which exists in most of the pages. The search result can be filtered by existing areas of expertise of the lawyer, and/or his/her name. By applying no filter, you can browse through all the registered lawyers. **Pagination** is applied of course:

|||
|:-:|:-:|
|![Home Page](screenshots/home-page.webp)|![Search Results](screenshots/search-results.webp)|

||
|:-:|
|![Pagination](screenshots/pagination.webp)|

#### Login/Register
&nbsp;&nbsp;&nbsp;&nbsp;A user can register with **username/password** or **google account**.

||
|:-:|
|![Login Screen](screenshots/login.webp)|

&nbsp;&nbsp;&nbsp;&nbsp;The user can choose between registering as a **client** or a **lawyer**.

|||
|:-:|:-:|
|![Login Screen](screenshots/question-specialty.webp)|![Register Screen](screenshots/register.webp)|

#### Reset password

&nbsp;&nbsp;&nbsp;&nbsp;In case a user has registered with username/password, he/she can reset the password if he/she forgot it.

|||
|:-:|:-:|
|![Forgot Password](screenshots/forgot-password.webp)|![Reset Password](screenshots/reset-password.webp)|

#### Lawyer's Info

&nbsp;&nbsp;&nbsp;&nbsp;If a user registers as a lawyer, he/she is redirected to a screen to add some informations regarding his/her qualifications as a lawyer/legal advisor.

||
|:-:|
|![Lawyer's Info Screen](screenshots/lawyer-info.webp)|

#### Lawyer's Available Hours

&nbsp;&nbsp;&nbsp;&nbsp;After the lawyer fills up his/her information, he/she is redirected to a page to choose the hours that he/she is available for the next 2 weeks, the appointments' duration and the breaks in between. Then, the algorithm generates the available appointments, which can be chosen by a client. 

||
|:-:|
|![Lawyer's Available Hours](screenshots/available-hours.webp)|

#### User Profile

&nbsp;&nbsp;&nbsp;&nbsp;Each user's profile looks different, depending on whether they are a client or a lawyer, and it further varies based on whether they are viewing their own profile or that of another user.
If a user check's someone else's profile it looks like this:
|Client's Profile|Lawyer's Profile|
|:-:|:-:|
|![Client's Profile](screenshots/client-profile.webp)|![Lawyer's Profile](screenshots/lawyer-profile.webp)|

&nbsp;&nbsp;&nbsp;&nbsp;And if a user check's his own profile ehile logged in it may look like this:
|Own Client's Profile|Own Lawyer's Profile|
|:-:|:-:|
|![Own Client's Profile](screenshots/own-client-profile.webp)|![Own Lawyer's Profile](screenshots/own-lawyer-profile.webp)|

&nbsp;&nbsp;&nbsp;&nbsp;In case the user is a lawyer, he/she can edit his info and his/her available hours from his profile page:

|Edit Info|Set available Hours|
|:-:|:-:|
|![Edit Info](screenshots/edit-lawyer-info.webp)|![Set available Hours](screenshots/set-available-hours.webp)|

#### Book an Appointment

&nbsp;&nbsp;&nbsp;&nbsp;An authenticated client can book an appointment with a lawyer. Once an appointment is booked, the lawyer receives a real-time notification via the **WebSocket** protocol using Django Channels and Redis as message broker.

|Book Appointment|Real Time Notification|
|:-:|:-:|
|![Book Appointment](screenshots/book-appointment.webp)|![Real Time Notification](screenshots/real-time-notification.webp)|

&nbsp;&nbsp;&nbsp;&nbsp;A lawyer can check all his booked appointments by clicking the link in his/her profile page, to navigate to the booked appointments page.

|Booked Appointments Link|Booked Appointments Page|
|:-:|:-:|
|![Booked Appointments Link](screenshots/booked-appointments-link.webp)|![Booked Appointments Page](screenshots/booked-appointments-page.webp)|

#### Messaging

&nbsp;&nbsp;&nbsp;&nbsp;Any authenticated user can send real-time messages to another user via the **WebSocket** protocol using the Django Channels library and Redis as message broker.

|Message notification|Messages Page|
|:-:|:-:|
|![Edit Info](screenshots/message-notification.webp)|![Set available Hours](screenshots/messages-page.webp)|

#### Cancel Appointment

&nbsp;&nbsp;&nbsp;&nbsp;Any of both parties can cancel an appointment. If so, a real time automated chat message is sent to the other party.

|Cancel Appointment|Automated Message|
|:-:|:-:|
|![Edit Info](screenshots/cancel-appointment.webp)|![Set available Hours](screenshots/automated-message.webp)|