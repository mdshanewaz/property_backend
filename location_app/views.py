from django.shortcuts import render

# Create your views here.

from location_app.models import DistrictModel

v = DistrictModel.objects.values_list('name', flat=True)

for d in v:
    print(d)