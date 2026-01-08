import numpy as np
import matplotlib.pyplot as plt


#PARAMETRELER VE SABİTLER
g=9.81 #Yerçekimi ivmesi(m/s^2)
Vd=200.0 #Drone hızı(m/s)
h=1000.0 #Drone yerden yükseklik(m)
d_baslangic=5000.0 #Drone'un başlangıç yatay mesafesi(m)
k=0.005 #Sürüklenme katsayısı(kg/m)
m=40.0 #Mermi(kg)
dt=0.01 #Simülasyon zaman adımı(saniye)(Hassasiyet için 0.01 seçtim)
dmax=10.0 #Vuruş için gereken maks mesafe(m)
Vs=1310 #m/s
#Tetaya karşı dmin çizdirmek için listeler
teta_list=[]
dmin_list=[]
#KULLANICI GİRDİSİ
print("EMP Mermisi Atış Simülasyonu(Optimize)")

print("Atış hızı",Vs,"m/s için açı aranıyor")

#Açı tarama döngüsü
for deneme in np.arange(0.0, 90.0, 0.1):
    theta = np.deg2rad(deneme)
    t=0.0
    xs,ys=0.0,0.0
    vxs=Vs*np.cos(theta)
    vys=Vs*np.sin(theta)
    xd=d_baslangic
    yd=h
    dmin_teta=np.sqrt((xs - xd)**2 + (ys - yd)**2)
    
    while ys>=0: #Mermi yere düşene kadar
        # Xd(t)=d+Vd*t
        xd = d_baslangic+Vd*t
        yd = h #Yükseklik
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
        t+=dt
        #MESAFE HESABI
        anlik_mesafe=np.sqrt((xs-xd)**2+(ys-yd)**2)
        
        #Uzaklaşma Kontrolü
        #Eğer anlık mesafe, kaydedilen en küçük mesafeden büyükse
        #mermi hedefi geçmiş ve uzaklaşıyor demektir.
        if anlik_mesafe<dmin_teta:
            dmin_teta=anlik_mesafe
        else:
            #Uzaklaşıyor sim bitir
            break
        
    #SONUÇLARI LİSTEYE KAYYDET    
    teta_list.append(deneme)
    dmin_list.append(dmin_teta)
    
#En iyi sonucu seçiyoruz    
en_kucuk_dminteta=min(dmin_list)
indeks=dmin_list.index(en_kucuk_dminteta)    
teta_opt=teta_list[indeks]


print("En küçük yaklaşma mesafesi: ",en_kucuk_dminteta) 
print("En iyi yaklaşma açısı: ",teta_opt,"derece")   
    #Vurduk mu?
if en_kucuk_dminteta<=dmax:
    print("ZAFER! HEDEF YOK EDİLDİ!")
else:
    print("Bu hız ve kütle ile uygun bir açı bulunamadı.")
    
#Bulunan en iyi açıyı burada kullanıp hedefi vuruyoruz
#Ve verileri buradan alıp kaydediyoruz
theta=np.deg2rad(teta_opt)
# BAŞLANGIÇ KOŞULLARI
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
ay_list=[]
t_list=[]
#Mesafe Takibi
dmin=np.sqrt((xs - xd)**2 + (ys - yd)**2)
basari=False
#ilk grafikteki en iyi noktayı işaretlemek için x ve y'nin en yakın olduğu konumu bulacağız
x_eniyi=0.0
y_eniyi=0.0

#SİMÜLASYON DÖNGÜSÜ

while ys>=0: #Mermi yere düşene kadar
    #Xd(t)=d+Vd*t
    xd=d_baslangic+Vd*t
    yd=h #Yükseklik
    v=np.sqrt(vxs**2+vys**2) #Hava direnci
    #İvmeler 
    ax=-(k/m)*v*vxs
    ay=-g-(k/m)*v*vys
    
    #ivmeleri kaydet
    ay_list.append(ay)
    t_list.append(t)
    
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
        basari=True
        x_eniyi=xs
        y_eniyi=ys
        break
    #Verileri kaydet
    xs_list.append(xs)
    ys_list.append(ys)
    xd_list.append(xd)
    yd_list.append(yd)


#ay verilerini kaydetme
#ay verileri binlerce olacağından ekrana yazdırmak mantıksız
dosya_adi = "aci-dmin.txt"
with open(dosya_adi, "w", encoding="utf-8") as dosya:
    dosya.write("Açı(derece)\tDmin(metre)\n")
    dosya.write("-" * 30 + "\n")    
    for açı, dmin in zip(teta_list, dmin_list):
        # Format: virgülden sonra 2 hane zaman, 4 hane ivme
        dosya.write(f"{açı:.2f}\t\t{dmin:.4f}\n")
print("Opt açıya karşılık gelen dmin verileri aci-dmin.txt dosyasına kaydedildi")




#Grafik Çizimi
plt.figure(figsize=(12,6))
plt.plot(xs_list, ys_list, 'b-', label='Mermi')
plt.plot(xd_list, yd_list, 'r--', label='Drone Yolu')
plt.scatter(x_eniyi, y_eniyi, color='black', label='En Yakın Konum')
plt.title("Hava Dirençli EMP Atış Simülasyonu")
plt.xlabel("Yatay Mesafe (m)")
plt.ylabel("Yükseklik (m)")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12,6))
plt.plot(teta_list, dmin_list,'g-', label='dmin(teta)')
plt.plot(teta_opt, en_kucuk_dminteta, 'ro', label='Optimum Nokta')
plt.title("OPTIMUM Açı Grafiği")
plt.xlabel("Teta (Derece)")
plt.ylabel("dmin (Metre)")
plt.axhline(dmax, color='red', linestyle='--', label='Vuruş Limiti (10m)')
plt.legend()
plt.grid(True)
plt.show()







