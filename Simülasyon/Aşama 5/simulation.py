import numpy as np
import matplotlib.pyplot as plt

#PARAMETRELER VE SABİTLER
g=9.81 #Yerçekimi ivmesi(m/s^2)
Vd=200.0 #Drone hızı(m/s)
h=1000.0 #Drone yerden yükseklik(m)
d_baslangic=5000.0 #Drone'un başlangıç yatay mesafesi(m)
m=40.0 #Mermi(kg)
dt=0.01 #Simülasyon zaman adımı(saniye)(Hassasiyet için 0.01 seçtim)
dmax=10.0 #Vuruş için gereken maks mesafe(m)


#KULLANICI GİRDİSİ
print("Aynı Hızda 2 Açı Problemi")
k_list=[0,0.005]

Vs=2000 #m/s


def vurdumu(aci,k):
    theta = np.deg2rad(aci)
    t=0.0
    xs,ys=0.0,0.0
    vxs=Vs*np.cos(theta)
    vys=Vs*np.sin(theta)
    xd=d_baslangic
    yd=h
    
    while ys>=0: #Mermi yere düşene kadar
        #Xd(t)=d+Vd*t
        xd = d_baslangic+Vd*t
        v=np.sqrt(vxs**2+vys**2) #Hava direnci
        #İvmeler
        if k==0:
            ax,ay=0,-g
        else:
            ax=-(k/m)*v*vxs
            ay=-g-(k/m)*v*vys
            
        #Hız Güncelleme(Euler)
        vxs+=ax*dt
        vys+=ay*dt          
        #Konum Güncelleme
        xs+=vxs*dt
        ys+=vys*dt
        t+=dt
    
    #MESAFE HESABI
        mesafe=np.sqrt((xs-xd)**2+(ys-yd)**2)
    
    #Uzaklaşma Kontrolü
        if mesafe<=dmax:
            return True
    return False

  
def sim(aci,k):
    theta=np.deg2rad(aci)
    #BAŞLANGIÇ KOŞULLARI
    #Zaman
    t=0.0
    #Mermi(konum,hız bileşenleri)
    xs,ys=0.0,0.0
    vxs=Vs*np.cos(theta)
    vys=Vs*np.sin(theta)

    #Drone konumu
    xd=d_baslangic
    yd=h

    #Kayıt Listeleri
    xs_list, ys_list = [xs], [ys]
    xd_list, yd_list = [xd], [yd]

    vurdu=False

    #SİMÜLASYON DÖNGÜSÜ

    while ys>=0: #Mermi yere düşene kadar
        #Xd(t)=d+Vd*t
        xd=d_baslangic+Vd*t
        v=np.sqrt(vxs**2+vys**2) #Hava direnci
        #İvmeler 
        if k==0:
            ax,ay=0,-g
        else:
            ax=-(k/m)*v*vxs
            ay=-g-(k/m)*v*vys
        
        
        #Hız Güncelleme(Euler)
        vxs+=ax*dt
        vys+=ay*dt
        
        #Konum Güncelleme
        xs+=vxs*dt
        ys+=vys*dt
        t+=dt
        #MESAFE HESABI
        anlik_mesafe=np.sqrt((xs-xd)**2+(ys-yd)**2)
               
        #KAZANMA KOŞULU: 10mden küçükse
        if anlik_mesafe<=dmax:
            vurdu=True
            break
        #Verileri kaydet
        xs_list.append(xs)
        ys_list.append(ys)
        xd_list.append(xd)
        yd_list.append(yd)
    return xs_list, ys_list, xd_list, yd_list, vurdu

for k in k_list:
    print("Açı bulunuyor: k =", k)
    
    bulunan_acilar = []

    acilar = np.arange(0.1, 89.9, 0.1)
    for ang in acilar:
        if vurdumu(ang,k):
            #Eğer liste boşsa, bu ilk açı
            if len(bulunan_acilar) == 0:
                bulunan_acilar.append(ang)
                print("1. Açı Bulundu:", ang)
            elif len(bulunan_acilar) == 1:
                ilk_aci=bulunan_acilar[0]
                if (ang-ilk_aci) > 10.0:
                    bulunan_acilar.append(ang)
                    print("2. Açı Bulundu:", ang)
                    break 


    if len(bulunan_acilar) > 0:
        plt.figure(figsize=(10, 6))
    #Drone yolunu bir kez çizmek için T-F anahtarı
        drone_cizildi = False
        for i, hedef_aci in enumerate(bulunan_acilar):
            xs, ys, xd, yd, vurdu = sim(hedef_aci, k)
            renk = 'blue' if i == 0 else 'red'
            etiket = f"{'Düşük' if i == 0 else 'Yüksek'} Açı: {hedef_aci:.1f}°"
            plt.plot(xs, ys, color=renk, label=etiket)
            if vurdu:
                plt.scatter(xs[-1], ys[-1], c='black', s=80)
            if not drone_cizildi:
                plt.plot(xd, yd, 'k--', label='Drone Yolu')
                drone_cizildi = True
        plt.title("İki Farklı Açı Analizi")
        plt.xlabel("Mesafe (m)")
        plt.ylabel("Yükseklik (m)")
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("Çözüm bulunamadı.")

            






