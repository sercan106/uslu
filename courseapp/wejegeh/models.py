from django.db import models
import datetime
from django.utils.text import slugify #slugify (java-kursu) import ettik

class Ödemedetay(models.Model):
    kategori = models.CharField(max_length=100)#zorunlu
    taksitsayısı = models.CharField(max_length=100,blank=True)
    tutar=models.CharField(max_length=100,blank=True)
    ödemeilk=models.DateField(verbose_name="Ödeme Tarihi",blank=True)
    ödemeson=models.DateField(verbose_name="Son Ödeme Tarihi",blank=True)
    ödendimi=models.BooleanField(blank=True)
    notekle = models.TextField(blank=True)
    def __str__(self):
      return f"{self.kategori} {self.taksitsayısı}. taksit" 



class DüzenliÖdeme(models.Model):
    kategori = models.CharField(max_length=100)#zorunlu
    toplamtaksit = models.CharField(max_length=100,blank=True)
    detay = models.ManyToManyField(Ödemedetay,blank=True)
    notekle = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.kategori
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.kategori)
        super().save(*args, **kwargs)



class Renk(models.Model):
    renkadı= models.CharField(max_length=100)#zorunlu
    renkcode= models.CharField(max_length=100)#zorunlu
    
    def __str__(self):
        return self.renkadı

