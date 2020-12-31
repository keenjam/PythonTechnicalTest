from django.db import models

class Bond(models.Model):
    isin = models.CharField(max_length=12, primary_key=True, help_text="International Securities Identification Number")
    size = models.IntegerField(help_text="Size of offering")
    currency = models.CharField(max_length=3, help_text="Currency of offering in ISO 4217 code format")
    maturity = models.DateField(auto_now=True, help_text="Date of maturity")
    lei = models.CharField(max_length=20, help_text="Legal Entity Field of institution in ISO 17442 code format")
    legal_name = models.CharField(max_length=50, null=True, blank=True, help_text="Legal name of financial institution")
