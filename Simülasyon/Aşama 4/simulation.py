import numpy as np

#PARAMETRELER VE SABİTLER
g=9.81 #Yerçekimi ivmesi(m/s^2)
h=1000.0 #Drone yerden yükseklik(m)
Vs=400 #m/s
m=40 #kg
dt=0.01 #Simülasyon zaman adımı(saniye)(Hassasiyet için 0.01 seçtim)
dmax=10.0 #Vuruş için gereken maks mesafe(m)


#KULLANICI GİRDİSİ
print("Drone Kaçış Simülasyonu)")
k_list=[0,0.005]

def sim(Vdrone,k):
    t=0.0
    xs=0.0
    ys=0.0
    vys=Vs
    xd=0
    yd=h   
    vuruldu=False
    hmax=0.0
    
    while ys>=0: #Mermi yere düşene kadar
        xd=Vdrone*t
        if k==0:
            ay=-g
        else:
            v=vys
            ay=-g-(k/m)*v*vys
        vys+=ay*dt
        ys+=vys*dt
        t+=dt
        if ys>hmax:
            hmax=ys
        
        #MESAFE HESABI
        anlik_mesafe=np.sqrt((xs-xd)**2+(ys-yd)**2)
        
        if anlik_mesafe<=dmax: 
            vuruldu=True
            break
    if hmax<h-dmax:
        return False
    return vuruldu

sonuc={}
for k in k_list:
    bulunan_hiz=0.0    
    for vdeneme in np.arange(0.0,20.0,0.01):
        vuruldumu=sim(vdeneme,k)
        if not vuruldumu:
            bulunan_hiz=vdeneme
            break
    sonuc[k]=bulunan_hiz
    durum="k=0 durumunda" if k==0 else "k=0.005 durumunda"
    print(durum,"kaçış için gerekli minimum hız: ",bulunan_hiz,"m/s")



