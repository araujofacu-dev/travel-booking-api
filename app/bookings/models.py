from django.db import models

# Create your models here.
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    # "sub" claim from the Keycloak token: links the identity to business data
    keycloak_id = models.UUIDField(unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TourPackage(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="package_end_after_start",
            ),
            models.CheckConstraint(
                condition=Q(price__gt=0),
                name="package_price_positive",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.start_date})"


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="bookings"
    )
    package = models.ForeignKey(
        TourPackage, on_delete=models.PROTECT, related_name="bookings"
    )
    seats = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(seats__gt=0),
                name="booking_seats_positive",
            ),
        ]

    def __str__(self):
        return f"Booking #{self.pk} - {self.customer} - {self.package}"


class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    booking = models.ForeignKey(
        Booking, on_delete=models.PROTECT, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    external_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment #{self.pk} - {self.amount} ({self.status})"