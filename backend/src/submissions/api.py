from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics, filters
from .serializers import SubmissionSerializer, SubmissionTasksSerializer, ContestSubmissionSerializer, ContestSubmissionTasksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Submission, SubmissionTasks, ContestSubmission, ContestSubmissionTasks
from problems.models import Problem
from rest_framework import viewsets
from rest_framework import status


class SubmissionViewSet(viewsets.ModelViewSet):

	queryset = Submission.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = SubmissionSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, )
	filter_fields = ('user', 'id', )

class SubmissionTasksViewSet(viewsets.ModelViewSet):

	queryset = SubmissionTasks.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = SubmissionTasksSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, )
	filter_fields = ('submission',)

class ContestSubmissionViewSet(viewsets.ModelViewSet):

	queryset = ContestSubmission.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ContestSubmissionSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, )
	filter_fields = ('user',)


class ContestSubmissionTasksViewSet(viewsets.ModelViewSet):

	queryset = ContestSubmissionTasks.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ContestSubmissionTasksSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, )
	filter_fields = ('submission',)