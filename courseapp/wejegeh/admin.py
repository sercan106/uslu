from django.contrib import admin
from .models import DüzenliÖdeme,Ödemedetay,Notlar,Renk,Birim,Gıda,Başlık,Diğer,Fatura,Diğerbaşlık,Faturabaşlık
from .models import Düzensiz,Düzensizm,Düzensize,Düzensizkategori, Harcayan
from .models import Kategorisi,Gıdakategorisi,Sahibi,Kartlar,Gelir,Günlük,Haftalık,Hedefler


class KartlarAdmin(admin.ModelAdmin):
    list_display = ('sahibi', 'kategori', 'toplam_borç', 'güncelleme_tarihi')
    list_filter = ('sahibi',) # Filtreleme seçenekleri ekler
admin.site.register(Kartlar, KartlarAdmin)   

class GelirAdmin(admin.ModelAdmin):
    list_display = ('kaynak', 'birim', 'miktar', 'tarih')  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('kaynak','birim','tarih',) # Filtreleme seçenekleri ekler  
admin.site.register(Gelir, GelirAdmin)  # Modeli admin paneline kaydeder 


class DüzenliÖdemeAdmin(admin.ModelAdmin):
    list_display = ('kategori', 'toplamtaksit' )  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('kategori',) # Filtreleme seçenekleri ekler   
admin.site.register(DüzenliÖdeme, DüzenliÖdemeAdmin)  # Modeli admin paneline kaydeder

class ÖdemedetayAdmin(admin.ModelAdmin):
    list_display = ('kategori', 'taksitsayısı', 'tutar', 'ödemeson', 'ödendimi', 'tutar')  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('kategori','ödemeson','ödendimi',) # Filtreleme seçenekleri ekler
admin.site.register(Ödemedetay, ÖdemedetayAdmin)

class GıdaAdmin(admin.ModelAdmin):
    list_display = ('harcayan', 'kategorisi', 'başlık', 'birim', 'miktar', 'tutar', 'tarih')  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('harcayan','kategorisi','başlık','tarih',) # Filtreleme seçenekleri ekler
    search_fields = ('başlık__başlık','harcayan__başlık',)  # Arama özelliğini belirler
admin.site.register(Gıda, GıdaAdmin)  # Modeli admin paneline kaydeder


class FaturaAdmin(admin.ModelAdmin):
    list_display = ('harcayan', 'kategorisi',  'tutar', 'tarih')  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('harcayan','kategorisi__başlık','tarih',) # Filtreleme seçenekleri ekler
admin.site.register(Fatura, FaturaAdmin)  # Modeli admin paneline kaydeder

class DiğerAdmin(admin.ModelAdmin):
    list_display = ('harcayan', 'kategorisi', 'başlık', 'birim', 'miktar', 'tutar', 'tarih')  # Listeleme sırasında hangi alanların görüneceğini belirler
    list_filter = ('harcayan','kategorisi__başlık','başlık', 'tarih') # Filtreleme seçenekleri ekler
admin.site.register(Diğer, DiğerAdmin)  # Modeli admin paneline kaydeder


admin.site.register(Notlar)
admin.site.register(Günlük)
admin.site.register(Haftalık)
admin.site.register(Hedefler)
admin.site.register(Sahibi)
admin.site.register(Gıdakategorisi)
admin.site.register(Kategorisi)
admin.site.register(Harcayan)
admin.site.register(Düzensizm)
admin.site.register(Düzensize)
admin.site.register(Düzensizkategori)
admin.site.register(Düzensiz)
admin.site.register(Diğerbaşlık)
admin.site.register(Faturabaşlık)
admin.site.register(Başlık)