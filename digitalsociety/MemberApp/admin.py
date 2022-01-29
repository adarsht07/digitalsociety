from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(House)
admin.site.register(Member)
admin.site.register(Notice)
admin.site.register(Event)
admin.site.register(Complain)
admin.site.register(Noticeview)
admin.site.register(Maintenance)
admin.site.register(LikeNotice)
admin.site.register(LikeEvent)
admin.site.register(Transaction)