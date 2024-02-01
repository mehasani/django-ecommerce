from django.views.generic import ListView

from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from django.views.generic.edit import CreateView
from .models import ContactUs


# Create your views here.

class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact-us/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context
