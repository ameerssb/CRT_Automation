from django.db import models

class Breakout(models.Model):
    currency_pair = models.CharField(max_length=10)  # e.g., 'EURUSD'
    breakout_time = models.DateTimeField()  # Timestamp when the breakout was detected
    alert_sent = models.BooleanField(default=False)  # Track if an alert has been sent

    def __str__(self):
        return f"{self.currency_pair} - {self.breakout_time}"

    class Meta:
        unique_together = ('currency_pair', 'breakout_time')  # Ensure no duplicate records

