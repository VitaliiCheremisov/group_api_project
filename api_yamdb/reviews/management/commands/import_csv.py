import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import CustomUser
from reviews.models import Category, Comment, Genre, Reviews, Title