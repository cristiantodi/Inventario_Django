from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, Cargo

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = [
#                      'id',
#                      'username',
#                     ]

# class CargoAdmin(admin.ModelAdmin):
#         list_display = [
#                      'id',
#                      'nombre',
#                     ]

# admin.site.register(User, UserAdmin)

# admin.site.register(Cargo, CargoAdmin)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = [
                    'id',
                    'nombre',
                    ]

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = ((None,{"fields": (
                        'username', 
                        'password', 
                        'cargo', 
                        'local'
                    ),
                }),('Personal Information', {"fields": (
                        'first_name',
                        'last_name', 
                        'email'
                    ),
                }),
    )
    list_display = [
                    'id',
                    'username',
                    'email',
                    'get_groups',
                    'local',
                    ]
    
    def get_groups(self, obj):
        return ", ".join([group.nombre for group in obj.cargo.all()])
    get_groups.short_description = 'cargo'