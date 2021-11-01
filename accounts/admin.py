from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, InternationalTransfer, LocalTransfer, History, Contact

from .models import UpdateUser

# Register your models here.

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'first_name','middle_name', 'surname', 'sex', 'phone', 'security_question', 'security_answer', 'account_number', 'available_bal', 'status', 'password', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'first_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)

class UpdateUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'dob', 'owner', 'next_of_kin', 'passport', 'next_of_kin', 'date_updated')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(UpdateUser, UpdateUserAdmin)

class InternationalTransferAdmin(admin.ModelAdmin):

    list_display = ('id','to_fullname', 'to_account','transfer_amount', 'transfer_date', 'transaction_id','owner', 'status')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(InternationalTransfer, InternationalTransferAdmin)

class LocalTransferAdmin(admin.ModelAdmin):

    list_display = ('id', 'to_fullname', 'to_account', 'transfer_amount', 'transfer_date', 'transaction_id','owner', 'status')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(LocalTransfer, LocalTransferAdmin)


class HistoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'to_fullname', 'to_account', 'transaction_type', 'transaction_amount', 'transaction_description', 'transaction_id', 'transaction_date', 'status', 'owner')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(History, HistoryAdmin)

# Register your models here.
admin.site.site_header = 'Steplight Bank'
admin.site.site_title = 'Steplight Bank'
admin.site.index_title = 'Steplight Bank Admin'

class ContactAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'email', 'query')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)