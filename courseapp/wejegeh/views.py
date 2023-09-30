import json
from django.db.models import Q
from itertools import chain
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse
# from wejegeh.forms import ErzakForm     #hesap klasörünün altındakı forms.py kategoriyi import ettik
from .models import DüzenliÖdeme,Ödemedetay,Notlar,Gıda,Diğer,Fatura
from .models import Düzensize,Düzensizm,Düzensiz,Kartlar,Gelir
from .models import Notlar,Günlük,Haftalık,Hedefler
import random #rastgele sayı üretmek için
from django.db.models.functions import TruncMonth
from django.db.models import F
import os
from django.contrib.auth.decorators import login_required , user_passes_test #loginmi kontrolleri için ilk parametre normal kullanıcılar ikincisi superuser kullanıcı için geçerli

from django.contrib import messages
from datetime import datetime





@login_required()#normal kullanıcı login mi?
def gelir(request):
    # Bu queryset, verileri aylara göre gruplayarak birimlere göre toplamları hesaplar.
    gelirler_aylik = Gelir.objects.annotate(ay=TruncMonth('tarih')).values('ay', 'birim').annotate(toplam=Sum(F('miktar'))).order_by('ay', 'birim').order_by('-id')

    # Sonuçları bir sözlük içinde düzenleyin, her ayın birim toplamları bu sözlüğün içinde olacak.
    gelirler_sozluk = {}
    for gelir in gelirler_aylik:
        ay = gelir['ay'].strftime('%Y-%m')  # Ayı Yıl-Ay formatında alın
        birim = gelir['birim']
        toplam = gelir['toplam']

        if ay not in gelirler_sozluk:
            gelirler_sozluk[ay] = {}

        gelirler_sozluk[ay][birim] = toplam

    # Şimdi gelirler_sozluk adlı sözlüğü şablona iletebilirsiniz.
    veri = Gelir.objects.all().order_by('-id')
    
    # Şablon ile verileri bir araya getirip HTTP yanıtını oluşturun
    return render(request, 'wejegeh/gelir.html', {'veri': veri, 'gelirler_sozluk': gelirler_sozluk})
  
  




@login_required()#normal kullanıcı login mi?
def ev(request):
    # Tüm verileri tarih sırasına göre birleştirin ve ters sıralayın
    tarihsel_veriler = sorted(
        list(Diğer.objects.all()) + list(Fatura.objects.all()) + list(Gıda.objects.all()),
        key=lambda x: x.tarih,
        reverse=True  # Ters sıralama
    )
    
    # Şu anki tarihi alın
    su_an = datetime.now()
    
    # Market, Fatura ve Diğer modellerindeki tutarları bulunduğunuz ay için toplamak için aggregate kullanın
    gıda_toplam = Gıda.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00
    fatura_toplam = Fatura.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00
    diger_toplam = Diğer.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00

    # Toplam tutarı hesaplayın
    toplam = int(gıda_toplam) + int(fatura_toplam) + int(diger_toplam)

    
    return render(request, 'wejegeh/ev.html', {'tarihsel_veriler': tarihsel_veriler,
                                               'gıda_toplam': gıda_toplam,
                                               'fatura_toplam': fatura_toplam,
                                               'diger_toplam': diger_toplam,
                                               'toplam':toplam})

  
@login_required()#normal kullanıcı login mi?
def harcama(request,kategori):
    print(kategori)
    print(type(kategori))
    
    # Tüm verileri tarih sırasına göre birleştirin ve ters sıralayın
    tarihsel_veriler = sorted(
        list(Diğer.objects.filter(harcayan__başlık=kategori).all()) + list(Fatura.objects.filter(harcayan__başlık=kategori).all()) + list(Gıda.objects.filter(harcayan__başlık=kategori).all()),
        key=lambda x: x.tarih,
        reverse=True  # Ters sıralama
    )
    
    # Şu anki tarihi alın
    su_an = datetime.now()
    
    # Market, Fatura ve Diğer modellerindeki tutarları bulunduğunuz ay için toplamak için aggregate kullanın
    gıda_toplam = Gıda.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year, harcayan__başlık=kategori).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00
    fatura_toplam = Fatura.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year, harcayan__başlık=kategori).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00
    diger_toplam = Diğer.objects.filter(tarih__month=su_an.month, tarih__year=su_an.year, harcayan__başlık=kategori).aggregate(toplam=Sum('tutar'))['toplam'] or 0.00
    # Toplam tutarı hesaplayın
    toplam = int(gıda_toplam) + int(fatura_toplam) + int(diger_toplam)
    
    return render(request, 'wejegeh/harcama_detay.html', {'tarihsel_veriler': tarihsel_veriler,
                                            'gıda_toplam': gıda_toplam,
                                            'fatura_toplam': fatura_toplam,
                                            'diger_toplam': diger_toplam,
                                            'toplam':toplam})

