import numpy as np
import matplotlib.pyplot as plt


#PARAMETRELER VE SABİTLER
g=9.81 #Yerçekimi ivmesi(m/s^2)
Vd=200.0 #Drone hızı(m/s)
h=1000.0 #Drone yerden yükseklik(m)
d_baslangic=5000.0 #Drone'un başlangıç yatay mesafesi(m)
k=0.005 #Sürüklenme katsayısı(kg/m)
dt=0.01 #Simülasyon zaman adımı(saniye)(Hassasiyet için 0.01 seçtim)
dmax=10.0 #Vuruş için gereken maks mesafe(m)


#KULLANICI GİRDİSİ
print("EMP Mermisi Atış Simülasyonu(Sürtünmeli)")
theta_deg=10.6
m=float(input("Mermi kütlesini giriniz(kg): ")) 
Vs=float(input("Merminin ilk hızını giriniz(m/s): "))
theta=np.deg2rad(theta_deg)

def vurabilir_mi(mk):
    for theta_deg in np.arange(0.0, 90.0, 0.5):
        theta=np.deg2rad(theta_deg)
        xs,ys = 0.0, 0.0
        vxs=Vs*np.cos(theta)
        vys=Vs*np.sin(theta)
        t=0.0
        tmax=10
        d=np.inf
        
        while ys>=0 and t<tmax:
            xd=d_baslangic+Vd*t
            yd=h

            v=np.sqrt(vxs**2 + vys**2)
            ax=-(k/mk)*v*vxs
            ay=-g-(k/mk)*v*vys
            vxs+=ax*dt
            vys+=ay*dt
            xs+=vxs*dt
            ys+=vys*dt
            t+=dt
            
            d=np.sqrt((xs-xd)**2 + (ys-yd)**2)

            if d<=dmax:
                return True
    return False
#KÜTLE TARAMASI (drone'a 10m yaklaşabileceği minimum kütle)
for mk in np.arange(1.0, 100.0, 0.5):
    if vurabilir_mi(mk):
        print("Kritik minimum mermi kütlesi:", mk, "kg")
        break


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
ay_list=[]
t_list=[]
#Mesafe Takibi
dmin = np.sqrt((xs - xd)**2 + (ys - yd)**2)
basari = False


#SİMÜLASYON DÖNGÜSÜ

while ys>=0: #Mermi yere düşene kadar
    #Xd(t)=d+Vd*t
    xd=d_baslangic+Vd*t
    yd=h #Yükseklik
    v=np.sqrt(vxs**2+vys**2) #Hava direnci
    #İvmeler 
    ax=-(k/m)*v*vxs
    ay=-g-(k/m)*v*vys
    #Hız Güncelleme(Euler)
    vxs+=ax*dt
    vys+=ay*dt
    
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
        break
    #Verileri kaydet
    xs_list.append(xs)
    ys_list.append(ys)
    xd_list.append(xd)
    yd_list.append(yd)
    ay_list.append(ay)
    t_list.append(t)
    #Zamanı ilerlet
    t+=dt
#ay verilerini kaydetme
#ay verileri binlerce olacağından ekrana yazdırmak mantıksız
dosya_adi = "ay_verileri.txt"
with open(dosya_adi, "w", encoding="utf-8") as dosya:
    dosya.write("Zaman(s)\tIvme_y(m/s^2)\n")
    dosya.write("-" * 30 + "\n")    
    for zaman, ivme in zip(t_list, ay_list):
        # Format: virgülden sonra 2 hane zaman, 4 hane ivme
        dosya.write(f"{zaman:.2f}\t\t{ivme:.4f}\n")
print("ay verileri ay_verileri.txt dosyasına kaydedildi")

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
plt.scatter(xs_list[-1], ys_list[-1], color='black', label='Bitiş')
plt.axhline(0, color='gray', linewidth=1)
plt.title("Hava Dirençli Atış Simülasyonu")
plt.xlabel("Yatay Mesafe (m)")
plt.ylabel("Yükseklik (m)")
plt.legend()
plt.grid()
plt.show()