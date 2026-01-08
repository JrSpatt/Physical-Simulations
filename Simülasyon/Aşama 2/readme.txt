Hareketli drone'a karşı elektro manyetik mermi (emp): Sürtünmeli atış simülasyonu

simulation.py dosyasını çalıştırın.
Merminin ilk hızını girin.(Derece varsayılan 10.6, Aşama 1 hızı 1200m/s)
Kritik kütle hesabı için ister critic-m-calc.py dosyasını çalıştırıp aynı hızı girin. 
Ve çıkan kütleyi simulation.py dosyasında kullanın...

İsterseniz direkt simulation(w-criticm).py dosyasını çalıştırın ve kütle, hız bilgilerini girerek hesaplama yapın.
Varsayılan parametreler: 
m=40kg
V=1310 m/s
g=9.81 #Yerçekimi ivmesi(m/s^2)
Vd=200.0 #Drone hızı(m/s)
h=1000.0 #Drone yerden yükseklik(m)
d_baslangic=5000.0 #Drone'un başlangıç yatay mesafesi(m)
k=0.005 #Sürüklenme katsayısı(kg/m)
dt=0.01 #Simülasyon zaman adımı(saniye)
dmax=10.0 #Vuruş için gereken maks mesafe(m)
