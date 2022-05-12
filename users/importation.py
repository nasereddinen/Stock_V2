from typing_extensions import get_args
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from .filter import ArticleFilter
from django.db.models import Sum, query
from .form import *
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
import csv

from users import form
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Count, F, Value
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from .viewDisc import datacor
from json import dumps
from django.contrib.auth import get_user_model