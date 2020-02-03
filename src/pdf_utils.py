from fpdf import FPDF 
import pandas as pd 

def create_pdf():
    pdf = FPDF('P','mm','A4')
    pdf.set_font('Arial', 'B', 12)

    pdf.cell(64, 56, 'Hello, World!',1,1,'C')
    pdf.cell(64, 56, 'Hello, World!',1,1,'C')
    pdf.cell(64, 56, 'Hello, World!',1,1,'C')



    pdf.output("archivo.pdf",'F')




def cell_film(pdf=None, image="", x=10, y=10 ,h=51, description="", rate="", win="", name="", category=""):
    URL = "http://image.tmdb.org/t/p/w300/"
    pdf.set_font('Arial', 'B', 12)

    if image == "":
        name = "img/not_found.jpg"
    else:
        name = URL + image
    if pdf == None:
        pdf = FPDF('P','mm','A4')
    if win == 'y':
        pdf.set_fill_color(153,153,0)
    if win == 'n':
        pdf.set_fill_color(204,229,255)
    if image != "":
        pdf.image(name, x, y, h=h)
    else:
        pdf.image(name, x, y, h=h)

    pdf.cell(64, 56, rate,1,1,'C')
    pdf.cell(64, 56, name,1,1,'C')