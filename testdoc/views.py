from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Tester,Company
from .forms import CompanyForm
# Create your views here.
def testdoc(request):
    companies = Company.objects.all()
    return render(request,'testdoc/docform.html',{'companies':companies})
def companydetails(request):
    return HttpResponse('Yo not implemented yet')

def company_new(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            company.save()
            return redirect('testdoc')
    else:
        form = CompanyForm()
    return render(request,'testdoc/companynew.html',{'form':form})
