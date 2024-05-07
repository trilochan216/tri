from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings

def save_pdf(params: dict):
    template = get_template("pdfs/invoice.html")
    html = template.render(params)
    response = BytesIO()
    pisa_status = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()

    try:
        output_path = str(settings.BASE_DIR) + f"/public/static/{file_name}.pdf"
        with open(output_path, 'wb+') as output:
            output.write(response.getvalue())

    except Exception as e:
        print("Error saving PDF:", e)

    if pisa_status.err:
        return '', False

    return str(file_name), True
