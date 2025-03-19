from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CafeteriaMenu, 
    BusRoute, 
    bus_schedule,
    Faculty, 
    Course, 
    ClassSchedule, 
    Club, 
    Event, 
    CampusBuilding
)

class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'updated_at')
    search_fields = ('title', 'date')

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'role', 'id_number', 'level', 'term', 'is_admin')
    search_fields = ('email', 'name', 'role', 'id_number', 'level', 'term')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ('is_admin', 'role', 'level', 'term')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'id_number', 'level', 'term', 'contact_information')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'id_number', 'level', 'term', 'contact_information', 'password1', 'password2')}
        ),
    )

    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CafeteriaMenu)
admin.site.register(BusRoute)
admin.site.register(bus_schedule, BusScheduleAdmin)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(ClassSchedule)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(CampusBuilding)
