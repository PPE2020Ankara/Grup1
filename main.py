import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTest import *
from PyQt5.QtCore import Qt
import sqlite3
import pandas as pd

# csv dosyasını okuma ve nan değerleri unknown olarak değiştirme

df = pd.read_csv('netflix_titles.csv')
df = df.fillna(value= "unknown")

# formlarda kullanılan yazı fontları ve stilleri burada tanımlanıyor

baslikfont = QFont("Century Gothic",20)
butonFont = QFont("Century Gothic",14)
yaziFont = QFont("Century Gothic",14)
formYaziFont = QFont("Century Gothic",12)
uyariFont = QFont("Century Gothic",14,)
yaziSitil = "color :white"
yaziSitilB = "color :white;font-weight:bold;"
baslikSitil = "color :red;font-weight:bold;"
uyariSitil = "color :red"
editSitil = "color :black;background-color :white"
btnSitil = "color :black;background-color :gray"
pencereSitil = "background-color :black"

# veritabanı bağlantısı tablo yoksa oluşturuluyor 

baglanti = sqlite3.connect("vt.db")
kalem = baglanti.cursor()
kalem.execute("""CREATE TABLE IF NOT EXISTS "kullanici" (
	"id"	INTEGER UNIQUE,
	"kullaniciAdi"	TEXT UNIQUE,
	"parola"	TEXT,
    "adSoyad"	TEXT,
	"dogumTarihi"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)""")

# yeni kullanıcı kayıt formu için sınıf tanımı

class KayitFormu(QWidget):
    def __init__(self):
        super().__init__()  
                
        pencereBaslik = "Kullanıcı Kaydı"
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()
        yatayAdi = QHBoxLayout()
        yatayKadi = QHBoxLayout()
        yatayParola = QHBoxLayout()
        yatayDtarihi = QHBoxLayout()
        yatayUyari = QHBoxLayout()
        yatayBtn = QHBoxLayout()
        

        baslik = QLabel("KULLANICI KAYIT EKRANI")
        baslik.setFixedWidth(500)
        baslik.setStyleSheet(yaziSitil)
        baslik.setFont(baslikfont)
        aciklama = QLabel("Kayıt için formu doldurunuz")        
        aciklama.setStyleSheet(uyariSitil)
        
        self.adSoyad = QLineEdit(font=formYaziFont)
        self.adSoyad.setStyleSheet(editSitil)
        self.adSoyad.setFixedWidth(200)
        self.adSoyad.setPlaceholderText("Adınız ve Soyadınız")
        
        self.kAdi = QLineEdit(font=formYaziFont)
        self.kAdi.setStyleSheet(editSitil)
        self.kAdi.setFixedWidth(200)
        self.kAdi.setPlaceholderText("Kullanici adiniz")

        self.kParola = QLineEdit(font=formYaziFont)
        self.kParola.setStyleSheet(editSitil)
        self.kParola.setFixedWidth(200)
        self.kParola.setPlaceholderText("Parolanız")
        self.kParola.setEchoMode(QLineEdit.Password)
        
        self.dTarihi = QLineEdit(font=formYaziFont)
        self.dTarihi.setStyleSheet(editSitil)
        self.dTarihi.setFixedWidth(200)
        self.dTarihi.setPlaceholderText("Doğum yılınız")
        
        yeniEkle = QPushButton("Kayıt Ol")
        yeniEkle.setFont(butonFont)
        yeniEkle.setStyleSheet(btnSitil)
        yeniEkle.setFixedWidth(200)
        yeniEkle.clicked.connect(self.yeniEkle)
        
        self.uyari = QLabel("",font=uyariFont)
        self.uyari.setStyleSheet(uyariSitil)
        yatayUyari.addWidget(self.uyari)

        adS = QLabel("Ad ve Soyad",font=formYaziFont)
        adS.setStyleSheet(yaziSitil)
        
        
        yatayAdi.addWidget(adS)
        yatayAdi.addStretch()
        yatayAdi.addWidget(self.adSoyad)
        
        kulAdi = QLabel("Kullanıcı Adı",font=formYaziFont)
        kulAdi.setStyleSheet(yaziSitil)
        
        yatayKadi.addWidget(kulAdi)
        yatayKadi.addStretch()
        yatayKadi.addWidget(self.kAdi)
        
        kulP = QLabel("Parola",font=formYaziFont)
        kulP.setStyleSheet(yaziSitil)
        
        yatayParola.addWidget(kulP)
        yatayParola.addStretch()
        yatayParola.addWidget(self.kParola)
        
        dogT = QLabel("Doğum Tarihi",font=formYaziFont)
        dogT.setStyleSheet(yaziSitil)
        
        yatayDtarihi.addWidget(dogT)
        yatayDtarihi.addStretch()
        yatayDtarihi.addWidget(self.dTarihi)

        
        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addStretch()        
        
        dikey.addLayout(yatayAdi)
        dikey.addLayout(yatayKadi)
        dikey.addLayout(yatayParola)
        dikey.addLayout(yatayDtarihi)
        dikey.addLayout(yatayUyari)
        
        yatayBtn.addStretch()
        yatayBtn.addWidget(yeniEkle)
        
        dikey.addStretch()
        dikey.addLayout(yatayBtn)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setFixedSize(500, 500)
        self.setStyleSheet(pencereSitil)
        self.setWindowTitle(pencereBaslik)

