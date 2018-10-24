from django.urls import path
from .views import (Login, Logout, user_follow, update_profile, Signup, home, history_events, profile_page, detail_event, book_event, my_events, booked_events, public_events, no_access, create_event, update_event, delete_event)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', home, name='home'),
	path('dashboard/<int:user_id>/', my_events, name='my-events'),
	path('history/<int:user_id>/', history_events, name='history-events'),
	path('booked/', booked_events, name='booked-events'),
	path('events/', public_events, name='public-events'),
	path('create/', create_event, name='create-event'),
	path('update/<int:event_id>/', update_event, name='update-event'),
	path('userprofile/<int:user_id>/', profile_page, name='user-profile'),
	path('updateprofile/<int:user_id>/', update_profile, name='update-profile'),
	path('delete/<int:event_id>/', delete_event, name='delete-event'),
	path('book/<int:event_id>/', book_event, name='book-event'),
	path('profile/<int:user_id>/follow/', user_follow ,name='profile-follow'),
	path('detail/<int:event_id>/', detail_event, name='detail-event'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('no-access/',no_access ,name='no-access'),
]
