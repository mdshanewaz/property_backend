from django.db import models

# Create your models here.

# Divisions of the country
class DivisionModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Districts under Divisions
class DistrictModel(models.Model):
    division = models.ForeignKey(DivisionModel, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('division', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.division.name}"

# Upazilas under Districts
# class UpazilaModel(models.Model):
#     district = models.ForeignKey(DistrictModel, on_delete=models.CASCADE, related_name='upazilas')
#     name = models.CharField(max_length=100)

#     class Meta:
#         unique_together = ('district', 'name')
#         ordering = ['name']

#     def __str__(self):
#         return f"{self.name}, {self.district.name}"

