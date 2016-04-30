from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import PublicationSubscriptionForm
from .models import PublicationSubscription
from mainsite.context_processors.spe_context import (
    get_context_variable, )


def publications(request):
    pubs = PublicationSubscription.objects.all()
    return render(request, 'spe_contact/publications.html', {'publications': pubs})

# Create your views here.
def publication_new(request):
    if request.method == "POST":
        form = PublicationSubscriptionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.customer_id = get_context_variable(request, "cid", get_context_variable(request, "sm_constitid", ""))
            post.save()
            return redirect('publications')
    else:
        form = PublicationSubscriptionForm()

    return render(request, 'spe_contact/publication_subscription_form_wrapper.html', {'form': form})

def publication_submit(request):
        if request.is_ajax():
            try:
                form = PublicationSubscriptionForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.customer_id = get_context_variable(request, "cid", get_context_variable(request, "sm_constitid", ""))
                    post.save()
                    return HttpResponse(str('success'))
                else:
                    return HttpResponse(str('form is invalid: print the invalid stuff...'))
            except KeyError:
                return HttpResponse('Error') # incorrect post
        else:
            raise Http404
