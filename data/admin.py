from django.contrib import admin
from .models import Snt, LandPlot, ChairMan, Owner
from .models import ElectricMeter

# Register your models here.
admin.site.register(Snt)
admin.site.register(LandPlot)
admin.site.register(ChairMan)
admin.site.register(Owner)
admin.site.register(ElectricMeter)
#admin.site.register(ElectricMeterReadings)
#admin.site.register(Tarrifs)
