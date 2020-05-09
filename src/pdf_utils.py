from fpdf import FPDF
import fpdf
import pandas as pd 
import requests




URL = "http://image.tmdb.org/t/p/w200/"


fpdf.set_global('SYSTEM_TTFONTS', "Fonts")

def get_fpdf():
    pdf = FPDF()
    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname="NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname="NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname="NotoSans-BoldItalic.ttf", uni=True)
    return pdf


def create_pdf(oscars):
    count_cell = 0
    x_image= 15
    y_image = 14
    H_IMAGE = 51
    H_CELL = 60
    pdf = get_fpdf()
    pdf.add_page()
    pdf.set_font('NotoSans', 'B', 12)
    for i,_ in enumerate(list(oscars.film)):
        im = get_image(URL + oscars.Poster[i], i)
        if i == 0:
            cell_film(pdf, im, x_image, y_image + H_CELL*count_cell, H_IMAGE, oscars.film[i], oscars.Description[i], oscars.Rate[i], oscars.win[i], oscars.name[i], oscars.category[i])
        else:
            cell_film(pdf, im, x_image, y_image + (H_CELL+5)*count_cell, H_IMAGE, oscars.film[i], oscars.Description[i], oscars.Rate[i], oscars.win[i], oscars.name[i], oscars.category[i])
        count_cell += 1
        if count_cell == 4:
            count_cell = 0
            pdf.add_page()
    pdf.output("archivo.pdf",'F')




def cell_film(pdf=None, image="", x_image=15, y_image=15 ,h_image=51, title="",description="", rate="", win=False, name="", category=""):
    if win:
        pdf.set_fill_color(153,153,0)
    else:
        pdf.set_fill_color(204,229,255)
    pdf.cell(190, 60, "", 1, 1, 'C', True)
    
    if pdf == None:
        pdf = get_fpdf()
    if image == "":
        image = "img/not_found.jpg"

    pdf.image(image, x_image, y_image, h=h_image, type="jpg")
    #name - category
    na_ca = resize_text(('NotoSans', 'B', 12),f"{name} - {category}",190)
    pdf.set_text_color(0)
    pdf.text(x_center_text(('NotoSans', 'B', 12), na_ca, 190), y_image, na_ca)
    pdf.set_text_color(50)
    #title
    pdf.text(x_image + 60, y_image+6, f"Titulo: {title}")
    #rate
    pdf.text(x_image + 60 , y_image+12, f"Puntuación: {rate}")
    #description
    text = split_text(['NotoSans', 'B', 12],description,115)
    y = y_image+18
    for i,e in enumerate(text):
        if i < 7:
            pdf.text(x_image + 60, y, e)
            y += 5
        else:
            pdf.text(x_image + 60, y, e[:-3]+"...")
            break
    pdf.cell(190, 5, "", 0, 1, 'C')
    



def split_text(font, text, width):
    ver = get_fpdf()
    index = 0
    temp = ""
    result = []
    ver.set_font(font[0], font[1], font[2])
    if ver.get_string_width(text) > width:
        while index < len(text):
            index += 1
            temp = text[:index]
            if ver.get_string_width(temp) >= width:
                result.append(temp)
                text = text[index:]
                index = 0
    else:
        result.append(text)
    return result

def x_center_text(font, text, width):
    ver = get_fpdf()
    h_image = 51
    ver.set_font(font[0], font[1], font[2])
    return 10 + (width - ver.get_string_width(text) + h_image)/2

def resize_text(font, text, width):
    ver = get_fpdf()
    ver.set_font(font[0], font[1], font[2])
    if ver.get_string_width(text) > width:
        while ver.get_string_width(text) >= width:
            text = text[:-1]
        text = text[:-7] + "..."
    return text



def get_image(url, i):
    image_request = requests.get(url)
    if image_request.status_code == 200:
        with open(f"img/image{i}.jpg", 'wb') as f:
            f.write(image_request.content)
            return f"img/image{i}.jpg"
    return ""