from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="reservations")

    def __str__(self):
        return f"{self.user.email}, created_at: {self.created_at}"


class Actor(models.Model):
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=225)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=355)
    description = models.TextField(null=True, blank=True)
    actor = models.ManyToManyField(Actor, related_name="plays")
    genre = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField(verbose_name="Date and Time of Show")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.play.title}, {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tickets",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["row", "seat"],
                                    name="unique_ticket")
        ]

    def clean(self) -> None:
        if not (1 <= self.row <= self.performance.theatre_hall.rows):
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range:"
                        f" (1, {self.performance.theatre_hall.rows}):"
                    ]
                }
            )
        if not (1 <= self.seat <= self.performance.theatre_hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range:"
                        f"(1, {self.performance.theatre_hall.seats_in_row})"
                    ]
                }
            )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str = None,
        update_fields: list = None,
    ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.performance.play.title} row {self.row} seat {self.seat}"
