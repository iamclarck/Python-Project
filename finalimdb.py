import time
from datetime import datetime as dt
from requests_html import HTMLSession, HTML
import csv
import urllib.request
import cv2
import os

import glob
all_images = glob.glob('*.jpg')

session = HTMLSession()


urls = ['https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth', 'https://www.imdb.com/movies-coming-soon/?ref_=inth_cs',
        'https://www.imdb.com/chart/top/?ref_=nv_mv_250', 'https://www.imdb.com/search/title/?genres=horror&start=1&explore=title_type.genres&ref_=adv_nxt']

csv_file = open('imdbScraped4.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['TITLE', 'RATING', 'RUNTIME', 'GENRE',
                     'SUMMARY', 'DIRECTOR', 'ACTORS'])


images1 = []


for i in urls:
    response = session.get(i)
    # for response in responses:
    source = response.html
   

    names = source.find('.nm-title-overview-widget-layout')
    for name in names:
        title = name.find('h4 a', first=True).text

        runTime = name.find('.cert-runtime-genre time', first=True).text
        genre = name.find('.cert-runtime-genre span', first=True).text

        try:
            rating = name.find('.rating_tx', first=True).text
        except Exception as identifier:
            rating = 'None'

        outline = name.find('.outline', first=True).text

        director = name.find('.txt-block span a', first=True).text

        stars = name.find('.txt-block a')

        # print("ACTORS")
        iter_stars = iter(stars)
        next(iter_stars)

        for star_name in iter_stars:
            print(star_name.text)
        print(type(iter_stars))
        csv_writer.writerow([title, rating, runTime, genre,
                     outline, director, star_name.text,])
        
    images = source.find('div.image a img')
    for image in images:
        images1.append(image.attrs['src'])

    for i in range(len(images1)):
        
        urllib.request.urlretrieve(images1[i], f'{i}.jpg')

csv_file.close()

face_cascade = cv2.CascadeClassifier(
    r'C:\Users\Deepak\Desktop\Miniproject1\classifier\haarcascade_frontalface_default.xml')

for i in range(0,26):
    image = cv2.imread(
        f'{i}.jpg', 1)

    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        grey_image, scaleFactor=1.02, minNeighbors=10)
    print(faces)
    for x, y, w, h in faces:
        image = cv2.rectangle(image, (x, y), (x+w, y+w), (0, 255, 0), 3)
        roi_color = image[y:y + h, x:x + w]
        print("[INFO] Object found. Saving locally.")
        cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)

    cv2.imshow('Grey image Window', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def hyperBlock(host_path,hosts,redirect):
    weblist = ['www.imdb.com', 'imdb.com']
    date1 = dt(dt.now().year, dt.now().month, dt.now().day, 23)
    date2 = dt(dt.now().year, dt.now().month, dt.now().day, 23, 20)
    while True:
        today = dt.now()  # today object is created

        if(date1 < today < date2):
            print('Working hours!', dt.now())
            with open(host_path, 'r+') as file:
                content = file.read()
                for website in weblist:
                    if(website in content):
                        pass
                    else:
                        file.write(redirect + ' ' + website + "\n")

        else:
            with open(host_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)  # start line from 0 index
                for line in content:
                    if not any(website in line for website in weblist):
                        file.write(line)
                file.truncate()  # it will keep latest content of file and delete privious content
            print("Fun Time", dt.now())

        time.sleep(1)
hyperBlock(r'C:\Windows\System32\drivers\etc\hosts',r'hosts', '127.0.0.1')
