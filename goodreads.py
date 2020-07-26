def find_genre_urls(): #get the url of 20 genres and store them in genre_urls list
    global genre_urls
    for url in soup.find_all("a", class_="categoriesList__categoryLink"):
        genre_urls.append("https://www.goodreads.com"+url['href'])

def find_genre_names(): #get the name of 20 genres and store them in genre_names

    global genre_names
    genres_scrapped = []

    for link in soup.select("li.categoriesList__category > a"):
        genres_scrapped+=link
    #we do some editing on text to get just the genre name 
    [genre_names.append(genres_scrapped[num].replace("\n","").replace(" ","-").replace("-&-","-").lower()) for num in range(0,100,5)]       

def get_author_bookname(): #get the author name and book name of 20 genres and store them in autor_book_name
    author_book_name = []
    
    for div in soups.find_all('a', class_="pollAnswer__bookLink"):
        for img in div.find_all('img', alt=True):
            author_book_name.append(img['alt'].split('by'))
        
    return author_book_name

def get_votes(): #get the votes of 20 genres and store them in list_of_ratings list
    list_of_ratings = []
    for ratings in soups.find_all("strong", class_="uitext result"):
        list_of_ratings+=(ratings)    
    return list_of_ratings       

def get_book_url(): #get the book url of all books in genre[i] and store it in book_url list
    book_url = []
    
    for div in soups.find_all('a', class_="pollAnswer__bookLink"):
        book_url.append("https://www.goodreads.com"+div['href'])
        
    return book_url

def get_book_details(url): #get the stars of all books in genre[i] and store it in stars_book
    global request3
    global soups3
    request3 = []
    soups3 = []

    #request url of book to get its rating
    request3 = requests.get(url)
    soups3 = bs4.BeautifulSoup(request3.text,"lxml")
    

    stars_book = []
    for ratings in soups3.find_all("span", itemprop="ratingValue"):
        stars_book+=(ratings)    
    return stars_book

    
def scrapwebsites(i):
    global request
    global soups
    global driver
    
    book_name = []
    author_name = []
    genre_list = []
    stars = []
    
    #request webpage of genre[i]
    request = requests.get(genre_urls[i])
    #get html of webpage of genre[i]
    soups = bs4.BeautifulSoup(request.text,"lxml")    
    

    author_book = get_author_bookname() #find top 20 names of all books and their authors in genre[i]
    
    book_name = [i[0] for i in author_book] #get book name from author_book list
    author_name = [i[1] for i in author_book] #get author name from author_book list
    
    votes = get_votes() #get number of votes received by each book in genre[i]

    book_url_list = get_book_url() #get urls of each book in genre[i]

    for index in range(0,20): #loop through 20 books in genre[i], collect their information, and store it in genre_list list
        stars = get_book_details(book_url_list[index].replace("\n","")) #we go to url of each book and scrap its rating or stars
        genre_list.append([genre_names[i].capitalize(),book_name[index],author_name[index],votes[index].replace("\n",""),book_url_list[index],stars])
        
    return genre_list


def main():

    find_genre_names() #function to scrape names of all genres

    find_genre_urls() #function to scrape url of all genres 

    One_Genre_list = []   
    All_Genre_List = []

    #traverse webpages of all genres
    for genre in range(0,20):
        #One_Genre_list contains information about 20 books awarded in a particular genre.
        One_Genre_list = scrapwebsites(genre)
        #Append information about books in each genre to one consolidated list
        for x in range(0,20):
            All_Genre_List.append([One_Genre_list[x][0],One_Genre_list[x][1],One_Genre_list[x][2],One_Genre_list[x][3],One_Genre_list[x][4],One_Genre_list[x][5]])
    #show data in form of table
    df = DataFrame (All_Genre_List,columns=['Genre','Book','Author','Votes','URL','Stars'])
    
    df.to_csv(r"D:\Project2.csv",index=False)

    print(df)

if __name__ == "__main__": 
    #Getting dependencies

    #import request to request access to webpage we want to scrap
    import requests

    #import bs4 ie BeautifulSoup to get to the elements in webpage
    import bs4

    #import dataframe to make table of the data collected
    from pandas import DataFrame

    #import selenium to login to goodreads
    #it comes in handy when we try to scrap webpage that throws the popup to login to goodreads
    #before we being to scrape goodreads, we will log-in so that a log-in popup doesn't spoil our game later.
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(PATH)

    driver.get("https://goodreads.com")

    #enter username, password, and click on the submit button to log-in
    driver.find_element_by_id("userSignInFormEmail").send_keys("xyz@gmail.com")
    driver.find_element_by_id("user_password").send_keys("Abc123")
    driver.find_element_by_class_name("gr-button").click()


    genre_names = [] #list of 20 genres
    genre_urls = [] #list of url of respective genres. we will use them to scrap books awarded in respective genre

    #make request to goodreads
    res = requests.get("https://www.goodreads.com/choiceawards/best-fiction-books-2019")

    #collect html in soup object
    soup = bs4.BeautifulSoup(res.text,"lxml")

    main()
