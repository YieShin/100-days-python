from bs4 import BeautifulSoup
import requests

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
list_of_movies = [item.text for item in soup.find_all("h3", "title")]

file_name = "100-greatest-movies"
movies = list_of_movies[::-1]
with open(file_name, "w") as file:
    for movie in movies:
        file.write(str(movie) + "\n")