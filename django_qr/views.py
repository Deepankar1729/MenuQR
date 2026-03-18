from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from .forms import QRCodeForm
import qrcode
import os

@never_cache
def generate_qr(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            # generate qr code
            qr = qrcode.make(url)

            file_name = res_name.replace(" ",'_') + '_menu.png'

            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            qr.save(file_path)

            # create image url
            qr_url = os.path.join(settings.MEDIA_URL, file_name)

            context = {
                'res_name': res_name,
                'qr_url': qr_url,
                'file_name': file_name
            }

            return render(request, 'qr_result.html', context)
    else:
        form = QRCodeForm()

    return render(request, 'generate_qr.html', {'form': form})
