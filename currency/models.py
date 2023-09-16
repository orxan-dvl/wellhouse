from django.db import models



class CurrencyModel(models.Model):
    #Base currency is Euro

    try_rate = models.FloatField(verbose_name='TRY', null=True)    #Turkey
    rub_rate = models.FloatField(verbose_name='RUB', null=True)    #Russian
    usd_rate = models.FloatField(verbose_name='USD', null=True)    #Usa
    gbp_rate = models.FloatField(verbose_name='GBP', null=True)    #England
    pln_rate = models.FloatField(verbose_name='PLN', null=True)    #Poland
    nok_rate = models.FloatField(verbose_name='NOK', null=True)    #Norway
    kzt_rate = models.FloatField(verbose_name='KZT', null=True)    #Kazakh
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.updated_at)
    
    