@login_required()#normal kullanıcı login mi?
def düzenli(request):
   if request.method=='POST':
      selected_ids = request.POST.getlist("selected_action")
      # Veritabanındaki Ödemedetay nesnelerini alıp ödendimi'yi True olarak işaretle
      Ödemedetay.objects.filter(id__in=selected_ids).update(ödendimi=True)
    
      print(selected_ids)
     
   
   şu_an = datetime.now().date()
   düzenliödeme=DüzenliÖdeme.objects.all()
   düzenliödeme_listesi=[]
   for i in düzenliödeme:
      for detay in i.detay.all():
         if detay.ödendimi==False:
  
            kalan_gün = (detay.ödemeson - şu_an).days
            # print(kalan_gün)
            if kalan_gün<=0:
               renk="D50000"
               # print("ödeme tarihi geçmiş")
            elif 0 <= kalan_gün <= 10:
               renk="F44336"
               # print("Sayı 0 ile 10 arasındadır.")   
            else:
               renk="AEEA00"
               
 
            düzenliödeme_listesi.append({'kategori': i.kategori, 
                                         'toplamtaksit': i.toplamtaksit,
                                         'notekle': i.notekle, 
                                         'taksitsayısı': detay.taksitsayısı, 
                                         'tutar': detay.tutar, 
                                         'ödemeilk': detay.ödemeilk, 
                                         'ödemeson': detay.ödemeson, 
                                         'ödendimi': detay.ödendimi, 
                                         'detaynotekle': detay.notekle,
                                          'id': detay.id,
                                         'kalangün': kalan_gün,
                                         'renk': renk,
                                       })
            düzenliödeme_listesi = sorted(düzenliödeme_listesi, key=lambda x: x['kalangün'])
            
            break
         else:
            pass 

   return render(request, 'wejegeh/düzenli.html',{
      'düzenliödeme':düzenliödeme_listesi,
   })




def isAdmin(user):#superuser kullanıcı login mi?
    return user.is_superuser
@user_passes_test(isAdmin)#normal kullanıcı login mi?
def notlar(request):
    if request.method == 'POST':
        gelen_veri = request.POST.get("id")
        not_obj = get_object_or_404(Notlar, id=gelen_veri)
        not_obj.yapıldımı = True
        not_obj.save()
        return redirect('notlar')#urls deseninde namesi notlar olan desene yönlenir
    else:
        aktif_notlar = Notlar.objects.filter(yapıldımı=False)
        return render(request, 'wejegeh/notlar.html', {'notlar': aktif_notlar})
    
 
 
def isAdmin(user):#superuser kullanıcı login mi?
    return user.is_superuser
@user_passes_test(isAdmin)#normal kullanıcı login mi?
def günlük(request):
    if request.method == 'POST':
        gelen_veri = request.POST.get("id")
        not_obj = get_object_or_404(Günlük, id=gelen_veri)
        not_obj.yapıldımı = True
        not_obj.save()
        return redirect('günlük')#urls deseninde namesi notlar olan desene yönlenir
    else:
        aktif_notlar = Günlük.objects.filter(yapıldımı=False)
        return render(request, 'wejegeh/günlük.html', {'notlar': aktif_notlar})   
           
    
    
def isAdmin(user):#superuser kullanıcı login mi?
    return user.is_superuser
@user_passes_test(isAdmin)#normal kullanıcı login mi?
def haftalık(request):
    if request.method == 'POST':
        gelen_veri = request.POST.get("id")
        not_obj = get_object_or_404(Haftalık, id=gelen_veri)
        not_obj.yapıldımı = True
        not_obj.save()
        return redirect('haftalık')#urls deseninde namesi notlar olan desene yönlenir
    else:
        aktif_notlar = Haftalık.objects.filter(yapıldımı=False)
        return render(request, 'wejegeh/haftalık.html', {'notlar': aktif_notlar})   
    
    

    
    
