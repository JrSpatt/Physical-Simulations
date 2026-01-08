import numpy as np

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
Vs=float(input("Merminin ilk hızını giriniz: "))
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