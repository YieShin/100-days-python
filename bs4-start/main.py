from bs4 import BeautifulSoup
# import lxml  <<<<< try this if html.parser not working
import requests


response = requests.get("https://appbrewery.github.io/news.ycombinator.com/")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, features="html.parser")
articles = soup.find_all(name="a", class_="storylink")
article_texts = []
article_links = []
for article in articles:
    text = article.getText()
    article_texts.append(text)
    link = article.get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvotes)
index_of_largest = article_upvotes.index(largest_number)

print(article_texts[index_of_largest])
print(article_links[index_of_largest])
print(article_upvotes[index_of_largest])

# #find a single or first item in the webpage
# article_tag = soup.find(name="a", class_="storylink")
# article_text = article_tag.getText()
# article_link = article_tag.get("href")
# article_upvote = soup.find(name="span", class_="score").getText()
#
# print(article_text, "\n", article_link, "\n", article_upvote)


# with open("website.html") as file:
#     contents = file.read()
#
#
# soup = BeautifulSoup(contents, features="html.parser")
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
# print(soup.a)

# soup.find_all() is most used for most people
# all_anchor_tag = soup.find_all(name="a")
# print(all_anchor_tag)

# for tag in all_anchor_tag:
    # only get the anchor tag text
    # # print(tag.getText)
    # only get link
    # # print(tag.get("href"))

# # find item with "id"
# heading = soup.find(name="h1", id="name")
# print(heading)
#
# # find item with class
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading)

# The selector = "p a" is like in CSS which are paragraph and anchor tag. To find selected item in selected place
# company_url = soup.select_one(selector="p a")
# print(company_url)