from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField


class Positions(ChoiceEnum):
    goalkeeper = "goalkeeper"
    centre_back = "centre-back"
    sweeper = "sweeper"
    full_back = "full-back"
    wing_back = "wing-back"
    centre_midfield = "centre-midfield"
    defensive_midfield = "defensive-midfield"
    attacking_midfield = "attacking-midfield"
    wide_midfield = "wide-midfield"
    centre_forward = "centre-forward"
    second_striker = "second-striker"
    winger = "winger"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Positions))

    def __str__(self):
        return self.name


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=50)
    oib = models.CharField(max_length=11)

    def __str__(self):
        return self.club_name


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    best_position = EnumChoiceField(Positions, default=Positions.goalkeeper)
    last_modified = models.DateTimeField(auto_now=True)
    manager_id = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    club_id = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['last_modified']
