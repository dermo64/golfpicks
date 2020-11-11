from django.core.exceptions import ValidationError
from django.db import models

class Punter(models.Model):
    """Model representing a punter."""
    name = models.CharField(max_length=200, help_text='Enter the punters name')
    
    def __str__(self):
        """String for representing the Punter object."""
        return self.name

    class Meta:
        ordering = ['name']

class Event(models.Model):
    """Model representing a event."""
    name = models.CharField(max_length=200, help_text='Enter the Evetns name')
    external_id = models.IntegerField(help_text='Enter the golf channel event id')
    
    def __str__(self):
        """String for representing the Punter object."""
        return self.name

class Golfer(models.Model):
    """Model representing a golfer."""
    name = models.CharField(max_length=200, help_text='Enter the golfers name')
    
    def __str__(self):
        """String for representing the Punter object."""
        return self.name

    class Meta:
        ordering = ['name']

class Pick(models.Model):
    """Model representing a golfer."""
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True)
    punter = models.ForeignKey('Punter', on_delete=models.SET_NULL, null=True)
    picks = models.ManyToManyField(Golfer, help_text='Select golfer picks')
    
    class Meta:
        unique_together = ["event", "punter"]

    def __str__(self):
        """String for representing the Picks object."""
        s = f'Picks for {self.event}. Punter: {self.punter}. Picks: '
        for pick in self.picks.values():
            s+= pick['name'] + ', '
        return s[0:-2]
