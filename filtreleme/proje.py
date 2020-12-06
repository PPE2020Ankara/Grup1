import pandas as pd
df = pd.read_csv('dataset/netflix_titles.csv')
result = df.columns
# result=df.info
country='United States'
# country='India'
#director = 'Steven Spielberg'
director='Nathanael Wiseman'
duration = '90 min'
# Burada sliderden durationa gelen integer değeri önce stringe çevirip, sonra stringin sonuna " min" eklenecek.
listed_in = 'Comedies'
rating = 'TV-PG'
# Gelen yaş değerine göre uygun olan ratingler listelenecek.
result = df[(df.country.str.contains(country)) | (df['country']==country)][['title','country']] # Ülke adına göre sadece film adı ve ülke adı filtreleme
#result = df[(df.country.str.contains(country)) | (df['country']==country)] # Ülke adına göre filtreleme tüm kolonlar
result = df[(df.director.str.contains(director)) | (df['director']==director)][['title','director']] # Yönetmen adına göre film adı ve yönetmen adı filtreleme
result= df[(df.duration.str.contains(duration)) | (df['director']==duration)][['title','duration']] # İçerik süresine göre film adı ve süre filtreleme
#result = df[(df.listed_in.str.contains(listed_in)) | (df['listed_in']==listed_in)][['title','listed_in']] # İçerik türüne göre film adı ve içerik türü filtreleme
# result=df[df['rating']==rating]  # İzleyici yaşına göre filtreleme
#print(result.head(20))
print(result)