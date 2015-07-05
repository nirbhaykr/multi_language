from django.views.generic.base import TemplateView
from django.utils import translation

# Create your views here.

class HomePageView(TemplateView):
    """
        Class for home page
    """
    template_name = "about.html"


class SetLangView(TemplateView):
    """
        Class for change language request
    """
    template_name = "about.html"
    
    def get(self, request, *args, **kwargs):
        """
            Change Language Logic
        """
        try:
            request.session['LANG'] = kwargs['lang_code'] 
            translation.activate(request.session['LANG'])
            request.LANGUAGE_CODE = translation.get_language()
        except:
            pass
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    