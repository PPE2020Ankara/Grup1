import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTest import *
from PyQt5.QtCore import Qt
import sqlite3
import pandas as pd
import xlsxwriter

# csv dosyasını okuma ve nan değerleri unknown olarak değiştirme

df = pd.read_csv('netflix_titles.csv')
df = df.fillna(value= "unknown")

cevir = lambda x : x.replace("İ","i").replace("I","İ").lower()
df["yonetmen"] = df["director"].apply(cevir)

# formlarda kullanılan yazı fontları ve stilleri burada tanımlanıyor
tema = "dark"
icon = 'logo.png'

if tema == "dark":    
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
    btnSitil2 = "color :white;font-weight:bold;background-color :#4c4c4c"
    pencereSitil = "background-color :black"
elif tema == "light":
    baslikfont = QFont("Century Gothic",20)
    butonFont = QFont("Century Gothic",14)
    yaziFont = QFont("Century Gothic",14)
    formYaziFont = QFont("Century Gothic",12)
    uyariFont = QFont("Century Gothic",14,)
    yaziSitil = "color :black"
    yaziSitilB = "color :black;font-weight:bold;"
    baslikSitil = "color :red;font-weight:bold;"
    uyariSitil = "color :red"
    editSitil = "color :black;background-color :white"
    btnSitil = "color :black;background-color :gray"
    btnSitil2 = "color :black;background-color :gray"    
    pencereSitil = "background-color :white"
    

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
        self.setWindowIcon(QIcon(icon))

