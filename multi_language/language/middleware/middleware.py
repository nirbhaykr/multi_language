from django.utils import translation
from location.models import City, Country, UserLocation
from ipware.ip import get_ip
from django.utils.translation import ugettext
from django.conf import settings
import urllib2
import json


class SetLangMiddleware(object):
    """Middleware for change language and
        saving user's ip and location""" 
    
    def process_template_response(self,request, response):
#     def process_response(self, request, response):
        """
        Process Response
        """
        translation.activate(request.session.get('LANG','en'))
        request.LANGUAGE_CODE = translation.get_language()
        if not request.session.get('visted',None):
            try:
                ip = get_ip(request)
                if ip is not None:
                    user_data = self.get_data(ip)
                    if user_data['country_code']:
                        if UserLocation.objects.filter(ip=ip).count() == 0:
                            country_obj,flag = Country.objects.get_or_create\
                                    (country=user_data['country_name'])
                            city_obj,flag = City.objects.get_or_create\
                                    (country=country_obj, city=user_data['city'])
                            UserLocation.objects.create(ip=ip,zipcode=\
                                        user_data['zip_code'],city=city_obj)
                        request.session['visted'] = True
                        request.session['ip_message'] = ugettext("Location Saved successfully")
                    else:
                        request.session['ip_message'] = ugettext("Error occured while saving location")
                else:
                    request.session['ip_message'] = ugettext("Error occured while saving location")
            except:
                request.session['ip_message'] = ugettext("Error occured while saving location")
        else:
            request.session['ip_message'] = None
        return response
            
#     def process_response(self, request, response):
#         translation.deactivate()
#         return response
    
    def get_data(self,ip):
        """
            Get Location Data from API
        """
        geo_url= "{}{}".format(settings.FREE_GEO_IP_URL,ip)
        req = urllib2.Request(geo_url)
        response = urllib2.urlopen(req)
        json_page = response.read()
        user_data = json.loads(json_page)
        return user_data
        
#         http://freegeoip.net/json/14.192.96.0