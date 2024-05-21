from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Recommendation)
admin.site.register(Comment)
admin.site.register(Accommodation)
admin.site.register(Internship)
admin.site.register(Transport)
admin.site.register(Reservation)
admin.site.register(ClubEvent)
admin.site.register(SocialEvent)
admin.site.register(Notifications)