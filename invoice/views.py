from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem,Invoice
from .forms import LineItemFormset,InvoiceForm

import pdfkit

class InvoiceListView(View):
    def get(self,*args,**kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request,'invoice/invoice-list.html',context)

def createInvoice(request):
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset= LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address = form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data["due_date"], 
                    message=form.data["message"],
                    )
        # invoice.save()

        if formset.is_valid():
            total=0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount= float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                                service=service,
                                description=description,
                                quantity=quantity,
                                rate=rate,
                                amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request,id=invoice.id)
            except Exception as e:
                print(f"********{e}******")
            return redirect('/')
    
    context ={
        "title":"Invoice Generator",
        "formset": formset,
        "form": form
    }
    return render(request,'invoice/invoice-create.html',context)

def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice,id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company":{
            "name": "Virtual Company Ltd.",
            "address": "23th Street, Zbcxyz",
            "phone": "+91 XXXX-XX-XXXX",
            "email": "abc@xompany.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email":invoice.customer_email,
        "date": invoice.date,
        "due_date":invoice.due_date,
        "billing_address":invoice.billing_address,
        "message": invoice.billing_address,
        "lineitem":lineitem,
    }
    return render(request,'invoice/pdf_template.html',context)

def generate_PDF(request,id):
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail',args=[id])),False)
    response= HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="invoice.pdf"'

    return response


def view_404(request, *args, **kwags):
    return redirect('invoice:invoice-list')
