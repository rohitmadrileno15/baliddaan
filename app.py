from flask import Flask,request,render_template
from time import sleep
import time
import re,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired, ValidationError


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
url = "https://www.honourpoint.in"
driver.get(url)


app = Flask(__name__)
app.config['SECRET_KEY'] = '450933c08c5ab75e79619102eddf47dee813a9d6'



class SearchForm(FlaskForm):
    name = StringField('Name' , validators = [DataRequired()])

    submit = SubmitField('Search')


@app.route('/')
def hello_world():
    flag= True
    m=23
    i=0
    while(flag):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #scrolling down

        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/div/div[7]/div/div/div/div/div/div/div/a").click()
        i+=1
        if(i>m):
            flag=False
    time.sleep(10)

    posts= driver.find_elements_by_class_name("hp-profile-item")
    print("Ready")
    print(i)


    arr=[]


    for post in posts:
        arr.append({"name" : post.find_element_by_class_name("hp-profile-title").text , "year" : post.find_element_by_class_name("hp-profile-publish-date").text , "image" : post.find_element_by_class_name("hp-profile-image").find_element_by_tag_name("img").get_attribute("src")})


    n = "Search feature coming soon!"

    return render_template('index.html', posts = arr ,alert=n)



@app.route('/search' , methods=['GET', 'POST'])
def search():
    n= None
    find_ = None

    form = SearchForm()
    if (form.validate_on_submit() ):
        name = form.name.data
        iter = name.strip()

        n=None
        flag= True
        m=23
        i=0

        while(flag):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            #scrolling down

            driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/div/div[7]/div/div/div/div/div/div/div/a").click()
            i+=1
            if(i>m):
                flag=False
        time.sleep(10)

        posts= driver.find_elements_by_class_name("hp-profile-item")
        print("Ready")
        print(i)


        arr=[]


        for post in posts:
            arr.append({"name" : post.find_element_by_class_name("hp-profile-title").text , "year" : post.find_element_by_class_name("hp-profile-publish-date").text , "image" : post.find_element_by_class_name("hp-profile-image").find_element_by_tag_name("img").get_attribute("src")})




        find_ = [(item for item in arr if re.search(iter, item["name"]))]
        if(find_ ):
            print("Found")

        count = 0

        for i,objs in enumerate(find_):
            if(objs):
                count +=1

        if(not (count > 0)):
            n="No such record found! Please try again"

    return render_template('search.html',form = form, posts = find_, alert=n)



if __name__ == '__main__':
    app.run(debug= True)
