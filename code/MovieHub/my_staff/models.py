from django.db import models
from datetime import datetime

# Seat model
class Seat(models.Model):
    release_id = models.IntegerField()
    room_id = models.IntegerField()
    row_id = models.IntegerField()
    column_id = models.IntegerField()
    is_available = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    def toDict(self):
        return {'id':self.id, 'release_id': self.release_id, 'room_id': self.room_id, 'row_id': self.row_id, 'column_id': self.column_id, 'is_available':self.is_available}

    class Meta:
        db_table = "Seat"


