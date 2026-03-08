from pypdf import PdfReader, PdfWriter

with open("split.txt", "r") as file:
    data = file.readlines()

page_dict={}
for x in data:
    colon_pos = x.find(':')
    hyphen_pos = x.find('-')

    title = x[:colon_pos]
    firstnumber = int(x[(colon_pos+2):hyphen_pos].strip()) - 1
    secondnumber = int(x[(hyphen_pos+1):].strip()) 

    page_dict[title] = [firstnumber, secondnumber]

print(page_dict)

with open("Schuetz.pdf", 'rb') as pdf_file:
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for k, v in page_dict.items():
        for page in reader.pages[v[0]:v[1]]:
            writer.add_page(page)

            with open("./readyscan/Schuetz/" + k + ".pdf", 'wb') as output_pdf:
                writer.write(output_pdf)

        writer = PdfWriter()

