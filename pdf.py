import pdftotext


def read_pdf(name):
    # Load your PDF
    with open(name, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Read all the text into one string
    return " ".join(pdf)
