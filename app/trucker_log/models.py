
from django.db import models
from django.contrib.auth import get_user_model


class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_used_hours = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_miles = models.IntegerField(default=0)
    driver = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"


class Stop(models.Model):
    STOP_TYPES = [
        ("fuel", "Fuel"),
        ("rest", "Rest"),
        ("pickup", "Pickup"),
        ("dropoff", "Dropoff"),
        ("other", "Other"),
    ]
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="stops"
    )
    location = models.CharField(max_length=255)
    stop_type = models.CharField(max_length=20, choices=STOP_TYPES)
    duration_minutes = models.IntegerField()
    remarks = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.stop_type.title()} at {self.location}"


class LogSheet(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="logsheets"
    )
    date = models.DateField()
    total_drive_time = models.FloatField(
        help_text="Hours driven"
    )
    total_on_duty_time = models.FloatField(
        help_text="Hours on duty (not driving)"
    )
    total_off_duty_time = models.FloatField(
        help_text="Hours off duty"
    )
    total_sleeper_berth_time = models.FloatField(
        help_text="Hours in sleeper berth"
    )
    miles_driven = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"LogSheet for {self.date} (Trip {self.trip_id})"


class DutyStatusChange(models.Model):
    STATUS_CHOICES = [
        ("off_duty", "Off Duty"),
        ("sleeper_berth", "Sleeper Berth"),
        ("driving", "Driving"),
        ("on_duty", "On Duty (not driving)")
    ]
    log_sheet = models.ForeignKey(
        LogSheet,
        on_delete=models.CASCADE,
        related_name="duty_status_changes"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.status} from {self.start_time} to {self.end_time}"
