from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
from logger import get_logger


LOGGER = get_logger("extract_personnel_pdfs")


def open_pdf(pdf_path, output_path):
    try:
        with open(pdf_path, "rb") as f:
            LOGGER.info(f"opening path: {pdf_path}")
            pdf = PdfFileReader(f)
            not_assigned_pages = iterate_pages(pdf, output_path)

            return not_assigned_pages
    except ValueError as e:
        LOGGER.debug(str(e))
        raise ValueError(str(e))
    except Exception as e:
        LOGGER.debug(f"pdf_path couldn't be opened ({pdf_path}); {str(e)}")
        raise OSError(f"pdf_path couldn't be opened ({pdf_path})")


def get_first_personnel_number(pdf):
    number_of_pages = pdf.getNumPages()

    for page in range(number_of_pages):
        page = pdf.getPage(page)
        text = page.extractText().split(" ")
        text_list = [word.strip() for word in text if (word != " " and word != "")]

        if "Personalnummer:" in text_list:
            return extract_personnel_infos_de(text_list)
        elif "Employee:" in text_list:
            return extract_personnel_infos_en(text_list)
        else:
            LOGGER.debug(f"could not find a personnel number: {text_list}")
            continue

    LOGGER.debug(f"could not find any personnel number.")
    raise ValueError("could not find any personnel number.")


def iterate_pages(pdf, save_to_path):
    number_of_pages = pdf.getNumPages()
    not_assigned_pages = []

    try:
        personnel_number, lastname, firstname, date = get_first_personnel_number(pdf)
        page_numbers_for_output = []

        for page_number in range(number_of_pages):
            text_list = extract_text(pdf, page_number)

            if "Personalnummer:" in text_list:
                personnel_number_index = text_list.index("Personalnummer:") + 1

                if text_list[personnel_number_index] == personnel_number:
                    page_numbers_for_output.append(page_number)
                elif text_list[personnel_number_index] != personnel_number:
                    save_path = f"{save_to_path}\\{date} {lastname}, {firstname}.pdf"
                    LOGGER.info(f"saving: {lastname} to file")
                    save_pdf(pdf, page_numbers_for_output, save_path)

                    (
                        personnel_number,
                        lastname,
                        firstname,
                        date,
                    ) = extract_personnel_infos_de(text_list)
                    LOGGER.info(
                        f"new personnel: {personnel_number}, {lastname}, {firstname}, {date}"
                    )
                    page_numbers_for_output = [page_number]
                else:
                    LOGGER.debug("could not find fitting personnel number.")
                    continue
            elif "Employee:" in text_list:
                personnel_number_index = text_list.index("Employee:") + 1

                if text_list[personnel_number_index] == personnel_number:
                    page_numbers_for_output.append(page_number)
                elif text_list[personnel_number_index] != personnel_number:
                    save_path = f"{save_to_path}\\{date} {lastname}, {firstname}.pdf"
                    LOGGER.info(f"saving: {lastname} to file")
                    save_pdf(pdf, page_numbers_for_output, save_path)

                    (
                        personnel_number,
                        lastname,
                        firstname,
                        date,
                    ) = extract_personnel_infos_en(text_list)
                    LOGGER.info(
                        f"new personnel: {personnel_number}, {lastname}, {firstname}, {date}"
                    )
                    page_numbers_for_output = [page_number]
                else:
                    LOGGER.debug("could not find fitting personnel number.")
                    continue
            else:
                not_assigned_pages.append(page_number)
                LOGGER.debug("could not find any personnel number.")
                continue

        save_path = f"{save_to_path}\\{date} {lastname}, {firstname}.pdf"
        save_pdf(pdf, page_numbers_for_output, save_path)

        return not_assigned_pages
    except Exception as e:
        LOGGER.debug(f"{str(e)}")
        raise ValueError(str(e))


def extract_text(pdf, page_number):
    page = pdf.getPage(page_number)
    text = page.extractText()

    return [word.strip() for word in text.split(" ")]


def extract_personnel_infos_de(info_list):
    try:
        personal_number_index = info_list.index("Name:")
        azp_regel_index = info_list.index("AZPRegel:")
        print(f"{personal_number_index}, {azp_regel_index}")
        personnel_number = info_list[info_list.index("Personalnummer:") + 1]
        lastname = info_list[info_list.index("Name:") + 2]
        firstname = info_list[info_list.index("Name:") + 1]
        date = datetime.strptime(
            info_list[info_list.index("Abrechnungszeitraum:") + 1], "%d.%m.%Y"
        ).strftime("%Y-%m")

        LOGGER.info(
            f"first personnel: {personnel_number}, {lastname}, {firstname}, {date}"
        )

        return personnel_number, lastname, firstname, date
    except:
        LOGGER.debug(f"Unknown data: {info_list}")
        return 0, "unbekannt", "unbekannt", datetime.now().strftime("%Y-%m")


def extract_personnel_infos_en(info_list):
    try:
        employee_index = info_list.index("Employee:")
        personnel_number = info_list[employee_index + 1]
        lastname = info_list[employee_index + 3]
        firstname = info_list[employee_index + 2]
        date = datetime.strptime(
            info_list[info_list.index("period:") + 1], "%d.%m.%Y"
        ).strftime("%Y-%m")

        LOGGER.info(
            f"first personnel: {personnel_number}, {lastname}, {firstname}, {date}"
        )

        return personnel_number, lastname, firstname, date
    except:
        LOGGER.debug(f"Unknown data: {info_list}")
        return 0, "unbekannt", "unbekannt", datetime.now().strftime("%Y-%m")


def save_pdf(pdf, pages, save_path):
    pdf_writer = PdfFileWriter()
    for page in pages:
        pdf_writer.addPage(pdf.getPage(page))

    try:
        with open(save_path, "wb") as output:
            pdf_writer.write(output)
    except Exception as e:
        LOGGER.debug(f"file couldn't be saved. {str(e)}")


if __name__ == "__main__":
    input_path = r"C:\SSD\Downloads\ZNW_data\ZNW_data\ZNW_big_file.pdf"
    output_path = r"C:\SSD\Downloads\ZNW_data\ZNW_data\neu"
    open_pdf(input_path, output_path)
