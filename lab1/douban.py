import requests
from bs4 import BeautifulSoup
import csv
import random
import os


def header_x():
    # 随机获取一个headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    ]

    headers = {"User-Agent": random.choice(user_agents)}
    return headers


def search_movie(movie_list, output_path):
    url = "https://movie.douban.com/subject/"
    headers = header_x()

    fp = open(
        os.path.join(output_path, "movie.csv"), mode="w", encoding="utf-8", newline=""
    )
    header = ["id", "基本信息", "剧情简介", "演职员表"]
    writer = csv.writer(fp)
    writer.writerow(header)

    print("movie.csv open!")
    for id in movie_list:
        print(id)
        res = requests.get(url + id, headers=headers)
        soup = BeautifulSoup(res.text, features="lxml")

        ## 基本信息
        try:
            info = soup.find("div", id="info").get_text().replace(" ", "")
        except:
            print("info not find")
            info = None

        ## 剧情简介
        try:
            intro = (
                soup.find("div", id="link-report-intra", class_="indent")
                .find("span", class_="all hidden")
                .get_text()
                .replace(" ", "")
            )
        except:
            try:
                intro = (
                    soup.find("div", id="link-report-intra", class_="indent")
                    .find("span", class_="", property="v:summary")
                    .get_text()
                    .replace(" ", "")
                )
            except:
                print("intro not find!")
                intro = None

        # 演职员表在另一个网页
        res = requests.get(url + id + "/celebrities", headers=headers)
        soup = BeautifulSoup(res.text, features="lxml")
        try:
            celebrities_list = soup.find_all("div", class_="info")
        except:
            print("celebrities not find")
            celebrities_list = None
        celebrities = ""
        for i in celebrities_list:
            celebrities = celebrities + i.get_text().replace(" ", "")

        p = [id, info, intro, celebrities]
        writer.writerow(p)

    fp.close()


def search_book(book_list, output_path):
    url = "https://book.douban.com/subject/"
    headers = header_x()

    fp = open(
        os.path.join(output_path, "book.csv"), mode="w", encoding="utf-8", newline=""
    )
    header = ["id", "基本信息", "内容简介", "作者简介"]
    writer = csv.writer(fp)
    writer.writerow(header)

    print("book.csv open!")
    for id in book_list:
        print(id)
        res = requests.get(url + id, headers=headers)
        soup = BeautifulSoup(res.text, features="lxml")

        ## 基本信息
        try:
            info = soup.find("div", id="info").get_text().replace(" ", "")
        except:
            print("info not find")
            info = None

        ## 内容简介
        try:
            intro_list = (
                soup.find("div", id="link-report", class_="indent")
                .find("span", class_="all hidden")
                .find("div", class_="intro")
                .find_all("p")
            )
            intro = ""
            for i in intro_list:
                intro += "  "
                intro += i.get_text()
                intro += "\n"
        except:
            try:
                intro = (
                    soup.find("div", id="link-report", class_="indent")
                    .find("div", class_="intro")
                    .get_text()
                )
            except:
                print("intro not find!")
                intro = None

        ## 作者简介
        try:
            related_info = soup.find("div", class_="related_info")
            authorintro_list = (
                related_info.find_all("div", class_="indent", limit=2)[1]
                .find("span", class_="all hidden")
                .find("div", class_="intro")
                .find_all("p")
            )
            authorintro = ""
            for i in authorintro_list:
                authorintro += "  "
                authorintro += i.get_text()
                authorintro += "\n"
        except:
            try:
                related_info = soup.find("div", class_="related_info")
                authorintro = (
                    related_info.find_all("div", class_="indent", limit=2)[1]
                    .find("div", class_="intro")
                    .get_text()
                )
            except:
                print("authorintro not find!")
                authorintro = None

        p = [id, info, intro, authorintro]
        writer.writerow(p)
    fp.close()


if __name__ == "__main__":
    pth = os.path.split(os.path.realpath(__file__))[0]
    data_pth = os.path.join(pth, "data")
    out_pth = os.path.join(pth, "output")
    fp_movie = open(os.path.join(data_pth, "Movie_id.txt"), mode="r", encoding="utf-8")
    movie_read = fp_movie.readlines()
    movie_list = [i.rstrip() for i in movie_read]
    fp_movie.close()
    search_movie(movie_list[0:5], out_pth)
    fp_book = open(os.path.join(data_pth, "Movie_id.txt"), mode="r", encoding="utf-8")
    book_read = fp_book.readlines()
    book_list = [i.rstrip() for i in book_read]
    fp_book.close()
    search_book(book_list[0:5], out_pth)
