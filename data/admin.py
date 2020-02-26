from django.contrib import admin
from .models import Snt, LandPlot, ChairMan, Owner
from .models import ElectricalCounter, ElectricityPayments, Rate

# Register your models here.
admin.site.register(Snt)
admin.site.register(LandPlot)
admin.site.register(ChairMan)
admin.site.register(Owner)
admin.site.register(ElectricalCounter)
# admin.site.register(ElectricityPayments)
admin.site.register(Rate)

# Override default -(dash) for empty field
admin.site.empty_value_display = ''

# Register admin classes for ElectricityPayments
@admin.register(ElectricityPayments)
class ElectricityPaymentsAdmin(admin.ModelAdmin):
    list_display = (
        'land_plot',
        'record_date',
        't1_cons',
        't2_cons',
        'record_status',
        't1_amount',
        't2_amount',
        'sum_tot',
        )
    list_filter = ('land_plot',)
