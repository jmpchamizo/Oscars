from fpdf import FPDF 
import pandas as pd 

def create_pdf(oscars):
    x_image= 15
    y_image = 14
    H_IMAGE = 51
    H_CELL = 60
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    for i,_ in enumerate(list(oscars.film)):
        cell_film(pdf, "", x_image, y_image + H_CELL*i, H_IMAGE, oscars.film[i], oscars.Description[i], oscars.Rate[i], oscars.win[i], oscars.name[i], oscars.category[i])
    pdf.output("archivo.pdf",'F')




def cell_film(pdf=None, image="", x_image=15, y_image=15 ,h_image=51, title="",description="", rate="", win=False, name="", category=""):
    URL = "http://image.tmdb.org/t/p/w300/"

    if win:
        pdf.set_fill_color(153,153,0)
    else:
        pdf.set_fill_color(204,229,255)
    pdf.cell(190, 60, "", 1, 1, 'C', True)
    
    if pdf == None:
        pdf = FPDF('P','mm','A4')
    if image == "":
        image = "img/not_found.jpg"
    else:
        image = URL + image
    pdf.image(image, x_image, y_image, h=h_image, type="jpg")
    #name - category
    na_ca = resize_text(('Arial', 'B', 12),f"{name} - {category}",190)
    pdf.set_text_color(0)
    pdf.text(x_center_text(('Arial', 'B', 12), na_ca, 190), y_image-1, na_ca)
    pdf.set_text_color(50)
    #title
    pdf.text(x_image + 60, y_image+6, f"Titulo: {title}")
    #rate
    pdf.text(x_image + 60 , y_image+12, f"Puntuación: {rate}")
    #description
    text = split_text(['Arial', 'B', 12],description,115)
    y = y_image+18
    for i,e in enumerate(text):
        if i < 7:
            pdf.text(x_image + 60, y, e)
            y += 5
        else:
            pdf.text(x_image + 60, y, e[:-3]+"...")
            break
    



def split_text(font, text, width):
    ver = FPDF()
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
    ver = FPDF()
    ver.set_font(font[0], font[1], font[2])
    return 10 + (width - ver.get_string_width(text))/2

def resize_text(font, text, width):
    ver = FPDF()
    ver.set_font(font[0], font[1], font[2])
    if ver.get_string_width(text) > width:
        while ver.get_string_width(text) >= width:
            text = text[:-1]
        text = text[:-7] + "..."
    return text

