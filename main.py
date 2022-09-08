import requests 
import os
from tkinter import *
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
from PIL import Image

geolocator = Nominatim(user_agent="weather GUI")

def get_coords(city):
    address = geolocator.geocode(city)
    
    params = {
        "lat": address.latitude,
        "lon": address.longitude,
    }

    return params

def get_svg(svg_image, svg_name):
    try:
        drawing = svg2rlg(svg_image)
        # svg_bytes = BytesIO()
        png_name = svg_name.partition('.')[0]
        renderPM.drawToFile(svg_image, png_name, fmt='PNG')

        

    except Exception as ex:
        print(ex)
        print('Возникла ошибка')

def get_weather():

    #  -> Path to images
    cwd = os.getcwd() + r'/images'

    #  -> Получение название города
    city = name.get()

    #  -> Получение погоды города
    r = requests.get('http://yandex.ru/pogoda/?', params=get_coords(city))
    soup = bs(r.text, 'lxml')

    #  -> ПРОГНОЗ НА СЕГОДНЯ
    today_weather_temp = soup.select('div.fact__temp-wrap span.temp__value')
    today_weather_cond = soup.find('div', {'class': 'link__condition'})
    today_weather_props = soup.select('div.fact__props span.a11y-hidden')
    today_weather_image = soup.select('a.fact__basic_size_wide img.icon')

    #  -> Цикл обработки фотографии погоды сегодня
    for image in today_weather_image:
        image_map = image['src'][::-1]
        image_map_temp = cwd + '/' + image_map.partition('/')[0][::-1]

        print(f'File {image_map_temp} -- {os.path.exists(image_map_temp)}')

        if(os.path.exists(image_map_temp)):
            print(f'File {image_map_temp} is exists')
        else:
            p = requests.get(f"http:{image['src']}")
            out = open(f'{cwd}/{image_map_temp}', 'wb')
            out.write(p.content)
            out.close()
            print('File was created')
    

    #     svgfile = svg2rlg(item['src'])
    #     bytespng = BytesIO()
    #     # renderPM.drawToFile(svgfile, bytespng, fmt='PNG')

    #     img = Image.open(bytespng)


    props_ = ''
    print(f'Текущая температура {today_weather_temp[0].get_text()}')
    print(today_weather_cond.get_text())

    for item in today_weather_props:
        props_ += item.get_text() + '\n'
        print(item.get_text())

    middle_condition.config(text = f'Текущая температура {today_weather_temp[0].get_text()}\n{today_weather_cond.get_text()}', font=('Arial', 10), bg='silver', width=700)
    middle_props.config(text=props_, font=('Arial', 10), bg='silver', width=700)

    props_ = ''
    
    #  -> НЕДЕЛЬНЫЙ ПРОГНОЗ
    weekly_weather = soup.select('li.forecast-briefly__day a')
    weekly_weather_images = soup.select('a.forecast-briefly__day-link img.forecast-briefly__icon')

    image_temp_list = []

    for image in weekly_weather_images[1:6]:
        image_map = image['src'][::-1]
        image_map_temp = cwd + '/' + image_map.partition('/')[0][::-1]

        print(f'File {image_map_temp} -- {os.path.exists(image_map_temp)}')

        if(os.path.exists(image_map_temp) == False):
            p = requests.get(f"http:{image['src']}")
            out = open(f'{cwd}/{image_map_temp}', 'wb')
            out.write(p.content)
            out.close()
            print('File was created')
        else:
            print(f'File {image_map_temp} is exists')

    for item in weekly_weather[1:6]:
        Label(window, text = item["aria-label"].replace(",", "\n"), font=('Arial', 10), width=10).pack(side=LEFT)


window = Tk()
window.geometry('700x700')
window.title('Weather GUI')

    #  -> Фрейм ввода города
header_frame = Frame(window, height=100, width=700, bg='silver')
header_frame.pack(side=TOP)

    #  -> Фрейм вывода погоды сегодня
middle_frame = Frame(window)
middle_frame.pack(side=TOP)

    #  -> Фрейм вывода погоды неделя
bottom_frame = Frame(window)
bottom_frame.pack()

    #  -> Header Frame
header = Label(header_frame, text='Введите город: ', font=('Arial', 13), bg='silver', width=700)
header.pack(side=TOP)
name = Entry(header_frame, width=20)
name.pack(side=TOP, pady=5)    
btn = Button(header_frame, text='Enter', command=get_weather)
btn.pack(side=TOP, pady=5)

    #  -> Middle Frame
middle_condition = Label(middle_frame, text='', font=('Arial', 13))
middle_condition.pack(side=TOP)
middle_props = Label(middle_frame, text='', font=('Arial', 13))
middle_props.pack(side=TOP)

    #  -> Bottom Frame
bottom_condition1 = Label(middle_frame, text='', font=('Arial', 13))
bottom_condition2 = Label(middle_frame, text='', font=('Arial', 13))
bottom_condition3 = Label(middle_frame, text='', font=('Arial', 13))
bottom_condition4 = Label(middle_frame, text='', font=('Arial', 13))
bottom_condition5 = Label(middle_frame, text='', font=('Arial', 13))

bottom_condition1.pack()
bottom_condition2.pack()
bottom_condition3.pack()
bottom_condition4.pack()
bottom_condition5.pack()

window.mainloop()