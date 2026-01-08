import numpy as np
import matplotlib.pyplot as plt


#PARAMETRELER VE SABİTLER
g=9.81 #Yerçekimi ivmesi(m/s^2)
Vd=200.0 #Drone hızı(m/s)
h=1000.0 #Drone yerden yükseklik(m)
d_baslangic=5000.0 #Drone'un başlangıç yatay mesafesi(m)

dt=0.01 #Simülasyon zaman adımı(saniye)(Hassasiyet için 0.01 seçtim)
dmax=10.0 #Vuruş için gereken maks mesafe(m)


#KULLANICI GİRDİSİ
print("EMP Mermisi Atış Simülasyonu(Sürtünmesiz)")
Vs=float(input("Merminin ilk hızını giriniz(m/s): "))
theta_deg=float(input("Atış açısını giriniz(0-90 derece): "))
theta=np.deg2rad(theta_deg)


# BAŞLANGIÇ KOŞULLARI

#Zaman
t=0.0
#Mermi(konum,hız bileşenleri)
xs,ys = 0.0,0.0
vxs=Vs*np.cos(theta)
vys=Vs*np.sin(theta)

#Drone konumu
xd=d_baslangic
yd=h

#Kayıt Listeleri
xs_list, ys_list = [xs], [ys]
xd_list, yd_list = [xd], [yd]

#Mesafe Takibi
dmin = np.sqrt((xs - xd)**2 + (ys - yd)**2)
basari = False


#SİMÜLASYON DÖNGÜSÜ

while ys>=0: #Mermi yere düşene kadar
    #Xd(t)=d+Vd*t
    xd=d_baslangic+Vd*t
    yd=h #Yükseklik
    
    #İvmeler (Sürtünmesiz)
    axs =0.0
    ays=-g
    #Hız Güncelleme(Euler)
    vxs+=axs*dt
    vys+=ays*dt
    
    #Konum Güncelleme
    xs+=vxs*dt
    ys+=vys*dt
    
    #MESAFE HESABI
    anlik_mesafe=np.sqrt((xs-xd)**2+(ys-yd)**2)
    
    #Uzaklaşma Kontrolü
    #Eğer anlık mesafe, kaydedilen en küçük mesafeden büyükse
    #mermi hedefi geçmiş ve uzaklaşıyor demektir.
    if anlik_mesafe<dmin:
        dmin=anlik_mesafe
    else:
        #Uzaklaşıyor sim bitir
        break
    
    #KAZANMA KOŞULU: 10mden küçükse
    if dmin<=dmax:
        basari=True
    
    #Verileri kaydet
    xs_list.append(xs)
    ys_list.append(ys)
    xd_list.append(xd)
    yd_list.append(yd)
    
    #Zamanı ilerlet
    t+=dt


#Sonuçlar ve Grafik
print("Atış Açısı: ",theta_deg,"Derece")
print("Mesafe: ",dmin,"m")
print("Geçen Süre: ",t,"s")

if basari:
    print("ZAFER! HEDEF YOK EDİLDİ!")
else:
    print(dmin,"Metre ile hedef Kaçtı!")


#Grafik Çizimi
plt.figure(figsize=(12,6))
plt.plot(xs_list, ys_list, 'b-', label='Mermi')
plt.plot(xd_list, yd_list, 'r--', label='Drone Yolu')
plt.scatter(xs_list[-1], ys_list[-1], color='black', label='Bitiş Noktası')
plt.axhline(0, color='gray', linewidth=1)
plt.title("Hava Dirençsiz Atış Simülasyonu")
plt.xlabel("Yatay Mesafe (m)")
plt.ylabel("Yükseklik (m)")
plt.legend()
plt.grid()
plt.show()