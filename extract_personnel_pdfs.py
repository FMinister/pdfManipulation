from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime


def open_pdf(pdf_path, output_path):
    with open(pdf_path, "rb") as f:
        pdf = PdfFileReader(f)
        iterate_pages(pdf, output_path)


def get_first_personnel_number(pdf):
    number_of_pages = pdf.getNumPages()

    for page in range(number_of_pages):
        page = pdf.getPage(page)
        text = page.extractText().split(" ")
        text_list = [word.strip() for word in text]

        if "Personalnummer:" in text_list[0:20]:
            return extract_personnel_infos(text_list)

    return 0, "unbekannt", "unbekannt", datetime.now().strftime("%Y-%m")


def iterate_pages(pdf, save_to_path):
    number_of_pages = pdf.getNumPages()

    personnel_number, lastname, firstname, date = get_first_personnel_number(pdf)
    page_numbers_for_output = []

    for page_number in range(number_of_pages):
        text_list = extract_text(pdf, page_number)

        if "Personalnummer:" in text_list[0:20]:
            personnel_number_index = text_list.index("Personalnummer:", 8, 12) + 1

            if text_list[personnel_number_index] == personnel_number:
                page_numbers_for_output.append(page_number)
            elif text_list[personnel_number_index] != personnel_number:
                save_path = f"{save_to_path}\\{date} {lastname}, {firstname}.pdf"
                save_pdf(pdf, page_numbers_for_output, save_path)

                personnel_number, lastname, firstname, date = extract_personnel_infos(
                    text_list[0:40]
                )
                page_numbers_for_output = [page_number]

    save_path = f"{save_to_path}\\{date} {lastname}, {firstname}.pdf"
    save_pdf(pdf, page_numbers_for_output, save_path)


def extract_text(pdf, page_number):
    page = pdf.getPage(page_number)
    text = page.extractText()

    return [word.strip() for word in text.split(" ")]


def extract_personnel_infos(info_list):
    try:
        personnel_number = info_list[info_list.index("Personalnummer:", 0, 15) + 1]
        lastname = info_list[info_list.index("Name:", 0, 20) + 2]
        firstname = info_list[info_list.index("Name:", 0, 20) + 1]
        date = datetime.strptime(
            info_list[info_list.index("Abrechnungszeitraum:", 0, 40) + 1], "%d.%m.%Y"
        ).strftime("%Y-%m")

        return personnel_number, lastname, firstname, date
    except:
        return 0, "unbekannt", "unbekannt", datetime.now().strftime("%Y-%m")


def save_pdf(pdf, pages, save_path):
    pdf_writer = PdfFileWriter()
    for page in pages:
        pdf_writer.addPage(pdf.getPage(page))

    with open(save_path, "wb") as output:
        pdf_writer.write(output)


if __name__ == "__main__":
    input_path = r"C:\SSD\Downloads\ZNW_data\ZNW_data\ZNW_big_file.pdf"
    output_path = r"C:\SSD\Downloads\ZNW_data\ZNW_data\neu"
    open_pdf(input_path, output_path)
