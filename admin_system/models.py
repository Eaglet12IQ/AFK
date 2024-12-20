from django.db import models
from django.shortcuts import render, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import Tasks
from django.http import HttpResponse, JsonResponse
import json 
