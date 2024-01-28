from django.shortcuts import render
from site_module.models import SiteSetting, FooterLinkBox
from django.core.cache import cache
# Create your views here.


def site_header_component(request):
    if cache.get('site_setting'):
        setting = cache.get('site_setting')
    else:
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        cache.set('site_setting',setting,timeout=900)
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/front/site_header_component.html', context)


def site_footer_component(request):
    setting = cache.get('site_setting')
    if cache.get('footer_link_boxes'):
        footer_link_boxes = cache.get('footer_link_boxes')
    else:
        footer_link_boxes: FooterLinkBox = FooterLinkBox.objects.all().prefetch_related('footerlink_set')
        cache.set('footer_link_boxes',footer_link_boxes,timeout=900)
        
    context = {
        'footer_link_boxes': footer_link_boxes,
        'site_setting': setting,
    }
    return render(request, 'shared/front/site_footer_component.html', context)   
