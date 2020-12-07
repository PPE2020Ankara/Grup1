import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTest import *
import sqlite3

baslikfont = QFont("Century Gothic",20)
butonFont = QFont("Century Gothic",14)
yaziFont = QFont("Century Gothic",14)
formYaziFont = QFont("Century Gothic",12)
uyariFont = QFont("Century Gothic",14,)
yaziSitil = "color :white"
baslikSitil = "color :red"
uyariSitil = "color :red"
editSitil = "color :black;background-color :white"
btnSitil = "color :black;background-color :gray"
pencereSitil = "background-color :black"

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
 
    def geriDon(self):
        self.close()   # Formu kapatmak için kullanılacak

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

class FiltreEkrani(QWidget):
    def __init__(self):
        super().__init__()        

        pencereBaslik = "Filtre Ekranı"        
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()        
        

        baslik = QLabel("FİLTRE EKRANI")
        baslik.setStyleSheet(yaziSitil)
        baslik.setFont(baslikfont)
        
        aciklama1 = QLabel("Merhaba " + GirisEkrani.kullanici)
        aciklama1.setStyleSheet(yaziSitil)
        aciklama1.setFont(baslikfont)
        
        aciklama = QLabel("Filtrelemeler bu ekranda yapılacak")
        aciklama.setStyleSheet(yaziSitil)
        
        guncelle = QPushButton("Bilgilerimi Güncelle",font=butonFont)
        guncelle.setFixedWidth(350)
        guncelle.setStyleSheet(btnSitil)       
        guncelle.clicked.connect(self.guncellemeFormu)
        
               
        dikey.addStretch()
        dikey.addWidget(baslik)
        dikey.addWidget(aciklama1)
        dikey.addWidget(aciklama)
        dikey.addWidget(guncelle)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setGeometry(200,200,1024,768)
        self.setWindowTitle(pencereBaslik)
        self.setStyleSheet(pencereSitil)
    
    def guncellemeFormu(self):
        self.gFormu = KayitGuncelle()   # kayıt güncelleme formunu açar
        self.gFormu.show()  

    def geriDon(self):
        self.close()   # Formu kapatmak için kullanılacak


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

        #self.showFullScreen()
        #self.setGeometry(300, 300, 800, 600)
        #self.resize(800,600)
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
    pencere = GirisEkrani()
    sys.exit(uygulama.exec_())

if __name__ == '__main__':
    main()