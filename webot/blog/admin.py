from django.contrib import admin
from blog.models import Config_Search,Config_Task,Config_Update,Scan_Progress,Time_Diff,Config_Mangers,Config_Topic

admin.site.register(Config_Search)
admin.site.register(Config_Mangers)
admin.site.register(Config_Topic)
admin.site.register(Config_Update)
admin.site.register(Config_Task)
admin.site.register(Scan_Progress)
admin.site.register(Time_Diff)