def isAdmin(user):#superuser kullanıcı login mi?
    return user.is_superuser
@user_passes_test(isAdmin)#normal kullanıcı login mi?
def hedefler(request):
    if request.method == 'POST':
        gelen_veri = request.POST.get("id")
        not_obj = get_object_or_404(Hedefler, id=gelen_veri)
        not_obj.yapıldımı = True
        not_obj.save()
        return redirect('hedefler')#urls deseninde namesi notlar olan desene yönlenir
    else:
        aktif_notlar = Hedefler.objects.filter(yapıldımı=False)
        return render(request, 'wejegeh/hedefler.html', {'notlar': aktif_notlar})   
        
    
    
    
    
    
    
    
    
    
    
    
    
    

@login_required()#normal kullanıcı login mi?
def yapildi(request,id):
    

    Notlar.objects.filter(id=id).update(yapıldımı=True) 

    return render(request, 'wejegeh/notlar.html')

@login_required()#normal kullanıcı login mi?
def genel(request):
    şu_an = datetime.now().date()
    toplam_m_dict = Düzensizm.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))
    toplam_e_dict = Düzensize.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))
    toplam_s_dict = Düzensiz.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))

    toplam_m = toplam_m_dict['toplam_tutar'] if toplam_m_dict['toplam_tutar'] is not None else 0
    toplam_e = toplam_e_dict['toplam_tutar'] if toplam_e_dict['toplam_tutar'] is not None else 0
    toplam_s = toplam_s_dict['toplam_tutar'] if toplam_s_dict['toplam_tutar'] is not None else 0

    genel = toplam_s + toplam_m + toplam_e

    ödendimi_false_öğeler_düzensizm = Düzensizm.objects.filter(ödendimi=False)
    ödendimi_false_öğeler_düzensiz = Düzensiz.objects.filter(ödendimi=False)
    ödendimi_false_öğeler_düzensize = Düzensize.objects.filter(ödendimi=False)
    
    # Sorgu sonuçlarını birleştirme
    ödendimi_false_öğeler = list(chain(ödendimi_false_öğeler_düzensizm,
                                  ödendimi_false_öğeler_düzensiz,
                                  ödendimi_false_öğeler_düzensize))
   
    # Geri kalan kodlar aynı kalabilir.
    
    düzensiz_listesi = []
    
    for detay in ödendimi_false_öğeler:
        kalan_gün = (detay.ödemeson - şu_an).days
        if kalan_gün <= 0:
            renk = "D50000"
        elif 0 <= kalan_gün <= 10:
            renk = "F44336"
        else:
            renk = "AEEA00"

        düzensiz_listesi.append({
            'kategori': detay.kategori,
            'notekle': detay.notekle,
            'tutar': detay.tutar,
            'ödemeson': detay.ödemeson,
            'ödendimi': detay.ödendimi,
            'id': detay.id,
            'kalangün': kalan_gün,
            'renk': renk,
        })

    düzensiz_listesi = sorted(düzensiz_listesi, key=lambda x: x['kalangün'])
    print(düzensiz_listesi)
    return render(request, 'wejegeh/genel.html', {
        'düzensizödeme': düzensiz_listesi,
        'genel': genel,
        'sercan': toplam_s,
        'mehmet': toplam_m,
        'eren': toplam_e,
        
    })




