from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=60)
    company_type = models.CharField(max_length=50)
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Tester(models.Model):
    name = models.CharField(max_length=60)
    designation = models.CharField(max_length=100)
    companyid = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppInfo(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=10)
    platform = models.CharField(max_length=50)
    osver = models.CharField(max_length=10)
    companyid = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Test(models.Model):
    testname = models.CharField(max_length=100)
    summary = models.TextField()
    steps = models.TextField()
    result_expected = models.TextField()
    actual_excepted = models.TextField()
    status = models.CharField(max_length=10)
    appid = models.ForeignKey(AppInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.testname
