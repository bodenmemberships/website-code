from django.conf import settings
from ..models import Customer
import logging


logger = logging.getLogger(__name__)

# A context processor to add the default information to the current Context
# - variables: from settings files
# - login: from cookies to show login/logout info and welcome msg
# - cookies: added to context for quick referencing
# - customer: added to context and cached for quick referencing
def set_default_values(request):

    variables = get_context_variables(request)

    customer = get_visitor(request)

    login = request.session.get('session_login')
    if not login:
        login = {'authenticated': (
            get_context_variable(request, 'ERIGHTS', '') != '' and get_context_variable(request, 'sm_constitid',
                                                                                        '') != '')}
        if login['authenticated']:
            login['command'] = 'logout'
            login['label'] = 'Sign Out'
        else:
            login['command'] = 'login'
            login['label'] = 'Sign In'
        # if our host is localhost or 127.0.0.1 then lets use our login that sets cookies specifically for testing
        # otherwise we route to erights
        if get_context_variable(request, 'REMOTE_ADDR') == '127.0.0.1':
            login['url'] = "/localhost/" + str(login['command']) + "/"
        else:
            # build out the erights url for if we are not localhost
            login['target_url'] = request.get_full_path()
            login['url'] = "/appssecured/login/servlet/ErightsLoginServlet?g=ci&command=" + str(login['command']) + \
                           "&ERIGHTS_TARGET=" + str(login['target_url'])

        # TODO: add more login stuff if needed
        request.session['session_login'] = login
    #logging.error('login - ' + str(login))

    # NOTE: cookies are not generated so just append them to the context under cookies; no session info needed
    #logging.error('cookies - ' + str(request.COOKIES))

    return {
        'variables': variables,
        'cookies': request.COOKIES,
        'login': login,
        'customer': customer,
    }


# environment variables are looked up:
# - as a header
# - as a variable in settings file
# - as a cookie
# - if debug: as a parameter
# NOTE: first one found wins
def get_context_variable(request, variable_name, default_value=None):
    debug = getattr(settings, "DEBUG", True)
    header_name = variable_name.upper()
    value = request.META.get(header_name, None)
    if value is None:
        if not header_name.startswith("HTTP"):
            header_name = "HTTP-" + header_name
        value = request.META.get(header_name,
                                 getattr(settings, variable_name,
                                         request.COOKIES.get(variable_name, None)))
    if value is None and debug:
        if variable_name in request.POST:
            value = request.POST[variable_name]
        if value is None and variable_name in request.GET:
            value = request.GET[variable_name]
    if value is None:
        value = default_value
    return value


def get_context_variables(request):
    # get the environment and debug variables from the config file
    #  NOTE: add to server side variables and check for future requests
    # try and read the dictionary value from the session; if not found then create it and put it in this session
    variables = None  # request.session.get('session_variables')
    if not variables:
        variables = {"ENVIRONMENT": get_context_variable(request, "ENVIRONMENT", "localhost"),
                     "DEBUG": get_context_variable(request, "DEBUG", True),
                     "DATA_DIR": get_context_variable(request, "DATA_DIR"),
                     "BASE_DIR": get_context_variable(request, "BASE_DIR"),
                     "PROJECT_DIR": get_context_variable(request, "PROJECT_DIR"),
                     "STATIC_URL": get_context_variable(request, "STATIC_URL"),
                     "MEDIA_URL": get_context_variable(request, "MEDIA_URL"),
                     "STATIC_ROOT": get_context_variable(request, "STATIC_ROOT"),
                     "MEDIA_ROOT": get_context_variable(request, "MEDIA_ROOT"),
                     "vid": get_context_variable(request, "vid"),}
        # TODO: add more expected variables here as needed from the settings files
        request.session['session_variables'] = variables
    # load in any variables we don't already have but are parameters
    # if dev then replace with parameters to make it easier to debug
    for key, value in request.GET.items():
        # if debug then replace the value with the parameters
        if variables.get('DEBUG', False):
            variables[key] = value
        else:
            if key not in variables:
                variables[key] = get_context_variable(request, key)
    for key, value in request.POST.items():
        # if debug then replace the value with the parameters
        if variables.get('DEBUG', False):
            variables[key] = value
        else:
            if key not in variables:
                variables[key] = get_context_variable(request, key)

    #logging.error('variables - ' + str(variables))
    return variables


def get_visitor(request):
    cid = get_context_variable(request, "cid")
    if not cid:
        cid = get_context_variable(request, "sm_constitid")
    # if our customerid changed then reset the login and customer cache
    visitor = request.session.get('session_visitor')
    if visitor and visitor.id and unicode(visitor.id) != cid:
        request.session['session_visitor'] = None
    # re-read to make sure to pick up nulled values above
    visitor = request.session.get('session_visitor')
    visitor = None
    if not visitor:
        # read the customer from db and cache it up
        try:
            visitor = Customer.objects.get(pk=cid)
            # visitor.set_achievement_token()
            request.session['session_visitor'] = visitor
        except Customer.DoesNotExist:
            visitor = None

    #logging.error('customer - ' + str(visitor))
    # if visitor:
    #     logging.error('visitor call to is_officer: ' + str(visitor.has_classification("OFFICER")))
    return visitor