@login_required()#normal kullanıcı login mi?
def düzensiz(request):

    toplam_s_dict = Düzensiz.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))
    toplam_s = toplam_s_dict['toplam_tutar'] if toplam_s_dict['toplam_tutar'] is not None else 0
    if request.method == 'POST':
        selected_ids = request.POST.getlist("selected_action")
        # Veritabanındaki Ödemedetay nesnelerini alıp ödendimi'yi True olarak işaretle
        Düzensiz.objects.filter(id__in=selected_ids).update(ödendimi=True)

    şu_an = datetime.now().date()
    düzensiz = Düzensiz.objects.all()
    düzensiz_listesi = []

    for detay in düzensiz:
        if detay.ödendimi == False:

            kalan_gün = (detay.ödemeson - şu_an).days
            if kalan_gün <= 0:
                renk = "D50000"
            elif 0 <= kalan_gün <= 10:
                renk = "F44336"
            else:
                renk = "AEEA00"

            düzensiz_listesi.append({
                'kategori': detay.kategori,
                'notekle': detay.notekle,
                'tutar': detay.tutar,
                'ödemeson': detay.ödemeson,
                'ödendimi': detay.ödendimi,
                'id': detay.id,
                'kalangün': kalan_gün,
                'renk': renk,
            })

    düzensiz_listesi = sorted(düzensiz_listesi, key=lambda x: x['kalangün'])
    print(düzensiz_listesi)
    return render(request, 'wejegeh/düzensiz.html', {
        'düzensizödeme': düzensiz_listesi,
        'sercan': toplam_s,

    })



#______________________________MEHMET______________________________________________
@login_required()#normal kullanıcı login mi?
def düzensizm(request):
    toplam_m_dict = Düzensizm.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))
    toplam_m = toplam_m_dict['toplam_tutar'] if toplam_m_dict['toplam_tutar'] is not None else 0

    
    if request.method == 'POST':
        selected_ids = request.POST.getlist("selected_action")
        # Veritabanındaki Ödemedetay nesnelerini alıp ödendimi'yi True olarak işaretle
        Düzensizm.objects.filter(id__in=selected_ids).update(ödendimi=True)

    şu_an = datetime.now().date()
    düzensiz = Düzensizm.objects.all()
    düzensiz_listesi = []

    for detay in düzensiz:
        if detay.ödendimi == False:

            kalan_gün = (detay.ödemeson - şu_an).days
            if kalan_gün <= 0:
                renk = "D50000"
            elif 0 <= kalan_gün <= 10:
                renk = "F44336"
            else:
                renk = "AEEA00"

            düzensiz_listesi.append({
                'kategori': detay.kategori,
                'notekle': detay.notekle,
                'tutar': detay.tutar,
                'ödemeson': detay.ödemeson,
                'ödendimi': detay.ödendimi,
                'id': detay.id,
                'kalangün': kalan_gün,
                'renk': renk,
            })

    düzensiz_listesi = sorted(düzensiz_listesi, key=lambda x: x['kalangün'])

    return render(request, 'wejegeh/düzensizm.html', {
        'düzensizödeme': düzensiz_listesi,
        'mehmet': toplam_m,
       
    })
#________________________________EREN________________________________________    

@login_required()#normal kullanıcı login mi?
def düzensize(request):

    toplam_e_dict = Düzensize.objects.filter(ödendimi=False).aggregate(toplam_tutar=Sum('tutar'))
    toplam_e = toplam_e_dict['toplam_tutar'] if toplam_e_dict['toplam_tutar'] is not None else 0

    if request.method == 'POST':
        selected_ids = request.POST.getlist("selected_action")
        # Veritabanındaki Ödemedetay nesnelerini alıp ödendimi'yi True olarak işaretle
        Düzensize.objects.filter(id__in=selected_ids).update(ödendimi=True)

    şu_an = datetime.now().date()
    düzensiz = Düzensize.objects.all()
    düzensiz_listesi = []

    for detay in düzensiz:
        if detay.ödendimi == False:

            kalan_gün = (detay.ödemeson - şu_an).days
            if kalan_gün <= 0:
                renk = "D50000"
            elif 0 <= kalan_gün <= 10:
                renk = "F44336"
            else:
                renk = "AEEA00"

            düzensiz_listesi.append({
                'kategori': detay.kategori,
                'notekle': detay.notekle,
                'tutar': detay.tutar,
                'ödemeson': detay.ödemeson,
                'ödendimi': detay.ödendimi,
                'id': detay.id,
                'kalangün': kalan_gün,
                'renk': renk,
            })

    düzensiz_listesi = sorted(düzensiz_listesi, key=lambda x: x['kalangün'])
    print(düzensiz_listesi)
    
    return render(request, 'wejegeh/düzensize.html', {
        'düzensizödeme': düzensiz_listesi,
        'eren': toplam_e,
    })



