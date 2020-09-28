import tempfile
from uuid import uuid5, NAMESPACE_URL
import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def get_datetime_now_in_msec():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def generate_random_str():
    now = get_datetime_now_in_msec()
    random = str(uuid5(NAMESPACE_URL, str(now)))
    return random.split("-")[0]


def render_html_to_pdf(html):
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def generate_html_from_template(template: str, context: dict, request):
    html_string = render_to_string(template, context=context, request=request)
    return HTML(string=html_string, base_url=request.build_absolute_uri())