# yeni kullanıcı formundan gelen bilgilerin veritabanına eklenmesi icin tanımlanan fonksiyon

    def yeniEkle(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        
        adSoyad = self.adSoyad.text()
        kAdi = self.kAdi.text()
        kParola = self.kParola.text()        
        dTarihi = self.dTarihi.text()
        
        baglanti = sqlite3.connect("vt.db")
        kalem = baglanti.cursor()
                   
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
        baglanti.close()          
 
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
        
        baglanti = sqlite3.connect("vt.db")
        kalem = baglanti.cursor()
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
        self.setWindowIcon(QIcon(icon))
        baglanti.close()

# güncelleme formundan gelen bilgilerin veritabanına yazılması için kullanılan fonksiyon

    def guncelle(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        
        adSoyad = self.adSoyad.text() 
        kAdi = self.kAdi.text()       
        kParola = self.kParola.text()        
        dTarihi = self.dTarihi.text()
        
        baglanti = sqlite3.connect("vt.db")
        kalem = baglanti.cursor()
                   
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
        baglanti.close()        
 
    def geriDon(self):
        self.close()   # Formu kapatmak için kullanılacak

# filitre ekranı formu

class FiltreEkrani(QWidget):
    filmAdi = ""
    dosyayaYaz = []
    listeleme = False
    def __init__(self):
        super().__init__()        

        pencereBaslik = "Netflix Filtreleme"        
        yatay0 = QHBoxLayout()
        dikey1 = QVBoxLayout()
        dikey2 = QVBoxLayout()
        yatayBtn = QHBoxLayout()
        yatayBosluk = QHBoxLayout()
        sureEtiket = QHBoxLayout() 
        sureSlider = QHBoxLayout()
        sureRadio = QHBoxLayout() 
        yatayRating = QHBoxLayout()
        yatayListele = QHBoxLayout()
        yatayBaslik = QHBoxLayout()
        yatayLogo = QHBoxLayout()       
        
        
        logo = QLabel("FİLTRE EKRANI")
        logo.setFixedHeight(100)
        logo.setFixedWidth(250)
        logo.setPixmap(QPixmap("logoF.png"))
        
        yatayLogo.addStretch()
        yatayLogo.addWidget(logo)
        yatayLogo.addStretch()
        
        baslik = QLabel("Netflix Filtreleme")
        baslik.setFixedHeight(100)
        baslik.setStyleSheet(baslikSitil)
        baslik.setFont(baslikfont) 
        
        yatayBaslik.addStretch()
        yatayBaslik.addWidget(baslik)
        yatayBaslik.addStretch()     
        
        turL = QLabel("Tür")
        turL.setFixedHeight(45)        
        turL.setStyleSheet(yaziSitilB)
        turL.setFont(yaziFont)
        
        turler = self.bilgiAl(df["listed_in"])   # bilgiAl fonksiyonu csv den türleri verir
        
        self.tur = QComboBox()
        self.tur.setStyleSheet(editSitil)
        self.tur.setFont(yaziFont)
        self.tur.addItem("Seçiniz")
        self.tur.addItems(turler)
        
               
        ulkeL = QLabel("Ülke")
        ulkeL.setFixedHeight(45)
        ulkeL.setStyleSheet(yaziSitilB)
        ulkeL.setFont(yaziFont)
        
        ulkeler = self.bilgiAl(df["country"])
        ulkeler[0] = "Seçiniz" # bilgiAl fonksiyonu csv den ülkeleri verir 
        
        self.ulke = QComboBox()
        self.ulke.setStyleSheet(editSitil)
        self.ulke.setFont(yaziFont)
        self.ulke.addItems(ulkeler)
        
        yonetmenL = QLabel("Yönetmen")
        yonetmenL.setFixedHeight(45)          
        yonetmenL.setStyleSheet(yaziSitilB)
        yonetmenL.setFont(yaziFont)
        
        self.yonetmen = QLineEdit()
        self.yonetmen.setPlaceholderText("Yönetmen giriniz")        
        self.yonetmen.setStyleSheet(editSitil)
        self.yonetmen.setFont(yaziFont) 
        
        sureL = QLabel("Süre") 
        sureL.setFixedHeight(45)          
        sureL.setStyleSheet(yaziSitilB)
        sureL.setFont(yaziFont)
        
        self.sureYok=QRadioButton("Süre Yok")
        self.sureYok.setChecked(True)
        self.sureYok.setStyleSheet(yaziSitil)
        self.sureYok.setFont(yaziFont)       
        self.sureYok.toggled.connect(self.sYok)
        
        self.dk=QRadioButton("Dakika")
        self.dk.setChecked(False)
        self.dk.setStyleSheet(yaziSitil)
        self.dk.setFont(yaziFont)       
        self.dk.toggled.connect(self.dkSecildi)
 
        self.sezon=QRadioButton("Sezon")
        self.sezon.setChecked(False)
        self.sezon.setStyleSheet(yaziSitil)
        self.sezon.setFont(yaziFont)        
        self.sezon.toggled.connect(self.sezonSecildi)
        
        sureRadio.addWidget(self.sureYok)
        sureRadio.addWidget(self.dk)
        sureRadio.addWidget(self.sezon)
                        
        self.sureL1 = QLabel("")        
        self.sureL1.setStyleSheet(yaziSitil)
        self.sureL1.setFont(yaziFont)
        
        self.sureL2 = QLabel("")        
        self.sureL2.setStyleSheet(yaziSitil)
        self.sureL2.setFont(yaziFont)
        
        sureEtiket.addWidget(self.sureL1)
        sureEtiket.addWidget(self.sureL2)
        
        self.sure1 = QSlider(Qt.Horizontal,self)
        self.sure1.setEnabled(False)
        self.sure1.setRange(0, 200)
        self.sure1.setFocusPolicy(Qt.NoFocus)       
        self.sure1.setTickInterval (5)
        self.sure1.setTickPosition (QSlider.TicksBothSides)        
        self.sure1.setStyleSheet(editSitil)
        self.sure1.setFont(yaziFont)
        self.sure1.valueChanged[int].connect(self.sureAl1) 
        
        self.sure2 = QSlider(Qt.Horizontal,self)
        self.sure2.setEnabled(False)
        self.sure2.setRange(0, 200)
        self.sure2.setFocusPolicy(Qt.NoFocus)
        self.sure2.setValue(0)      
        self.sure2.setTickInterval (5)
        self.sure2.setTickPosition (QSlider.TicksBothSides)        
        self.sure2.setStyleSheet(editSitil)
        self.sure2.setFont(yaziFont)
        self.sure2.valueChanged[int].connect(self.sureAl2) 
        
        sureSlider.addWidget(self.sure1)
        sureSlider.addWidget(self.sure2)
      
        ratings = self.bilgiAl(df["rating"])   
        
        self.rating = QComboBox()
        self.rating.setStyleSheet(editSitil)
        self.rating.setFont(yaziFont)
        self.rating.addItem("Seçiniz")
        self.rating.addItems(ratings)
                      
        guncelle = QPushButton("Bilgilerimi Güncelle",font=butonFont)
        guncelle.setFixedWidth(250)
        guncelle.setStyleSheet(btnSitil)       
        guncelle.clicked.connect(self.guncellemeFormu)
        
        listeleBnt = QPushButton("Listele",font=butonFont)
        listeleBnt.setFixedWidth(100)
        listeleBnt.setStyleSheet(btnSitil)       
        listeleBnt.clicked.connect(self.listele)
        
        yatayListele.addStretch()
        yatayListele.addWidget(listeleBnt)
        
        ratingBnt = QPushButton("Derecelendirme",font=butonFont)
        ratingBnt.setFixedWidth(225)
        ratingBnt.setStyleSheet(btnSitil2)       
        ratingBnt.clicked.connect(self.derecelendirmeBilgileri) 
        
        indirBtn = QPushButton("Dosyayı İndir",font=butonFont)
        indirBtn.setFixedWidth(170)
        indirBtn.setStyleSheet(btnSitil)               
        indirBtn.clicked.connect(self.dosyaIndir)
        
        cikisBtn = QPushButton("Çıkış",font=butonFont)
        cikisBtn.setFixedWidth(170)
        cikisBtn.setStyleSheet(btnSitil)       
        cikisBtn.clicked.connect(self.cikis)
        
        
        hakkimizdaBtn = QPushButton("Hakkımızda",font=butonFont)
        hakkimizdaBtn.setFixedWidth(170)
        hakkimizdaBtn.setStyleSheet(btnSitil)       
        hakkimizdaBtn.clicked.connect(self.hakkimizda)
        
        yatayRating.addWidget(ratingBnt)
        yatayRating.addWidget(self.rating)
        
        self.uyariLabel = QLabel("")
        self.uyariLabel.setFixedHeight(100)
        self.uyariLabel.setStyleSheet(uyariSitil)
        self.uyariLabel.setFont(uyariFont)  
               
        sonuc = df["title"].sort_values()
        #print(len(sonuc))
        
        self.sonuclar = QListWidget()
        self.sonuclar.setFixedWidth(600)
        self.sonuclar.setFixedHeight(500)
        self.sonuclar.addItems(sonuc)
        self.sonuclar.setStyleSheet(editSitil)
        self.sonuclar.setFont(yaziFont) 
        self.sonuclar.itemClicked.connect(self.filmBilgileri)
        
        
        dikey1.addStretch()
        dikey1.addLayout(yatayLogo)        
        dikey1.addWidget(turL)
        dikey1.addWidget(self.tur)
        dikey1.addWidget(ulkeL)
        dikey1.addWidget(self.ulke)
        dikey1.addWidget(yonetmenL)
        dikey1.addWidget(self.yonetmen)
        dikey1.addWidget(QLabel(""))
        dikey1.addLayout(yatayRating)
        dikey1.addWidget(sureL) 
        dikey1.addLayout(sureRadio)        
        dikey1.addLayout(sureEtiket)
        dikey1.addLayout(sureSlider)               
        dikey1.addLayout(yatayListele)
        dikey1.addWidget(self.uyariLabel)        
        
        yatayBtn.addStretch()
        yatayBtn.addWidget(guncelle)
        yatayBtn.addWidget(indirBtn)
        yatayBtn.addWidget(hakkimizdaBtn)
        
        yatayBosluk.addStretch()
        yatayBosluk.addWidget(cikisBtn)
                
        dikey2.addLayout(yatayBaslik)
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
        self.setWindowIcon(QIcon(icon))
    
    def dkSecildi(self):
        self.sure1.setRange(0, 200)
        self.sure2.setRange(0, 200)
        self.sure1.setValue(0) 
        self.sure2.setValue(0)
        self.sure1.setEnabled(True)
        self.sure2.setEnabled(True)
        self.sureL1.setText(str(self.sure1.value()) + " dk")
        self.sureL2.setText(str(self.sure2.value()) + " dk")
    
    def sezonSecildi(self):
        self.sure1.setRange(0, 20)
        self.sure2.setRange(0, 20)
        self.sure1.setValue(0)
        self.sure2.setValue(0)
        self.sure1.setEnabled(True)
        self.sure2.setEnabled(True)  
        self.sureL1.setText(str(self.sure1.value()) + " sezon")
        self.sureL2.setText(str(self.sure2.value()) + " sezon")
    
    def sYok(self):        
        self.sure1.setValue(0) 
        self.sure2.setValue(0)
        self.sure1.setEnabled(False)
        self.sure2.setEnabled(False)
    
    def sureAl1(self,value):
        if self.dk.isChecked():            
            self.sureL1.setText(str(value) + " dk")
        else:
            self.sureL1.setText(str(value) + " sezon")
    
    def sureAl2(self,value):
        if self.dk.isChecked():
            self.sureL2.setText(str(value) + " dk")
        else:
            self.sureL2.setText(str(value) + " sezon")
    
    # güncelle butonu ile güncelleme formunun açılması için kullanılan fonksiyon
    def guncellemeFormu(self):
        self.gFormu = KayitGuncelle()   # kayıt güncelleme formunu açar
        self.gFormu.show()
    
    def hakkimizda(self):
        self.hakkimizda = HakkimizdaForm()   # kayıt güncelleme formunu açar
        self.hakkimizda.show()
    
    def filmBilgileri(self,item):
        FiltreEkrani.filmAdi = item.text()        
        self.filmBilgi = FilmBilgileri()   # kayıt güncelleme formunu açar
        self.filmBilgi.show()
        
    def derecelendirmeBilgileri(self,item):               
        self.bilgi = DerecelendirmeBilgileri()   # kayıt güncelleme formunu açar
        self.bilgi.show()
    
    # filtreler seçildikten sonra listeleme sonuçlarının gösterilmesi    
    def listele(self):
        tur = self.tur.currentText()
        ulke = self.ulke.currentText()
        yonetmen = self.yonetmen.text().strip()
        rating = self.rating.currentText()
        sure1 = self.sure1.value()
        sure2 = self.sure2.value()
        
        yonetmen = yonetmen.replace("İ","i").replace("I","ı").lower()
             
        print(yonetmen) 
        result = df              
        
        if tur != "Seçiniz":            
            result = result[(result.listed_in.str.contains(tur)) | (result['listed_in']==tur)]
            
        if ulke != "Seçiniz":
            result = result[(result.country.str.contains(ulke)) | (result['country']==ulke)]
            
        if yonetmen != "":
            result = result[(result.yonetmen.str.contains(yonetmen)) | (result['yonetmen']==yonetmen)]
        
        if rating != "Seçiniz":
            result = result[result['rating']==rating]
             
        if self.dk.isChecked() or self.sezon.isChecked():
            if sure1>sure2:
                sureMax = sure1
                sureMin = sure2
            else:
                sureMax = sure2
                sureMin = sure1
            
            if self.dk.isChecked():
                sureler = [str(sure)+" min" for sure in range(sureMin,sureMax+1)]
            else:
                sureler = [str(sure)+" Seasons" for sure in range(sureMin,sureMax+1)]           
             
            result = result[(result['duration'].isin(sureler))]  # .isin metotu liste içerisinde olup olmadığını karşılaştırır
        FiltreEkrani.dosyayaYaz = result
        FiltreEkrani.listeleme = True
                         
        #print(len(result))
        self.uyariLabel.setText(str(len(result)) + " Sonuç listelendi")    
        self.sonuclar.clear()
        self.sonuclar.addItems(result["title"].sort_values())
    
    # dosya indirme işlemlerinin yapıldığı fonksiyon
    def dosyaIndir(self):
        if FiltreEkrani.listeleme:
            dosya = self.dosya_dialog() # dosya dialog kutusunu aç            
            if isinstance(dosya, list): # gelen değer liste mi?
                kalem = pd.ExcelWriter(dosya[0]+".xlsx", engine="xlsxwriter")
                FiltreEkrani.dosyayaYaz.to_excel(kalem, sheet_name="Filmler")   
                kalem.save()
                self.uyariLabel.setText("Dosya kaydedildi")
                QTest.qWait(2000)
                self.uyariLabel.setText("")   
            else:
                self.uyariLabel.setText("İşlemi iptal ettiniz.")
                QTest.qWait(2000)
                self.uyariLabel.setText("")                    
        else:
            self.uyariLabel.setText(" Önce listeleme yapmalısınız.")
            QTest.qWait(2000)
            self.uyariLabel.setText("")        
  
    def dosya_dialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode (QFileDialog.AcceptSave)             
        if dlg.exec_():
            dosyaAdi = dlg.selectedFiles()
            return dosyaAdi
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

# Film bilgi ekranı
class FilmBilgileri(QWidget):
    def __init__(self):
        super().__init__()  
                
        pencereBaslik = "Film Bilgisi"
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()        
        
        filmAdi = FiltreEkrani.filmAdi          
        result = df[df['title']==filmAdi]        
        
        filmBilgileri = QTextEdit()
        filmBilgileri.setFixedWidth(675)
        filmBilgileri.setFixedHeight(550)
        filmBilgileri.setStyleSheet(yaziSitil)
        filmBilgileri.setReadOnly(True)        
        filmBilgileri.setHtml(f"""<font size='6'>
                              <p align="center" style="color:red;"><b>{filmAdi}</b></p>
                              <p><b>Yönetmen :</b> {result.director.values[0]}</p>
                              <p><b>Oyuncular :</b> {result.cast.values[0]}</p>
                              <p><b>Ülke :</b> {result.country.values[0]}</p>
                              <p><b>Yapım Yılı :</b> {result.release_year.values[0]}</p>
                              <p><b>Süre :</b> {result.duration.values[0]}</p>
                              <p><b>Kategori :</b> {result.listed_in.values[0]}</p>
                              <p><b>Açıklamalar :</b> {result.description.values[0]}</p>
                              <p><b>Derecelendirme :</b> {result.rating.values[0]}</p>
                              </font>""")    
        dikey.addWidget(filmBilgileri)
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setGeometry(300,300,700,600)
        self.setFixedSize(700, 600)
        self.setStyleSheet(pencereSitil)
        self.setWindowTitle(pencereBaslik)
        self.setWindowIcon(QIcon(icon))

# derecelendirme bilgilri açıklama ekranı
class DerecelendirmeBilgileri(QWidget):
    def __init__(self):
        super().__init__()  
                
        pencereBaslik = "Derecelendirme Bilgileri"
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()     
        
        bilgiler = QTextEdit()
        bilgiler.setFixedWidth(675)
        bilgiler.setFixedHeight(550)
        bilgiler.setStyleSheet(yaziSitil)
        bilgiler.setReadOnly(True)        
        bilgiler.setHtml(f"""<font size='5'>
                            <p align="center" style="color:red;"><b>Derecelendirme Bilgileri</b></p>
                            <p><b>G  :</b> Her yaştan izleyicinin izlemesinde sakınca olmayan filmler.</p>
                            <p><b>NC-17 :</b> 17 yaş altı çocuklar için uygun olmayan filmler. Film tamamen yetişkinlere yöneliktir. </p>
                            <p><b>NR  :</b> Henüz derecelendirilmemiş filmler.</p>
                            <p><b>PG :</b> Ebeveynlerin rehberliği tavsiye edilir. İçerik çocuklar için uygun olmayabilir.</p>
                            <p><b>PG-13 :</b> 13 yaş altı çocuklar için uygun olmayan filmler.</p>
                            <p><b>R :</b> 17 yaşın altı için bir ebeveynin refakati gereklidir.</p>
                            <p><b>TV-14 :</b> Bu program 14 yaşın altındaki çocuklar için uygun olmayabilir.  </p>
                            <p><b>TV-G :</b> Bu program her yaş için uygundur. </p>
                            <p><b>TV-MA :</b> Bu program, yetişkin ve yetişkin izleyiciler tarafından görülmek üzere tasarlanmıştır ve 17 yaşın altındaki çocuklar için uygun olmayabilir.</p>
                            <p><b>TV-PG :</b> Bu program, ebeveynlerin küçük çocuklar için uygun bulmayabileceği materyaller içermektedir. Ebeveyn rehberliği önerilir.  </p>
                            <p><b>TV-Y:</b> Bu program, 2-6 yaş arası çocuklar da dahil olmak üzere çok genç bir kitleye yöneliktir. </p>
                            <p><b>TV-Y7 :</b> Bu program en çok 7 yaş ve üstü çocuklar için uygundur. </p>
                            <p><b>TV-Y7-FV :</b> Bu program en çok 7 yaş ve üstü çocuklar için uygundur.  Fantezi şiddet TV-Y7 derecelendirmesine özel </p>
                            </font>""")    
        dikey.addWidget(bilgiler)
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setGeometry(300,300,700,600)
        self.setFixedSize(700, 600)
        self.setStyleSheet(pencereSitil)
        self.setWindowTitle(pencereBaslik)
        self.setWindowIcon(QIcon(icon))

class HakkimizdaForm(QWidget):
    def __init__(self):
        super().__init__()  
                
        pencereBaslik = "Program Hakkında"
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()     
        
        bilgiler = QTextEdit()
        bilgiler.setFixedWidth(675)
        bilgiler.setFixedHeight(550)
        bilgiler.setStyleSheet(yaziSitil)
        bilgiler.setReadOnly(True)        
        bilgiler.setHtml(f"""<font size='5'>
                            <p align="center" style="color:red;"><b>Program Hakkında</b></p>
                            
                            </font>""")    
        dikey.addWidget(bilgiler)
        
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.setGeometry(300,300,700,600)
        self.setFixedSize(700, 600)
        self.setStyleSheet(pencereSitil)
        self.setWindowTitle(pencereBaslik)
        self.setWindowIcon(QIcon(icon))
    
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
        self.setWindowIcon(QIcon(icon))        
        self.show()
        
        # veritabanında kullanıcı yoksa kullanıcı kayıt formunu aç
        baglanti = sqlite3.connect("vt.db")
        kalem = baglanti.cursor()
        kontrol = kalem.execute("SELECT * FROM kullanici")
        kBilgileri = kontrol.fetchall()
        if len(kBilgileri) < 1:
            self.kayitFormu()
        baglanti.close()

    def kayitFormu(self):
        self.kFormu = KayitFormu()   # kayıt formunu açar
        self.kFormu.show()
    
    def girisKontrol(self):
        self.uyari.setText("Kontrol ediliyor. Lütfen bekleyin...")
        QTest.qWait(750)
        kAdi = self.kAdi.text()
        kParola = self.kParola.text()
        
        baglanti = sqlite3.connect("vt.db")
        kalem = baglanti.cursor()
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
        baglanti.close()                

def main():
    uygulama = QApplication(sys.argv)
    #dene = FiltreEkrani()
    #dene.show()
    pencere = GirisEkrani()
    sys.exit(uygulama.exec_())

if __name__ == '__main__':
    main()