@login_required()#normal kullanıcı login mi?
def düzensizsdetay(request, id):
    duzensiz_veri = Düzensiz.objects.get(id=id)
    kategori = duzensiz_veri.kategori.kategori
    print("Kategori:", kategori)

    veri = Düzensiz.objects.filter(kategori__kategori=kategori).order_by('-id').all()
    
    return render(request, 'wejegeh/düzensiz_detays.html', {'veri': veri})

@login_required()#normal kullanıcı login mi?
def düzensizmdetay(request, id):
    duzensiz_veri = Düzensizm.objects.get(id=id)
    kategori = duzensiz_veri.kategori.kategori
    print("Kategori:", kategori)

    veri = Düzensizm.objects.filter(kategori__kategori=kategori).order_by('-id').all()
    
    return render(request, 'wejegeh/düzensiz_detaym.html', {'veri': veri})



@login_required()#normal kullanıcı login mi?
def düzensizedetay(request, id):
    duzensiz_veri = Düzensize.objects.get(id=id)
    kategori = duzensiz_veri.kategori.kategori
    print("Kategori:", kategori)

    veri = Düzensize.objects.filter(kategori__kategori=kategori).order_by('-id').all()
    
    return render(request, 'wejegeh/düzensiz_detaye.html', {'veri': veri})


#___________________________KARTLAR________________________

@login_required()#normal kullanıcı login mi?
def kartlar(request):
    kartlar=Kartlar.objects.all()
    return render(request, 'wejegeh/kartlar.html',{'kartlar': kartlar})


@login_required()#normal kullanıcı login mi?
def kart_detay(request, sahibi, kategori):
    veri = None
    print(sahibi)

        
    if sahibi == "Sercan":
        print(veri)
        veri = Düzensiz.objects.filter(kategori__kategori=kategori).all()
        
    elif sahibi == "Eren":
        print(veri)
        veri = Düzensize.objects.filter(kategori__kategori=kategori).all()
        print(veri)       
    elif sahibi == "Mehmet":
        print(veri)
        veri = Düzensizm.objects.filter(kategori__kategori=kategori).all()

    return render(request, 'wejegeh/kart_detay.html', {'veri': veri})






# def program_etkinlik(request,kategori,slug):
#     program = get_object_or_404(Program_Etkinlik, slug_tr=slug)  # burada slug_tr'yi kullandım, slug_ku veya slug_en'yi de kullanabilirsiniz.
#     return render(request, 'wejegeh/program_etkinlik.html', {'program': program})










# # def contact(request):
# #     return render(request, 'bal/contact.html')

# # def hakkında(request):
# #     return render(request, 'bal/hakkında.html')

# # def shop(request):
# #     entries = Urun.objects.all()
# #     return render(request, 'bal/shop.html',{'entries': entries})



# # def urun_ekle(request):
# #     if request.method == 'POST':
# #         form = UrunForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('urun_ekle')  # Yeniden formu temiz bir şekilde göstermek için aynı sayfaya yönlendiriyoruz
# #     else:
# #         form = UrunForm()
# #     return render(request, 'bal/urun_ekle.html', {'form': form})


# # def urun_detay(request, id, slug): 
# #     form = get_object_or_404(Urun, id=id)#id bilgisini dışardan gelen
# #      #idurlsye eşitledik
# #     return render(request, 'bal/urun_detay.html', {'form': form})


# #_______________________________________________________________________________________________
# # def home(request):
# #     toplam_borc = Ödeme.objects.aggregate(toplam_borc=Sum('miktar'))
# #     entries = Ödeme.objects.all()



# #     return render(request, 'hesap/hesap.html',{'entries': entries,
# #                                                'toplam_borc': toplam_borc, })

# # def kartlar(request):
# #     entries = Kartlar.objects.all()
# #     return render(request, 'hesap/kartlar.html',{'entries': entries})

# # def borc(request):
# #     toplam_borc = Ödeme.objects.aggregate(toplam_borc=Sum('miktar'))
# #     entries = Ödeme.objects.all()


# #     return render(request, 'hesap/borc.html',{'entries': entries,
# #                                                'toplam_borc': toplam_borc})