# yeni kullanıcı formundan gelen bilgilerin veritabanına eklenmesi icin tanımlanan fonksiyon

    def yeniEkle(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        
        adSoyad = self.adSoyad.text()
        kAdi = self.kAdi.text()
        kParola = self.kParola.text()        
        dTarihi = self.dTarihi.text()
                   
        if len(adSoyad)<4:
            self.uyari.setText("Adınız Soyadınız enaz 4 karakter olmalı !")
        elif len(kAdi)<4:
            self.uyari.setText("Kullanıci adı enaz 4 karakter olmalı !")
        elif len(kParola)<4:
            self.uyari.setText("Parola enaz 4 karakter olmalı !")
        elif(len(dTarihi)!=4 or not dTarihi.isnumeric()) :
            self.uyari.setText("Doğum tarihi hatalı!")            
        else:
            dTarihi = int(self.dTarihi.text())
            kontrol = kalem.execute("SELECT * FROM kullanici WHERE kullaniciAdi = ?",(kAdi,))
            durum = kontrol.fetchall()
            if len(durum)>0:
               self.uyari.setText("Bu kullanici adı kayıtlı")
            else:
                kalem.execute("INSERT INTO kullanici (kullaniciAdi,parola,adSoyad,dogumTarihi) VALUES (?,?,?,?)",(kAdi,kParola,adSoyad,dTarihi))
                baglanti.commit()
                self.uyari.setText("Kullanıcı kaydınız oluşturuldu")
                QTest.qWait(500)          
                #self.close()          
 
 #formu kapatmak için kullanılacak fonksiyon
    
    def geriDon(self):
        self.close()   # Formu kapatmak için kullanılacak

# kullanıcı bilgilerinin güncellenmesi için açılacak form

class KayitGuncelle(QWidget):
    def __init__(self):
        super().__init__()  
                
        pencereBaslik = "Kullanıcı Güncelle"
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()
        yatayAdi = QHBoxLayout()
        yatayKadi = QHBoxLayout()
        yatayParola = QHBoxLayout()
        yatayDtarihi = QHBoxLayout()
        yatayUyari = QHBoxLayout()
        yatayBtn = QHBoxLayout()
        
        kAdi = GirisEkrani.kullanici
        
        kontrol = kalem.execute("SELECT * FROM kullanici WHERE kullaniciAdi = ?",(kAdi,))
        kBilgileri = kontrol.fetchall()[0]
        

        baslik = QLabel("BİLGİ GÜNCELLEME")
        baslik.setFixedWidth(500)
        baslik.setStyleSheet(yaziSitil)
        baslik.setFont(baslikfont)
        aciklama = QLabel("Güncelleme için formu doldurunuz")        
        aciklama.setStyleSheet(uyariSitil)
        
        self.adSoyad = QLineEdit(font=formYaziFont)
        self.adSoyad.setStyleSheet(editSitil)
        self.adSoyad.setFixedWidth(200)
        self.adSoyad.setText(kBilgileri[3])
        
        self.kAdi = QLabel(kBilgileri[1],font=formYaziFont)
        self.kAdi.setStyleSheet(yaziSitil)
        self.kAdi.setFixedWidth(200)       
        
        self.kParola = QLineEdit(font=formYaziFont)
        self.kParola.setStyleSheet(editSitil)
        self.kParola.setFixedWidth(200)
        self.kParola.setText(kBilgileri[2])
        self.kParola.setEchoMode(QLineEdit.Password)
        
        self.dTarihi = QLineEdit(font=formYaziFont)
        self.dTarihi.setStyleSheet(editSitil)
        self.dTarihi.setFixedWidth(200)
        self.dTarihi.setText(str(kBilgileri[4]))
        
        yeniEkle = QPushButton("GÜNCELLE")
        yeniEkle.setFont(butonFont)
        yeniEkle.setStyleSheet(btnSitil)
        yeniEkle.setFixedWidth(200)
        yeniEkle.clicked.connect(self.guncelle)
        
        self.uyari = QLabel("",font=uyariFont)
        self.uyari.setStyleSheet(uyariSitil)
        yatayUyari.addWidget(self.uyari)
                
        kulAdi = QLabel("Kullanıcı Adı",font=formYaziFont)
        kulAdi.setStyleSheet(yaziSitil)
        
        yatayKadi.addWidget(kulAdi)
        yatayKadi.addStretch()
        yatayKadi.addWidget(self.kAdi)
        
        adS = QLabel("Ad ve Soyad",font=formYaziFont)
        adS.setStyleSheet(yaziSitil)        
        
        yatayAdi.addWidget(adS)
        yatayAdi.addStretch()
        yatayAdi.addWidget(self.adSoyad)
        
        kulP = QLabel("Parola",font=formYaziFont)
        kulP.setStyleSheet(yaziSitil)
        
        yatayParola.addWidget(kulP)
        yatayParola.addStretch()
        yatayParola.addWidget(self.kParola)
        
        dogT = QLabel("Doğum Tarihi",font=formYaziFont)
        dogT.setStyleSheet(yaziSitil)
        
        yatayDtarihi.addWidget(dogT)
        yatayDtarihi.addStretch()
        yatayDtarihi.addWidget(self.dTarihi)

        
        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addStretch()        
        
        dikey.addLayout(yatayKadi)
        dikey.addLayout(yatayAdi)        
        dikey.addLayout(yatayParola)
        dikey.addLayout(yatayDtarihi)
        dikey.addLayout(yatayUyari)
        
        yatayBtn.addStretch()
        yatayBtn.addWidget(yeniEkle)
        
        dikey.addStretch()
        dikey.addLayout(yatayBtn)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setFixedSize(500, 500)
        self.setStyleSheet(pencereSitil)
        self.setWindowTitle(pencereBaslik)

# güncelleme formundan gelen bilgilerin veritabanına yazılması için kullanılan fonksiyon

    def guncelle(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        
        adSoyad = self.adSoyad.text() 
        kAdi = self.kAdi.text()       
        kParola = self.kParola.text()        
        dTarihi = self.dTarihi.text()
                   
        if len(adSoyad)<4:
            self.uyari.setText("Adınız Soyadınız enaz 4 karakter olmalı !")
        elif len(kParola)<4:
            self.uyari.setText("Parola enaz 4 karakter olmalı !")
        elif(len(dTarihi)!=4 or not dTarihi.isnumeric()) :
            self.uyari.setText("Doğum tarihi hatalı!")            
        else:
            dTarihi = int(self.dTarihi.text())       
            
            kalem.execute("UPDATE kullanici SET parola=? WHERE kullaniciAdi=?",(kParola,kAdi))
            kalem.execute("UPDATE kullanici SET adSoyad=? WHERE kullaniciAdi=?",(adSoyad,kAdi))
            kalem.execute("UPDATE kullanici SET dogumTarihi=? WHERE kullaniciAdi=?",(dTarihi,kAdi))
            baglanti.commit()
            self.uyari.setText("Bilgileriniz Güncellendi")
            QTest.qWait(500)          
            #self.close()          
 
    def geriDon(self):
        self.close()   # Formu kapatmak için kullanılacak

# filitre ekranı formu

class FiltreEkrani(QWidget):
    def __init__(self):
        super().__init__()        

        pencereBaslik = "Netflix Filtreleme Ekranı"        
        yatay0 = QHBoxLayout()
        dikey1 = QVBoxLayout()
        dikey2 = QVBoxLayout()
        yatayBtn = QHBoxLayout()
        yatayBosluk = QHBoxLayout()   
        
        
        logo = QLabel("FİLTRE EKRANI")
        logo.setFixedHeight(175)
        logo.setFixedWidth(250)
        logo.setPixmap(QPixmap("logoF.png"))
        
        baslik = QLabel("Netflix Filtreleme")
        baslik.setFixedHeight(100)
        baslik.setStyleSheet(baslikSitil)
        baslik.setFont(baslikfont)       
        
        turL = QLabel("Tür")
        turL.setFixedHeight(75)
        turL.setStyleSheet(yaziSitilB)
        turL.setFont(yaziFont)
        
        turler = self.bilgiAl(df["type"])   # bilgiAl fonksiyonu csv den türleri verir
        
        self.tur = QComboBox()
        self.tur.setStyleSheet(editSitil)
        self.tur.setFont(yaziFont)
        self.tur.addItem("Seçiniz")
        self.tur.addItems(turler)
        
               
        ulkeL = QLabel("Ülke")
        ulkeL.setFixedHeight(75)
        ulkeL.setStyleSheet(yaziSitilB)
        ulkeL.setFont(yaziFont)
        
        ulkeler = self.bilgiAl(df["country"])
        ulkeler[0] = "Seçiniz" # bilgiAl fonksiyonu csv den ülkeleri verir 
        
        self.ulke = QComboBox()
        self.ulke.setStyleSheet(editSitil)
        self.ulke.setFont(yaziFont)
        self.ulke.addItems(ulkeler)
        
        yonetmenL = QLabel("Yönetmen")
        yonetmenL.setFixedHeight(75)
        yonetmenL.setStyleSheet(yaziSitilB)
        yonetmenL.setFont(yaziFont)
        
        self.yonetmen = QLineEdit()
        self.yonetmen.setStyleSheet(editSitil)
        self.yonetmen.setFont(yaziFont) 
        
        sureL = QLabel("Süre")
        sureL.setFixedHeight(75)
        sureL.setStyleSheet(yaziSitilB)
        sureL.setFont(yaziFont)
        
        self.sure = QSlider(Qt.Horizontal,self)
        self.sure.setRange(0, 200)
        self.sure.setFocusPolicy(Qt.NoFocus)
        self.sure.setPageStep(5)
        self.sure.setStyleSheet(editSitil)
        self.sure.setFont(yaziFont) 
        
                       
        guncelle = QPushButton("Bilgilerimi Güncelle",font=butonFont)
        guncelle.setFixedWidth(350)
        guncelle.setStyleSheet(btnSitil)       
        guncelle.clicked.connect(self.guncellemeFormu)
        
        listeleBnt = QPushButton("Listele",font=butonFont)
        listeleBnt.setFixedWidth(100)
        listeleBnt.setStyleSheet(btnSitil)       
        listeleBnt.clicked.connect(self.listele)
        
        indirBtn = QPushButton("Dosyayı İndir",font=butonFont)
        indirBtn.setFixedWidth(170)
        indirBtn.setStyleSheet(btnSitil)       
        indirBtn.clicked.connect(self.dosyaIndir)
        
        cikisBtn = QPushButton("Çıkış",font=butonFont)
        cikisBtn.setFixedWidth(170)
        cikisBtn.setStyleSheet(btnSitil)       
        cikisBtn.clicked.connect(self.cikis)
        
        self.sonuclar = QListWidget()
        self.sonuclar.setFixedWidth(700)
        self.sonuclar.setFixedHeight(500)
        self.sonuclar.setStyleSheet(editSitil)
        self.sonuclar.setFont(yaziFont) 
        
        
        dikey1.addWidget(logo)
        dikey1.addWidget(turL)
        dikey1.addWidget(self.tur)
        dikey1.addWidget(ulkeL)
        dikey1.addWidget(self.ulke)
        dikey1.addWidget(yonetmenL)
        dikey1.addWidget(self.yonetmen)
        dikey1.addWidget(sureL)
        dikey1.addWidget(self.sure)
        dikey1.addWidget(listeleBnt)
        dikey1.addStretch()
        
        yatayBtn.addStretch()
        yatayBtn.addWidget(indirBtn)
        yatayBtn.addWidget(cikisBtn)
        
        bosluk = QLabel("")
        bosluk.setFixedHeight(50)
        yatayBosluk.addWidget(bosluk)
                
        dikey2.addWidget(baslik)
        dikey2.addWidget(self.sonuclar)
        dikey2.addStretch()  
        dikey2.addLayout(yatayBtn)
        dikey2.addLayout(yatayBosluk)
                     
        yatay0.addStretch()
        yatay0.addLayout(dikey1)
        yatay0.addStretch()
        yatay0.addLayout(dikey2) 
        yatay0.addStretch()     
                     

        self.setLayout(yatay0)
        self.setGeometry(200,200,1024,768)
        self.setFixedSize(1054, 768)
        self.setWindowTitle(pencereBaslik)
        self.setStyleSheet(pencereSitil)
    
    # güncelle butonu ile güncelleme formunun açılması için kullanılan fonksiyon
    def guncellemeFormu(self):
        self.gFormu = KayitGuncelle()   # kayıt güncelleme formunu açar
        self.gFormu.show()
    # filtreler seçildikten sonra listeleme sonuçlarının gösterilmesi    
    def listele(self):
        pass   # listeleme komutları indirme komutları
    
    # dosya indirme işlemlerinin yapıldığı fonksiyon
    def dosyaIndir(self):
        pass   # dosya indirme komutları        
  
# çıkış butonuna basılması ile çalışacak fonksiyon
    def cikis(self):
        qApp.quit()   # çıkış  için kullanılacak
        
    def bilgiAl(self,veri): # csv dosyasından istyenilen sütünları liste olarak sıralı bir şekilde geri döndürür
        kume =set()
        veriler = veri.tolist()
        for i in veriler:
            for j in i.split(","):
                kume.add(j.strip())

        result = sorted(list(kume))
        return result

# kullanıcı giriş ekranı
class GirisEkrani(QWidget):
    
    kullanici = ""
    
    def __init__(self):
        super().__init__()
        
        kullanici = ""
        anaEkran = QVBoxLayout()
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()        
        yatayGiris = QHBoxLayout()
        yatayKayit = QHBoxLayout()
        dikeyEdit = QVBoxLayout()
        yatayEdit = QHBoxLayout()
        yatayAdi = QHBoxLayout()
        yatayParola = QHBoxLayout()
        yatayUyari = QHBoxLayout()
        yatayLogo = QHBoxLayout()

        self.yazi = QLabel("Netflix'de arama yapmanın kolay yolu")
        self.yazi.setStyleSheet(baslikSitil)
        self.yazi.setFixedHeight(100)
        self.yazi.setFont(baslikfont)
        
        self.pencereBaslik = "Netflix Filtreleme Programı"
        self.logo = QLabel("Logo")        
        self.logo.setPixmap(QPixmap("logo.png"))
        
        self.kAdi = QLineEdit(font=yaziFont)
        self.kAdi.setStyleSheet(editSitil)
        self.kAdi.setFixedWidth(350)
        self.kAdi.setFixedHeight(45)
        self.kAdi.setPlaceholderText("Kullanici adinizi giriniz")              

        self.kParola = QLineEdit(font=yaziFont)
        self.kParola.setPlaceholderText("Parolanızı giriniz")
        self.kParola.setStyleSheet(editSitil)
        self.kParola.setFixedWidth(350)
        self.kParola.setFixedHeight(45)
        self.kParola.setEchoMode(QLineEdit.Password)
        
        self.giris = QPushButton("Giris Yap",font=butonFont)
        self.giris.setFixedWidth(350)
        self.giris.setStyleSheet(btnSitil)
        self.giris.clicked.connect(self.girisKontrol)
        
        self.kaydol = QPushButton("Kayıt Ol",font=butonFont)
        self.kaydol.setFixedWidth(350)
        self.kaydol.setStyleSheet(btnSitil)       
        self.kaydol.clicked.connect(self.kayitFormu)
        
        self.uyari = QLabel("",font=uyariFont)
        self.uyari.setStyleSheet(baslikSitil)
        yatayUyari.addWidget(self.uyari)
        
        yatayLogo.addStretch()
        yatayLogo.addWidget(self.logo)
        yatayLogo.addStretch()
    
        kullaniciA = QLabel("Kullanıcı Adı",font=yaziFont)
        kullaniciA.setStyleSheet(yaziSitil) 
                              
        yatayAdi.addWidget(kullaniciA)
        yatayAdi.addWidget(self.kAdi) 
        
        kullaniciP = QLabel("Parola",font=yaziFont)
        kullaniciP.setStyleSheet(yaziSitil)       
        
        yatayParola.addWidget(kullaniciP)
        yatayParola.addWidget(self.kParola)       
        
        dikeyEdit.addLayout(yatayLogo)        
        dikeyEdit.addWidget(self.yazi)
        dikeyEdit.addLayout(yatayAdi)
        dikeyEdit.addLayout(yatayParola)
        dikeyEdit.addLayout(yatayUyari)
        
        yatayEdit.addStretch()
        yatayEdit.addLayout(dikeyEdit)
        yatayEdit.addStretch()
        
        
        yatayGiris.addStretch()
        yatayGiris.addWidget(self.giris)
        
        yatayKayit.addStretch()
        yatayKayit.addWidget(self.kaydol)

        dikey.addStretch()
        dikey.addLayout(yatayEdit)        
        dikey.addLayout(yatayGiris)
        dikey.addLayout(yatayKayit)
        dikey.addStretch()
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()  
        
        
        anaEkran.addLayout(yatay)

        self.setLayout(anaEkran)
        
        self.setFixedSize(800, 600)
        self.setWindowTitle(self.pencereBaslik)
        self.setStyleSheet(pencereSitil)
        self.show()
        

    def kayitFormu(self):
        self.kFormu = KayitFormu()   # kayıt formunu açar
        self.kFormu.show()
    
    def girisKontrol(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        kAdi = self.kAdi.text()
        kParola = self.kParola.text()
        
        kontrol = kalem.execute("SELECT * FROM kullanici WHERE kullaniciAdi = ?",(kAdi,))
        durum = kontrol.fetchall()
        if len(durum)<1:
            self.uyari.setText("Bu kullanici kayıtlı değil")
        else:
            if durum[0][2] != kParola:
                self.uyari.setText("Hatalı parola")
            else:
                self.uyari.setText(kAdi+" Giriş Başarılı")
                GirisEkrani.kullanici = kAdi
                QTest.qWait(500)        
                self.filtreler = FiltreEkrani() 
                self.filtreler.show() 
                self.close()                 

def main():
    uygulama = QApplication(sys.argv)
    dene = FiltreEkrani()
    dene.show()
    #pencere = GirisEkrani()
    sys.exit(uygulama.exec_())

if __name__ == '__main__':
    main()