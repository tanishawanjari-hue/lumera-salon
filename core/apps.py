from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.models import User, Group

        try:
            admin.site.unregister(User)
        except admin.sites.NotRegistered:
            pass

        try:
            admin.site.unregister(Group)
        except admin.sites.NotRegistered:
            pass