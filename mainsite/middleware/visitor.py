from django.conf import settings
import uuid

FOREVER = 365 * 24 * 60 * 60 * 60 # 60 years
TRACKING_COOKIE = "vid"


class VisitorMiddleware(object):
    def process_response(self, request, response):
        # determine if we have a vid cookie
        vid = request.COOKIES.get(TRACKING_COOKIE, None)
        if not vid:
            # attempt to set one forever
            response.set_cookie(TRACKING_COOKIE, value=make_uuid(), max_age=FOREVER)
        return response

def make_uuid():
    return str(uuid.uuid4())
