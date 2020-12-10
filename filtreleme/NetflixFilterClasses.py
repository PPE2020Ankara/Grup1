class Kullanici:
    def __init__(self, kullaniciAdi, parola, adSoyad, dogumTarihi):
        self.kullaniciAdi = kullaniciAdi
        self.parola = parola
        self.adSoyad = adSoyad
        self.dogumTarihi = dogumTarihi

    def yasHesabla(self):
        from datetime import date
        return date.today().year - self.dogumTarihi

    def getAdSoyad(self):
        return self.adSoyad

    def setAdSoyad(self, adSoyad):
        self.adSoyad = adSoyad


class Filtre:
    def ratingListesiOlustur(self, yas):
        ratingList = ['TV-Y', 'G', 'TV-G']
        if 7 < yas <= 14:
            ratingList.extend(['TV-Y7-FV', 'TV-Y7', 'PG', 'TV-PG'])
        elif 14 < yas <= 17:
            ratingList.extend(['TV-Y7-FV', 'TV-Y7', 'PG', 'TV-PG', 'TV-14', 'PG-13'])
        elif 18 < yas:
            ratingList.extend(['NC-17', 'TV-MA', 'UR', 'TV-Y7-FV', 'TV-Y7', 'PG', 'TV-PG', 'TV-14', 'PG-13','NaN'])
        return ratingList

    def __init__(self, yas):
        self.country = None
        self.director = None
        self.durationMax = None
        self.durationMin = 0
        self.listed_in = None
        self.ratingList = self.ratingListesiOlustur(yas)


class IcerikListesi:
    def __init__(self, dosyaAdi):
        import pandas as pd
        self.df = pd.read_csv(dosyaAdi)
        self.df[['sure', 'min/season']] = self.df.duration.str.split(" ", expand=True)

    def filtreUygula(self, filtre):
        # self.ratingFiltrele(filtre.ratingList)
        self.countryFiltrele(filtre.country)
        self.directorFiltrele(filtre.director)
        self.durationFiltrele(filtre.durationMin, filtre.durationMax)
        self.listed_inFiltrele(filtre.listed_in)
        return self.df
    def ratingFiltrele(self,ratingList):
        self.df = self.df[self.df['rating'].isin(ratingList)]

    def listed_inFiltrele(self, listed_in):
        if listed_in != None:
            self.df = self.df[(self.df.listed_in.str.contains(listed_in)) | (self.df['listed_in'] == listed_in)]

    def directorFiltrele(self, director):
        if director != None:
            self.df['director']=self.df['director'].str.lower()
            self.df = self.df[(self.df.director.str.contains(director.lower())) | (self.df['director'] == director.lower())]
            self.df['director'] = self.df['director'].str.title()

    def countryFiltrele(self, country):
        if country != None:
            self.df = self.df[(self.df.country.str.contains(country)) | (self.df['country'] == country)]

    def durationFiltrele(self, durationMin, durationMax):
        if durationMax != None:
            self.df = self.df[(self.df['min/season'] == 'min') & (durationMin <= self.df['sure'].astype(int)) & (
                        durationMax >= self.df['sure'].astype(int))]

kullanici = Kullanici("kulAdi", "parola", "ilham", 2000)
icerikListesi = IcerikListesi('dataset/netflix_titles.csv')
filtre = Filtre(kullanici.yasHesabla())
filtre.durationMax = 100
filtre.durationMin = 80
filtre.country = "United States"
filtre.director = "steven"
icerikListesi = icerikListesi.filtreUygula(filtre)
print(icerikListesi[["title", "director", "rating"]])