# # def sonuc(request, id): 
# #     data=Kartlar.objects.get(pk=id) #id nosuna göre sorgulama yapar.
# #     print(data.isim)
# #     if data.isim=="Ziraat":
# #         print("gerekli işlemler için seleniuma yönlendirliyorsunuz")
# #         ziraat_giris()
# #     if data.isim=="Akbank":
# #         print("gerekli işlemler için seleniuma yönlendirliyorsunuz")
# #         akbank_giris()    
# #     if data.isim=="Halkbank":
# #         print("gerekli işlemler için seleniuma yönlendirliyorsunuz")
# #         halkbank_giris()
# #     if data.isim=="Enpara":
# #         print("gerekli işlemler için seleniuma yönlendirliyorsunuz")
# #         enpara_giris()          

# #     return render(request, 'hesap/sonuc.html')

# # def gıda(request):
# #     harcamalar = gıda.objects.all()
# #     return render(request, 'hesap/gıda.html', {'harcamalar': harcamalar})

# # def aileharcama(request):
# #     toplam_gida_harcamasi = GidaHarcamasi.objects.aggregate(toplam_gida_harcamasi=Sum('tutar'))
# #     entries = GidaHarcamasi.objects.all()
# #     return render(request, 'hesap/aileharcama.html',{'entries': entries,
# #                                                'toplam_gida_harcamasi': toplam_gida_harcamasi,
# #                                                })

# # def analiz(request):#burada toplam tutarların analizi var

# #     entries = Gıdaisimleri.objects.all()

# #     if request.method=='POST':
# #         ayy=request.POST['ay']
# #         yıll=request.POST['yıl']
# #         isim=request.POST['gıdaismi']
# #         print(f"{ayy}------> {yıll}------->{isim}")
# #         toplam = GidaHarcamasi.objects.filter(gida_adi=isim, kayit_tarihi__year=yıll, kayit_tarihi__month=ayy).aggregate(toplam_tutar=Sum('tutar'))
# #         print(toplam)
# #         return render(request, 'hesap/analiz.html', {'toplam': toplam})#post requesti gelince yönlendirme(anasayfaya yönlendirdi)
# #     return render(request, 'hesap/analiz.html',{'entries': entries})







# #  #__________________EKLE________________________



# # def ekle(request):
# #      if request.method == 'POST':
# #          form = KategoriForm(request.POST)
# #          if form.is_valid():
# #              # Form doğrulandı, verileri işle
# #              form.save()
# #              # Başka bir yere yönlendir
# #              return redirect('/')#post requesti gelince yönlendirme(anasayfaya yönlendirdi)
         
# #          print(form)
# #      else:
# #          form = KategoriForm()
# #      return render(request, 'hesap/ekle.html', {'form': form})

# # def kart_ekle(request):
# #      if request.method == 'POST':
# #          form = KartForm(request.POST)
# #          if form.is_valid():
# #              # Form doğrulandı, verileri işle
# #              form.save()
# #              # Başka bir yere yönlendir
# #              return redirect('/kartlar')#post requesti gelince yönlendirme(anasayfaya yönlendirdi)
         
# #          print(form)
# #      else:
# #          form = KartForm()
# #      return render(request, 'hesap/kart_ekle.html', {'form': form})

# # def eklegıda(request):
# #      entries = Gıdaisimleri.objects.all()  
# #      if request.method == 'POST':
# #          form = GidaHarcamasiForm(request.POST)
# #          if form.is_valid():
# #              # Form doğrulandı, verileri işle
# #              form.save()
# #              # Başka bir yere yönlendir
# #              return redirect('/aileharcama')#post requesti gelince yönlendirme(anasayfaya yönlendirdi)
         
# #          print(form)
# #      else:
# #          form = GidaHarcamasiForm()
# #      return render(request, 'hesap/eklegıda.html', {'form': form,
# #                                                     'entries': entries})

# # def gıdaisimekle(request):
# #     entries = Gıdaisimleri.objects.all()
    
# #     if request.method == 'POST':
# #         gida_adi = request.POST['gıdaname']
        
# #         if Gıdaisimleri.objects.filter(gida_adi=gida_adi).exists():
# #             messages.warning(request, 'Bu gıda ismi zaten mevcut.')
# #         else:
# #             kurslar = Gıdaisimleri(gida_adi=gida_adi)
# #             kurslar.save()
# #             return redirect('/gıdaisimekle')
    
