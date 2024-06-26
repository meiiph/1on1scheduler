# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CalendarCalendar(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendar_calendar'


class CalendarEvent(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    recurrence = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    attendee_limit = models.PositiveIntegerField(blank=True, null=True)
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendar_event'


class CalendarsCalendar(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_calendar'


class CalendarsCalendarGuests(models.Model):
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_calendar_guests'
        unique_together = (('calendar', 'user'),)


class CalendarsCalendarHosts(models.Model):
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_calendar_hosts'
        unique_together = (('calendar', 'user'),)


class CalendarsCalendarPendingGuests(models.Model):
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_calendar_pending_guests'
        unique_together = (('calendar', 'user'),)


class CalendarsCalendarPendingHosts(models.Model):
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_calendar_pending_hosts'
        unique_together = (('calendar', 'user'),)


class CalendarsEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    organizer = models.ForeignKey(AuthUser, models.DO_NOTHING)
    start_time = models.TimeField()
    calendar = models.ForeignKey(CalendarsCalendar, models.DO_NOTHING)
    duration = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'calendars_event'


class CalendarsEventAttendees(models.Model):
    event = models.ForeignKey(CalendarsEvent, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'calendars_event_attendees'
        unique_together = (('event', 'user'),)


class CalendarsInvitation(models.Model):
    meeting_datetime = models.DateTimeField()
    is_accepted = models.BooleanField()
    calendar = models.ForeignKey(CalendarCalendar, models.DO_NOTHING)
    recipient = models.ForeignKey(AuthUser, models.DO_NOTHING)
    sender = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='calendarsinvitation_sender_set')

    class Meta:
        managed = False
        db_table = 'calendars_invitation'


class ContactsContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'contacts_contact'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InvitationsInvitation(models.Model):
    meeting_datetime = models.DateTimeField()
    recipient = models.ForeignKey(AuthUser, models.DO_NOTHING)
    sender = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='invitationsinvitation_sender_set')
    calendar = models.ForeignKey(CalendarsCalendar, models.DO_NOTHING)
    is_accepted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'invitations_invitation'


class SchedulesSchedule(models.Model):
    date = models.DateField()
    busy_times = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'schedules_schedule'


class TokenBlacklistBlacklistedtoken(models.Model):
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
