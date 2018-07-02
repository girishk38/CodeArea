from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

import json

from .tasks import *
from .normal import judge_main_normal

# TODO: return current submission page with submission id

@login_required
def run_judge(request):
	result = task_main(request)
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
    # return judge_main(request)

@login_required
def run_judge_contest(request):
	result = task_contest(request)
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
    # return judge_main_contest(request)

@login_required
def run_judge_normal(request):
    return judge_main_normal(request)