# #     return render(request, 'hesap/gıdaisimekle.html', {'entries': entries})
# #     #get requesti gelince yönlendirme





# # #__________________SİL________________________
# # def kart_sil(request, id): 
# #      ödeme = get_object_or_404(Kartlar, id=id)#id bilgisini dışardan gelen
# #      #idurlsye eşitledik
# #      if request.method == 'POST':
# #              ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #              return redirect("/kartlar") #anasayfaya yönlendirdi       
            
# #      else:
# #          form = ödeme
# #      return render(request, 'hesap/kart_sil.html', {'form': form})


# # def sil(request, id): 
# #      ödeme = get_object_or_404(Ödeme, id=id)#id bilgisini dışardan gelen
# #      #idurlsye eşitledik
# #      if request.method == 'POST':
# #              ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #              return redirect("/") #anasayfaya yönlendirdi       
            
# #      else:
# #          form = ödeme
# #      return render(request, 'hesap/sil.html', {'form': form})

# # def gıda_sil(request, id): 
# #      gıdaisim = get_object_or_404(Gıdaisimleri, id=id)#id bilgisini dışardan gelen
# #      #idurlsye eşitledik
# #      if request.method == 'POST':
# #              gıdaisim.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #              return redirect("/gıdaisimekle") #anasayfaya yönlendirdi       
            
# #      else:
# #          form = gıdaisim
# #      return render(request, 'hesap/gıda_sil.html', {'form': form})

# # def silgıdaharcama(request):
# #    if request.method=='POST':
# #         id_no=request.POST['id_no']
# #         ödeme = get_object_or_404(GidaHarcamasi, id=id_no)
# #         ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #         return redirect("/silgıdaharcama") #anasayfaya yönlendirdi  

# #    else:
# #         entries = GidaHarcamasi.objects.all()
# #         return render(request, 'hesap/silgıdaharcama.html',{'entries': entries})

# # def silsercanharcama(request):
# #    if request.method=='POST':
# #         id_no=request.POST['id_no']
# #         ödeme = get_object_or_404(Sercanharcama, id=id_no)
# #         ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #         return redirect("/silsercanharcama") #anasayfaya yönlendirdi  

# #    else:
# #         entries = Sercanharcama.objects.all()
# #         return render(request, 'hesap/silsercanharcama.html',{'entries': entries})

# # def silmehmetharcama(request):
# #    if request.method=='POST':
# #         id_no=request.POST['id_no']
# #         ödeme = get_object_or_404(Mehmetharcama, id=id_no)
# #         ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #         return redirect("/silmehmetharcama") #anasayfaya yönlendirdi  

# #    else:
# #         entries = Mehmetharcama.objects.all()
# #         return render(request, 'hesap/silmehmetharcama.html',{'entries': entries})

# # def silerenharcama(request):
# #    if request.method=='POST':
# #         id_no=request.POST['id_no']
# #         ödeme = get_object_or_404(Erenharcama, id=id_no)
# #         ödeme.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #         return redirect("/silerenharcama") #anasayfaya yönlendirdi  

# #    else:
# #         entries = Erenharcama.objects.all()
# #         return render(request, 'hesap/silerenharcama.html',{'entries': entries})






































# # def veritabanı(request):

# #     kurslar=Book.objects.all()
# #     return render(request,'pages/veritabanı.html',{"kurs":kurslar})

# # def index(request):
# #     entries = Kategori.objects.all()
# #     context = {'entries': entries}

# #     return render(request, 'pages/index.html', context)

# # def search(request):
# #     #burada get sorgusu yaptık.search ile gelen urlde dışarıya results değerini çıkardık
# #     query = request.GET.get('q')#get sorgusundan gelen değeri aldık
# #     results = Kategori.objects.filter(başlık__contains=query)
# #     return render(request, 'pages/search.html', {'results': results})

# # def post(request):#EĞER POSTA GİRİLEN DEĞERLERE ŞARTLAR YÜKLEMEK İSTİYORSAK 7.7 DERSİNE BAKILABİLİR
# #     if request.method=='POST':
# #         imgurl=request.POST['imgurl']
# #         başlık=request.POST['başlık']
# #         içerik=request.POST['içerik']
# #         isActive=request.POST.get("isActive",False)#burada işaretlenmediği zaman hata vermemesinin önüne geçtik
# #         if isActive=="on":
# #             isActive=True
# #         kurslar=Kategori(başlık=başlık,imgurl=imgurl,içerik=içerik,isActive=isActive)    
# #         kurslar.save() 
# #         return redirect('/pages/index')#post requesti gelince yönlendirme
# #     return render(request, 'pages/post.html')#get requesti gelince yönlendirme


