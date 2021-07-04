from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db import models
import docx2txt
import difflib
import nltk
import PyPDF2
import requests
from bs4 import BeautifulSoup
from django_xhtml2pdf.utils import generate_pdf
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.core.files.storage import FileSystemStorage
import os

# report here 

def report(text1,text2,text3,text4):
 from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
 from reportlab.lib.pagesizes import A4, landscape, portrait
 from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, Flowable, Spacer
 from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.lib.units import inch
 from reportlab.pdfgen import canvas
 
 doc1 =[]
 pdfmetrics.registerFont(TTFont('Timesbd', 'timesbd.ttf',))
 pdfmetrics.registerFont(TTFont('c','Georgia.ttf',))
 pdfmetrics.registerFont(TTFont('cb','Georgiab.ttf',))
 doc1.append(Spacer(1,-60))
#  doc1.append(Image('ayush.png'))
 doc1.append(Spacer(1,20))
 doc1.append(Paragraph('PLAGIARISM REPORT',ParagraphStyle(name='p',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=24,alignment=TA_CENTER)))
 doc1.append(Spacer(1,30))

 def addp(doc):
    doc1.append(Paragraph('PLAG SCORE:',ParagraphStyle(name='q',fontName='Timesbd',textColor='rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
    doc.append(Spacer(1,10))
    doc1.append(Paragraph(text1,ParagraphStyle(name='r',fontName='Timesbd',fontSize=16,textColor='rgb(204,0,0)',alignment=TA_CENTER)))

    doc.append(Spacer(1,30))
    doc1.append(Paragraph('INPUT 1',ParagraphStyle(name='s',fontName='Timesbd',fontSize=16,textColor= 'rgb(0,0,134)',alignment=TA_CENTER)))
    doc.append(Spacer(1,10))
    doc1.append(Paragraph(text2,ParagraphStyle(name='t',fontName='c',textColor='rgb(0,0,0)',fontSize=12,alignment=TA_CENTER)))

    doc.append(Spacer(1,25))
    doc1.append(Paragraph('INPUT 2',ParagraphStyle(name='u',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
    doc.append(Spacer(1,10))
    doc1.append(Paragraph(text3,ParagraphStyle(name='v',fontName='c',textColor= 'rgb(0,0,0)',fontSize=12,alignment=TA_CENTER)))

    doc.append(Spacer(1,25))
    doc1.append(Paragraph('MATCHED DATA',ParagraphStyle(name='w',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
    doc1.append(Spacer(1,10))
    doc1.append(Paragraph(text4,ParagraphStyle(name='x',fontName='cb',fontSize=12,textColor= 'rgb(180,0,0)',alignment=TA_CENTER)))
    return doc

 doc1=addp(doc1)

 SimpleDocTemplate('media\Plag_Report.pdf',title='Plag_Report',pagesize=A4).build(doc1)
 return doc1
# report ends 

def index2(request):
    fs=FileSystemStorage()
    filename="Plag_Report.pdf"
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition']='inline; filename="Plag_Report.pdf"'
            return response
    else:
        return HttpResponse("error hai")
def index3(request):
    fs=FileSystemStorage()
    filename="Plag_Report.pdf"
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition']='attachment; filename="Plag_Report.pdf"'
            return response
    else:
        return HttpResponse("error hai")

def login(request):
    return render(request, 'users/login.html')


def home(request):
    return render(request, 'dejavu/home.html')


def about(request):
    return render(request, 'dejavu/about.html')


def index(request):

    djtext1 = request.POST['t1']
    djtext2 = request.POST['t2']
    state1 = request.POST.get('x1', 'off')
    state2 = request.POST.get('x2', 'off')
    flag = 0
    m1 = len(djtext1)
    m2 = len(djtext2)
    if m1 == 18 and m2 == 18:
        flag = 1
    if state1 == "on" or state2 == "on":
        if state1 == "on":
            url1 = request.POST.get('u1')
            r1 = requests.get(url1)
            htmlcontent1 = r1.content
            soup1 = BeautifulSoup(htmlcontent1, 'html.parser')
            link = soup1.find('td').get_text()
            # link=link[:4000]

        if state2 == "on":
            url2 = request.POST.get('u2')
            r2 = requests.get(url2)
            htmlcontent2 = r2.content
            soup2 = BeautifulSoup(htmlcontent2, 'html.parser')
            link = soup2.find('article').get_text()
            # link=link[:4000]
        if m1 != 18:
            #common text list
            common=""
            matches = difflib.SequenceMatcher(
                  None, djtext1, link).get_matching_blocks()
            for match in matches:
                  #print (t1[match.a:match.a + match.size])
                  common+=djtext1[match.a:match.a + match.size]
            seq = difflib.SequenceMatcher(None, djtext1, common)
            d = seq.ratio()*100
            d = round(d, 2)
            x = ""
            x = str(d)
            
           
            # if common==djtext1 or common==link:
            #     x="100"
            report(x,djtext1,link,common)
            
            params = {'text1': djtext1, 'text2': link,
                      'res': flag, 'len1': m1, 'len2': m2, 'ans': x,'com':common}
            return render(request, 'result.html', params)
        elif request.method == 'POST':

            bfile1 = request.FILES['f1']
            ext1 = bfile1.name
            if ext1[-1] == 'x':
                z = docx2txt.process(bfile1)
            elif ext1[-1] == 'f':
                x1 = PyPDF2.PdfFileReader(bfile1)
                z = " "
                num = x1.getNumPages()
                for i in range(1, num):
                    z += x1.getPage(i).extractText()
            seq = difflib.SequenceMatcher(None, link, z)
            d = seq.ratio()*100
            d = round(d, 2)
            x = " "
            x = str(d)
            common=""
            matches = difflib.SequenceMatcher(
                     None, link, z).get_matching_blocks()
            for match in matches:
                 common+=link[match.a:match.a + match.size]
           
            report(x,link,z,common)
           
            params = {'text1': z, 'text2': link, 'res': flag,
                      'len1': m1, 'len2': m2, 'ans': x,'com':common}
            return render(request, 'result.html', params)

    elif request.method == 'POST' and flag == 1:

        bfile1 = request.FILES['f1']
        bfile2 = request.FILES['f2']

        ext1 = bfile1.name
        ext2 = bfile2.name

        if ext1[-1] == 'x':
            z = docx2txt.process(bfile1)
        elif ext1[-1] == 'f':
            x1 = PyPDF2.PdfFileReader(bfile1)
            z = " "
            num = x1.getNumPages()
            for i in range(1, num):
                z += x1.getPage(i).extractText()

        if ext2[-1] == 'x':
            y = docx2txt.process(bfile2)

        elif ext2[-1] == 'f':
            x2 = PyPDF2.PdfFileReader(bfile2)
            y = " "
            num = x2.getNumPages()
            for i in range(1, num):
                y += x2.getPage(i).extractText()
        seq = difflib.SequenceMatcher(None, y, z)
        d = seq.ratio()*100
        d = round(d, 2)
        x = " "
        x = str(d)
        common=""
        matches = difflib.SequenceMatcher(
                     None, y, z).get_matching_blocks()
        for match in matches:
                 common+=y[match.a:match.a + match.size]
        if common==y or common==z:
            x="100"
        report(x,y,z,common)
        params = {'text1': z, 'text2': y, 'res': flag,
                  'len1': m1, 'len2': m2, 'ans': x,'com':common}
        return render(request, 'result.html', params)
    else:
        common=""
        matches = difflib.SequenceMatcher(
                     None, djtext1, djtext2).get_matching_blocks()
        for match in matches:
                 common+=djtext1[match.a:match.a + match.size]
        seq = difflib.SequenceMatcher(None, djtext1, djtext2)
        d = seq.ratio()*100
        d = round(d, 2)
        x = ""
        x = str(d)
       
        # if common==djtext1 or common==djtext2:
        #     x="100"
               
        report(x,djtext1,djtext2,common)
        params = {'text1': djtext1, 'text2': djtext2,
                  'res': flag, 'len1': m1, 'len2': m2, 'ans': x,'com':common}
        return render(request, 'result.html', params)