class Notlar(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    detay = models.ForeignKey(Renk,on_delete=models.CASCADE)
    notekle = models.TextField(blank=True)
    yapıldımı=models.BooleanField(blank=True)
    
    def __str__(self):
        return self.başlık
    
class Günlük(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    detay = models.ForeignKey(Renk,on_delete=models.CASCADE)
    notekle = models.TextField(blank=True)
    yapıldımı=models.BooleanField(blank=True)
    
    def __str__(self):
        return self.başlık
class Haftalık(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    detay = models.ForeignKey(Renk,on_delete=models.CASCADE)
    notekle = models.TextField(blank=True)
    yapıldımı=models.BooleanField(blank=True)
    
    def __str__(self):
        return self.başlık
               
class Hedefler(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    detay = models.ForeignKey(Renk,on_delete=models.CASCADE)
    notekle = models.TextField(blank=True)
    yapıldımı=models.BooleanField(blank=True)
    
    def __str__(self):
        return self.başlık
       
       
           
class Harcayan(models.Model):
 başlık = models.CharField(max_length=100)#zorunlu
 def __str__(self):
     return self.başlık 

class Başlık(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.başlık

class Birim(models.Model):
    birim = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.birim

class Diğerbaşlık(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.başlık

class Faturabaşlık(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.başlık


class Kategorisi(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.başlık   
    
class Gıdakategorisi(models.Model):
    başlık = models.CharField(max_length=100)#zorunlu
    def __str__(self):
        return self.başlık   
         
class Diğer(models.Model):
    harcayan = models.ForeignKey(Harcayan,on_delete=models.CASCADE)
    kategorisi = models.ForeignKey(Kategorisi,on_delete=models.CASCADE)
    başlık = models.ForeignKey(Diğerbaşlık,on_delete=models.CASCADE)
    birim = models.ForeignKey(Birim,on_delete=models.CASCADE,blank=True, null=True)
    miktar = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    tarih=models.DateField(verbose_name="Tarih")
    def __str__(self):
        return self.başlık.başlık
    
class Fatura(models.Model):
    harcayan = models.ForeignKey(Harcayan,on_delete=models.CASCADE)
    kategorisi = models.ForeignKey(Faturabaşlık,on_delete=models.CASCADE)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    tarih=models.DateField(verbose_name="Tarih")
    def __str__(self):
        return self.kategorisi.başlık

class Gıda(models.Model):
    harcayan = models.ForeignKey(Harcayan,on_delete=models.CASCADE)
    kategorisi = models.ForeignKey(Gıdakategorisi,on_delete=models.CASCADE)
    başlık = models.ForeignKey(Başlık,on_delete=models.CASCADE)
    birim = models.ForeignKey(Birim,on_delete=models.CASCADE,blank=True, null=True)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    tarih=models.DateField(verbose_name="Tarih")
    def __str__(self):
        return self.başlık.başlık

#_______________________________SERCAN______________________

class Sahibi(models.Model):
 başlık = models.CharField(max_length=100)#zorunlu
 def __str__(self):
     return self.başlık 

class Düzensizkategori(models.Model):
    kategori = models.CharField(max_length=100)#zorunlu
    def __str__(self):
      return self.kategori

class Düzensiz(models.Model):
    sahibi = models.ForeignKey(Sahibi,on_delete=models.CASCADE)
    kategori = models.ForeignKey(Düzensizkategori,on_delete=models.CASCADE)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    ödemeson=models.DateField(verbose_name="Son Ödeme Tarihi",blank=True)
    ödendimi=models.BooleanField(blank=True)
    notekle = models.TextField(blank=True)
    
    def __str__(self):
        return self.kategori.kategori
  
#__________________________MEHMET__________________________________   
class Düzensizm(models.Model):
    sahibi = models.ForeignKey(Sahibi,on_delete=models.CASCADE)
    kategori = models.ForeignKey(Düzensizkategori,on_delete=models.CASCADE)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    ödemeson=models.DateField(verbose_name="Son Ödeme Tarihi",blank=True)
    ödendimi=models.BooleanField(blank=True)
    notekle = models.TextField(blank=True)
    
    def __str__(self):
        return self.kategori.kategori

#__________________________EREN__________________________________   
class Düzensize(models.Model):
    sahibi = models.ForeignKey(Sahibi,on_delete=models.CASCADE)
    kategori = models.ForeignKey(Düzensizkategori,on_delete=models.CASCADE)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    ödemeson=models.DateField(verbose_name="Son Ödeme Tarihi",blank=True)
    ödendimi=models.BooleanField(blank=True)
    notekle = models.TextField(blank=True)
    
    def __str__(self):
        return self.kategori.kategori        
        
        
        
        
        
        #________________________KARTLAR_________________________

#_________________________KARTLAR___________________________________                 
class Kartlar(models.Model):
    sahibi =models.CharField(max_length=10)
    kategori = models.ForeignKey(Düzensizkategori,on_delete=models.CASCADE)
    toplam_borç = models.DecimalField(max_digits=10, decimal_places=2)
    güncelleme_tarihi=models.DateField(verbose_name="Güncelleme Tarihi",blank=True)
    notekle = models.TextField(blank=True)
    
    def __str__(self):
        return self.kategori.kategori
        
#__________________________GELİR__________________________
class Gelir(models.Model):
    BIRIM_CHOICES = [
        ('TL', 'Türk Lirası'),
        ('RUB', 'Rus Rublesi'),
        ('ALTIN', 'Altın'),
        ('USD', 'Dolar'),
        ('EUR', 'Euro'),
        # Diğer birimler buraya eklenebilir
    ]

    kaynak = models.CharField(max_length=255)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    birim = models.CharField(max_length=50, choices=BIRIM_CHOICES)
    tarih = models.DateField(verbose_name="Tarih")

    def __str__(self):
        return f"{self.kaynak} - {self.miktar} {self.get_birim_display()}"        
        
        
        
        
        
        
        
        
        
# class Slide_index(models.Model):
#     tarih=models.DateField(verbose_name="Tarih",blank=True)
#     resim = models.ImageField(upload_to='index/slide')


# class Yıl(models.Model):
#     yıl = models.IntegerField()
#     def __str__(self):
#         return str(self.yıl)
  
# class Tür(models.Model):
#     tür_tr = models.CharField(max_length=50,blank=True)
#     tür_ku = models.CharField(max_length=50,blank=True)
#     tür_en = models.CharField(max_length=50,blank=True)
#     def __str__(self):
#         return self.tür_tr
# class Alan(models.Model):
#     alan_tr = models.CharField(max_length=50,blank=True)
#     alan_ku = models.CharField(max_length=50,blank=True)
#     alan_en = models.CharField(max_length=50,blank=True)
#     def __str__(self):
#         return self.alan_tr


# class Renk(models.Model):
#     renk_adi = models.TextField(blank=True)
#     renk_code=models.TextField(blank=True)
#     def __str__(self):
#         return self.renk_adi


# class Program_Anasayfa(models.Model):
#     renk = models.ForeignKey(Renk, on_delete=models.CASCADE)
#     baslik_tr = models.CharField(max_length=100,blank=True)
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     aciklama_tr = models.TextField(blank=True)
#     aciklama_ku = models.TextField(blank=True)
#     aciklama_en = models.TextField(blank=True)
#     foto_tr = models.ImageField(upload_to='program/fotoanasayfa',blank=True)
#     foto_ku = models.ImageField(upload_to='program/fotoanasayfa',blank=True)
#     foto_en = models.ImageField(upload_to='program/fotoanasayfa',blank=True)
#     slug_tr = models.SlugField(default="", null=False, blank=True)
#     slug_ku = models.SlugField(default="", null=False, blank=True)
#     slug_en = models.SlugField(default="", null=False, blank=True)
#     def __str__(self):
#         return self.baslik_tr
#     def save(self, *args, **kwargs):
#         if not self.slug_tr and self.baslik_tr:
#             self.slug_tr = slugify(self.baslik_tr)
#         if not self.slug_ku and self.baslik_ku:
#             self.slug_ku = slugify(self.baslik_ku)
#         if not self.slug_en and self.baslik_en:
#             self.slug_en = slugify(self.baslik_en)
#         super().save(*args, **kwargs)

# class Porogram_E_Foto(models.Model):
    
#     foto_name = models.CharField(max_length=100,blank=True)
#     foto = models.ImageField(upload_to='program_etkinlik')
#     redirect_url = models.URLField(blank=True)

#     def __str__(self):
#         return self.foto_name


# class Program_Etkinlik(models.Model):
#     tarih=models.DateField(verbose_name="Tarih",blank=True)
#     Ust_kategori = models.ForeignKey(Program_Anasayfa, on_delete=models.CASCADE)
#     Ustkategori_foto=models.ImageField(upload_to='program/fotoanasayfa')#zorunlu
#     etkinlik_fotoları = models.ManyToManyField(Porogram_E_Foto,blank=True)
#     baslik_tr = models.CharField(max_length=100)#zorunlu
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     yazar_tr = models.CharField(max_length=100,blank=True)
#     yazar_ku = models.CharField(max_length=100,blank=True)
#     yazar_en = models.CharField(max_length=100,blank=True)
#     metin_tr = models.TextField(blank=True)
#     metin_ku = models.TextField(blank=True)
#     metin_en = models.TextField(blank=True)
#     tür=models.ForeignKey(Tür,on_delete=models.CASCADE,blank=True, null=True)
#     alan=models.ForeignKey(Alan,on_delete=models.CASCADE,blank=True, null=True)
   
   
#     slug_tr = models.SlugField(default="", null=False, blank=True)
#     slug_ku = models.SlugField(default="", null=False, blank=True)
#     slug_en = models.SlugField(default="", null=False, blank=True)
#     genel_active=models.BooleanField(blank=True)
#     active_tr=models.BooleanField(blank=True)
#     active_ku=models.BooleanField(blank=True)
#     active_en=models.BooleanField(blank=True)
#     active_anasayfa=models.BooleanField(blank=True)
#     def __str__(self):
#         return self.baslik_tr
#     def save(self, *args, **kwargs):
#         if not self.slug_tr and self.baslik_tr:
#             self.slug_tr = slugify(self.baslik_tr)
#         if not self.slug_ku and self.baslik_ku:
#             self.slug_ku = slugify(self.baslik_ku)
#         if not self.slug_en and self.baslik_en:
#             self.slug_en = slugify(self.baslik_en)
#         super().save(*args, **kwargs)


# class Logos(models.Model):
#     logo_name = models.CharField(max_length=100,blank=True)
#     logo = models.ImageField(upload_to='logos/')
#     colored_image = models.ImageField(upload_to='colored_images/')
#     redirect_url = models.URLField()
#     def __str__(self):
#         return self.logo_name



# class Proje_anasayfa(models.Model):
#     baslik_tr = models.CharField(max_length=100,blank=True)
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)

#     aciklama_tr = models.TextField(blank=True)
#     aciklama_ku = models.TextField(blank=True)
#     aciklama_en = models.TextField(blank=True)

#     foto_tr = models.ImageField(upload_to='proje/fotoanasayfa',blank=True)
#     foto_ku = models.ImageField(upload_to='proje/fotoanasayfa',blank=True)
#     foto_en = models.ImageField(upload_to='proje/fotoanasayfa',blank=True)

#     slug_tr = models.SlugField(default="", null=False, blank=True)
#     slug_ku = models.SlugField(default="", null=False, blank=True)
#     slug_en = models.SlugField(default="", null=False, blank=True)

#     def __str__(self):
#         return self.baslik_tr

#     def save(self, *args, **kwargs):
#         if not self.slug_tr and self.baslik_tr:
#             self.slug_tr = slugify(self.baslik_tr)
#         if not self.slug_ku and self.baslik_ku:
#             self.slug_ku = slugify(self.baslik_ku)
#         if not self.slug_en and self.baslik_en:
#             self.slug_en = slugify(self.baslik_en)
#         super().save(*args, **kwargs)

# class Proje_icerik(models.Model):
#     paragraf_adi = models.CharField(max_length=100,blank=True)
#     metin_tr = models.TextField(blank=True)
#     metin_ku = models.TextField(blank=True)
#     metin_en = models.TextField(blank=True)
#     foto = models.ImageField(upload_to='proje/foto')
#     def __str__(self):
#         return self.paragraf_adi

# class Proje_slide(models.Model):
#     slide_name = models.CharField(max_length=100,blank=True)
#     foto=models.ImageField(upload_to='proje/slide')#zorunlu
#     def __str__(self):
#         return self.slide_name

# class Proje_Etkinlik(models.Model):
#     tarih=models.DateField(verbose_name="Tarih",blank=True)
#     Ust_kategori = models.ForeignKey(Proje_anasayfa, on_delete=models.CASCADE)
#     Ustkategori_foto=models.ImageField(upload_to='program/fotoanasayfa')#zorunlu
#     Ustkategori_renk=models.ForeignKey(Renk, on_delete=models.CASCADE)#zorunlu
#     foto=models.ImageField(upload_to='program/foto',blank=True)#zorunlu
#     baslik_tr = models.CharField(max_length=100)#zorunlu
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     proje_içerik = models.ManyToManyField(Proje_icerik,blank=True, null=True)
#     proje_slides = models.ManyToManyField(Proje_slide,blank=True, null=True)
 
#     tür=models.ForeignKey(Tür,on_delete=models.CASCADE,blank=True)
#     alan=models.ForeignKey(Alan,on_delete=models.CASCADE,blank=True)


#     slug_tr = models.SlugField(default="", null=False, blank=True)
#     slug_ku = models.SlugField(default="", null=False, blank=True)
#     slug_en = models.SlugField(default="", null=False, blank=True)

#     slide_active=models.BooleanField(blank=True)
#     genel_active=models.BooleanField(blank=True)
#     active_tr=models.BooleanField(blank=True)
#     active_ku=models.BooleanField(blank=True)
#     active_en=models.BooleanField(blank=True)
#     active_anasayfa=models.BooleanField(blank=True)
#     def __str__(self):
#         return self.baslik_tr
#     def save(self, *args, **kwargs):
#         if not self.slug_tr and self.baslik_tr:
#             self.slug_tr = slugify(self.baslik_tr)
#         if not self.slug_ku and self.baslik_ku:
#             self.slug_ku = slugify(self.baslik_ku)
#         if not self.slug_en and self.baslik_en:
#             self.slug_en = slugify(self.baslik_en)
#         super().save(*args, **kwargs)


# class Photo(models.Model):
#     url = models.ImageField(upload_to='photos/')  # Django'nun ImageField'ını kullanarak fotoğrafı yüklemek için
#     alt_text = models.CharField(max_length=255, help_text="Fotoğraf için alternatif metin")
#     caption = models.TextField(blank=True, help_text="Fotoğraf altındaki açıklama veya başlık")

#     def __str__(self):
#         return self.alt_text


# class Hakkimizda(models.Model):
#     foto=models.ImageField(upload_to='hakkımızda')#zorunlu
#     baslik_tr = models.CharField(max_length=100,blank=True)
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     metin_tr = models.TextField(blank=True)
#     metin_ku = models.TextField(blank=True)
#     metin_en = models.TextField(blank=True)
#     def __str__(self):
#         return self.baslik_tr

# class Ev_icerik(models.Model):
#     baslik_tr = models.CharField(max_length=100,blank=True)
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     metin_tr = models.TextField(blank=True)
#     metin_ku = models.TextField(blank=True)
#     metin_en = models.TextField(blank=True)
#     foto=models.ImageField(upload_to='ev/foto')#zorunlu
#     def __str__(self):
#         return self.baslik_tr

# class Ev_logo(models.Model):
#     logo_name = models.CharField(max_length=100,blank=True)
#     foto=models.ImageField(upload_to='ev/logo')#zorunlu
#     redirect_url = models.URLField(blank=True)
#     def __str__(self):
#         return self.logo_name

# class Ev(models.Model):
#     name = models.CharField(max_length=100,blank=True)
#     ev_icerik = models.ManyToManyField(Ev_icerik,blank=True)
#     ev_logoları = models.ManyToManyField(Ev_logo,blank=True)
#     def __str__(self):
#         return self.name

# class Yayıncılık_slide(models.Model):
#     slide_name = models.CharField(max_length=100,blank=True)
#     foto=models.ImageField(upload_to='yayıncılık/slide')#zorunlu
#     def __str__(self):
#         return self.slide_name

# class Yayıncılık_alt_icerik(models.Model):
#     baslik_tr = models.CharField(max_length=100,blank=True)
#     baslik_ku = models.CharField(max_length=100,blank=True)
#     baslik_en = models.CharField(max_length=100,blank=True)
#     metin_tr = models.TextField(blank=True)
#     metin_ku = models.TextField(blank=True)
#     metin_en = models.TextField(blank=True)
#     foto=models.ImageField(upload_to='yayıncılık/foto')#zorunlu
#     def __str__(self):
#         return self.baslik_tr

# class Yayıncılık(models.Model):
#     slide_ustubaslik_tr = models.CharField(max_length=100,blank=True)
#     slide_ustubaslik_ku = models.CharField(max_length=100,blank=True)
#     slide_ustubaslik_en = models.CharField(max_length=100,blank=True)
#     slide_ustmetin_tr = models.TextField(blank=True)
#     slide_ustmetin_ku = models.TextField(blank=True)
#     slide_ustmetin_en = models.TextField(blank=True)
#     slides = models.ManyToManyField(Yayıncılık_slide,blank=True)
#     yayıncılık_alt_icerik = models.ManyToManyField(Yayıncılık_alt_icerik,blank=True)
#     def __str__(self):
#         return self.slide_ustubaslik_tr



# class Yazi(models.Model):
#     name = models.CharField(max_length=100,blank=True)
#     def __str__(self):
#         return self.name
# class Settings(models.Model):
#     name = models.CharField(max_length=100,blank=True)
#     favicon=models.ImageField(upload_to='genel/favicon',blank=True)#zorunlu
#     logo=models.ImageField(upload_to='genel/logo',blank=True)#zorunlu
#     yazi_tipi =  models.ForeignKey(Yazi, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.name


# class Adres(models.Model):
#     name=models.CharField( max_length=50)
#     foto=models.ImageField(upload_to='adres/foto',blank=True)#zorunlu
#     adres_tr = models.TextField(blank=True)
#     adres_ku = models.TextField(blank=True)
#     adres_en = models.TextField(blank=True)
#     numara=models.CharField( max_length=50, blank=True)
#     e_mail=models.EmailField(blank=True)
#     def __str__(self):
#         return self.name


















