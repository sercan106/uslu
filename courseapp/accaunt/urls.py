from django.urls import path
from . import views #response için görüntü dosyasına yönlendirdik






urlpatterns = [
path('login', views.user_login, name='user_login'),
path('register', views.user_register, name='user_register'),
path('logout', views.user_logout, name='user_logout'),
    
]




# urlpatterns = [
#     path('', views.home),
#     path('borc', views.borc, name='borc'),
#     path('sonuc/<int:id>', views.sonuc, name='sonuc'),
#     path('gıda', views.gıda, name='gıda'),
#     path('aileharcama', views.aileharcama, name='aileharcama'),
#     path('kartlar', views.kartlar, name='kartlar'),
#     path('analiz', views.analiz, name='analiz'),
#     path('silgıdaharcama', views.silgıdaharcama, name='silgıdaharcama'),
    
#     path('silsercanharcama', views.silsercanharcama, name='silsercanharcama'),
#     path('silmehmetharcama', views.silmehmetharcama, name='silmehmetharcama'),
#     path('silerenharcama', views.silerenharcama, name='silerenharcama'),

#     path('sercanharcama', views.sercanharcama, name='sercanharcama'),
#     path('mehmetharcama', views.mehmetharcama, name='mehmetharcama'),
#     path('erenharcama', views.erenharcama, name='erenharcama'),



#     #______________SİL_______________________
#     path('kart_sil/<int:id>', views.kart_sil, name='kart_sil'),
#     path('sil/<int:id>', views.sil, name='sil'),
#     path('gıda_sil/<int:id>', views.gıda_sil, name='gıda_sil'),


#     #_____________________EKLE________________
#     path('ekle', views.ekle, name='ekle'),
#     path('kart_ekle', views.kart_ekle, name='kart_ekle'),
#     path('eklegıda', views.eklegıda, name='eklegıda'),
#     path('gıdaisimekle', views.gıdaisimekle, name='gıdaisimekle')

    




    # path('iletişim', views.kurslar),
    # path('search', views.search, name='search'),#arama sayfası burası
    # path('post', views.post, name='post'),#post
    # path('post2', views.post2, name='post2'),#post etme ve girilen verileri kontrol etme
    # path('ürün_detay', views.ürün_detay, name='ürün_detay'),
    # path('güncelle/<int:idurls>', views.güncelle, name='güncelle'),
    # path('sil/<int:idurls>', views.sil, name='sil'),
    # path('yükle', views.yükle, name='resim_yükle'),
    # path('index', views.index),
    # path('index/<int:kategori>', views.kategori),
    # path('veritabanı', views.veritabanı),
    
    # path('anasayfa', views.anasayfa),
    # path('<int:kategori>',views.dinamik),#burda ketegori değişkenimizi oluşturduk.Eğer str türünde veri
    # #alırsa views.dinamik çalışır
    # #not:yukarıdan aşağıya okuma yaptığı için üstte şartı karşılayan bir path varsa onu görür 
    # #aşağıdakileri görmez.
    # path('<str:kategori>',views.dinamikstr),
# ]
    

