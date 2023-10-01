import csv

from django.conf import settings
from django.core.management.base import BaseCommand
# from # откуда? import User

from reviews.models import Category, Comment, Genre, Review, Title