# # def post2(request):
# #     if request.method == 'POST':
# #         form = KategoriForm(request.POST)
# #         if form.is_valid():
# #             # Form doğrulandı, verileri işle
# #             form.save()
# #             # Başka bir yere yönlendir
# #             return redirect("/pages/index")#post requesti gelince yönlendirme
# #     else:
# #         form = KategoriForm()
# #     return render(request, 'pages/post2.html', {'form': form})


# # def ürün_detay(request): #güncellemek için
# #     entries = Kategori.objects.all()
    
# #     return render(request, 'pages/ürün_detay.html',{'entries': entries})




# # @login_required(login_url="/account/login") #Login değilse izin verilmez Burada içindeki linke yönlendirdi
# # def güncelle(request, idurls):
# #     kategori = get_object_or_404(Kategori, id=idurls)#idurls bilgisini dışardan gelen(urls.py.py dosyasından)
# #     #idurlsye eşitledik
# #     if request.method == 'POST':
# #         form = KategoriForm(request.POST, instance=kategori)
# #         if form.is_valid(): 
# #             form.save()# Başarılı bir şekilde güncellendiğinde yapılacak işlemler
# #             return redirect("/pages/ürün_detay")
# #     else:
# #         form = KategoriForm(instance=kategori)
# #     return render(request, 'pages/güncelle.html', {'form': form})



# # @login_required(login_url="/account/login") #Login değilse izin verilmez Burada içindeki linke yönlendirdi
# # def sil(request, idurls): #burdan devam edilecek
# #     kategori = get_object_or_404(Kategori, id=idurls)#id bilgisini dışardan gelen
# #     #idurlsye eşitledik
# #     if request.method == 'POST':
# #             kategori.delete()# Başarılı bir şekilde silme formu yapıldığında yapılacak işlemler
# #             return redirect("/pages/ürün_detay")        
            
# #     else:
# #         form = kategori
# #     return render(request, 'pages/sil.html', {'form': form})

# # def yükle(request):
# #     if request.method == 'POST':
# #         imgurl=request.FILES.getlist("dosya")
# #         for file in imgurl:
# #             dosya_yükleme(file) #dosya yükleme ffonksiyonu ile fotoğraf belirlenen klasöre yüklenir
# #         # print(imgurl)#çekilen verinin ismini verir
# #         # print(imgurl.name)#çekilen verinin ismini verir
# #         # print(imgurl.size)#çekilen boyutunu verir
# #         # print(imgurl.content_type)#çekilen verinin türünü verir
        


# #         return redirect("/pages/yükle")        
# #     return render(request, 'pages/yükle.html')


# # def dosya_yükleme(file):
# #     number=random.randint(1,99999)#rastgele sayı ürettik
# #     filename,file_extention=os.path.splitext(file.name)#file.name verisini uzantı adı ve dosya adına parçaladık
# #     name=filename+ "_"+str(number) + file_extention#bunu yeni değişkene atadık
# #     with open("temp/"+name,"wb+") as destination: #kızrmızı ile işaretlenen yerler gelen dosyayı belirlenen adrese yazmak için 
# #         for chunk in file.chunks():
# #             destination.write(chunk)


# # def kategori(request):
# #     return render(request,'pages/kategori.html')


# # def kurslar(request):
# #     return HttpResponse("selam pages")


# # def anasayfa(request):
# #     return HttpResponse("Buda pages anasayfadır")

# # def dinamik(request, kategori):
# #     return HttpResponse(f"'{kategori}' adlı değişken(int türünde) ile dinamik linke ulaştınız")

# # def dinamikstr(request, kategori):
# #     return HttpResponse(f"'{kategori}' adlı değişken(str türünde) ile dinamik linke ulaştınız")




# # def ziraatt():
# #     print("fonksiyon çalıştı")
# #     ziraat()#modülü çağırdık













