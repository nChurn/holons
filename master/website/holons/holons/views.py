import logging
import json

from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

from helpers.render_helper import custom_render
from email_api.helpers import auth_helper

from invitation.token import smart_redirect
from health.status import rays as rays_health
from accounts.models import User


def handler404(request: HttpRequest, *args, **argv) -> HttpResponse:
    """Serve custom 404 error page if DEBUG = False """
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request: HttpRequest, *args, **argv) -> HttpResponse:
    """Serve custom 500 error page if DEBUG = False """
    response = render(request, '500.html')
    response.status_code = 500
    return response


def cors_data(request: HttpRequest) -> HttpResponse:
    """Feed Matrix user data to make it available across subdomains """
    user_data = request.user
    user = User.objects.filter(pk=user_data.id).first()
    # :fixme: looks like shit
    cors_storage = user.cors_storage.replace('\'', '"')
    return custom_render(
      request,
      'cors-data.html',
      {'user_data': json.loads(cors_storage)}
    )


def layers(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers.html',
    )


def moneta_coins(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'moneta.html',
    )


def moneta(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'moneta.html',
    )


def identity(request: HttpRequest) -> HttpResponse:
    username = request.user.username
    return custom_render(
      request,
      'identity.html',
      {'username': username}
    )

def agenda(request: HttpRequest) -> HttpResponse:
    return custom_render( request,'index2.html')


def broker(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'broker/broker.html',
    )


def broker_talent(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'broker/talent.html',
    )


def broker_pheme(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'broker/pheme.html',
    )


def broker_grinstock(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'broker/grin-stock.html',
    )


def index(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'index.html',
    )


def email(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'email/email.html',
    )


def relations(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'relations/relations.html',
    )


def rays(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'rays/rays.html',
    )


def platos_flywheel(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'platos_flywheel/platos_flywheel.html',
    )


def campaigns(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'campaigns.html',
    )


def login(request: HttpRequest) -> HttpResponse:
    if auth_helper.get_user(request).id:
      return redirect('/')
    return custom_render(request, 'auth/login.html')


def classic_login(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'auth/classic_login.html'
    )


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


def workspaces(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/workspaces-legacy.html',
    )


def health_status(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'health_status.html',
      {
        'hours': rays_health(),
      }
    )


def schedule(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'schedule-meet/schedule.html',
    )

def meet(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'schedule-meet/meet.html',
    )

def booking_example(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'schedule-meet/book.html',
    )

def outreach(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'outreach.html',
    )

def dial(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'dial.html',
    )

def digest(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'digest.html',
    )

def hearsay(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'hearsay.html',
    )


def xo(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'xo.html',
    )


def layers_talent(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/talent.html',
    )

def talent_payroll(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/payroll.html',
    )


def layers_hosting(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/hosting.html',
    )


def layers_sops(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/sops.html',
    )


def docs_wikis(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/docs_wikis.html',
    )


def layers_assets(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/assets.html',
    )


def layers_equity(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/equity.html',
    )


def layers_audits(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/audits.html',
    )


def layers_blackboxes(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/blackboxes.html',
    )


def layers_talent(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'layers/talent.html',
    )


def purpose(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'purpose.html',
    )

def canned(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'ray-canned.html',
)


def platos_flywheel_subscription(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'platos_flywheel/subscription.html',
)

# hardcoded profile annd portfolios
def portfolios(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/profile-grintender.html',
)

def grintender(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/profile-grintender.html',
)

def grintender_words(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/profile-grintender-words.html',
)

def grintender_deeds(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/profile-grintender-deeds.html',
)

def grintender_deeds_azb(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-azb.html',
)
def grintender_deeds_avo(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-avo.html',
)
def grintender_deeds_prime(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-prime.html',
)
def grintender_deeds_carpedia(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-car.html',
)
def grintender_deeds_tennis(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-tennis.html',
)

def grintender_deeds_lid(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-lid.html',
)

def grintender_deeds_king(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-king.html',
)

def grintender_deeds_pc(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-pc.html',
)

def grintender_deeds_corinth(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-corinth.html',
)

def grintender_deeds_launcher(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-launcher.html',
)

def grintender_deeds_oil(request: HttpRequest) -> HttpResponse:
    return custom_render(
      request,
      'portfolios/grintender-deeds/grintender-deeds-oil.html',
)
