from django.shortcuts import render
from django.urls import path
from django.views.generic import View, TemplateView, UpdateView, CreateView, DeleteView,ListView, DetailView
from products.models import *
from . import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from products.forms import PBIForm, TaskForm,RegisterationForm,DevSignUpForm,POSignUpForm,SMSignUpForm,ProductForm
from django.http import JsonResponse



class ChangeSprintView(TemplateView):
	template_name = 'chang_sprint.html'

	def get_context_data(self, **kwargs):
		context = super(ChangeSprintView, self).get_context_data(**kwargs)
		context['product'] = Product.objects.get(pk=1)
		context['tasks'] = Task.objects.all()
		context['pbis'] = PBI.objects.filter(in_sprint=True)

		x = 1
		if (context['product'].sprint_status == 'NOT_YET_START' and x != 0):
			context['product'].sprint_status = 'START'
			x-=1
		elif (context['product'].sprint_status == 'START' and x != 0):
			for i in context['pbis']:
				if i.total_effort_hours == 0:
					i.status = 'DONE'
					i.in_sprint = False
					i.save()
			context['product'].sprint_status = 'FINISH'
			x-=1
		elif (context['product'].sprint_status == 'FINISH' and x != 0):
			context['product'].sprint_status = 'NOT_YET_START'
			x-=1
		context['product'].save()

		return context

class FullProductView(TemplateView):
	template_name = 'productfullview.html'

	def get_context_data(self, **kwargs):
		context = super(FullProductView, self).get_context_data(**kwargs)
		context['titled'] = ['Name', 'Product Owner', 'Scrum Master', 'Sprint Status']
		context['rows'] = Product.objects.all().order_by('sprint_status')
		context['product'] = Product.objects.filter(pk=self.kwargs.get('pk'))
		return context

class PBIView(TemplateView):
	template_name = 'pbi.html'

	def get_context_data(self, **kwargs):
		context = super(PBIView, self).get_context_data(**kwargs)
		context['title'] = ['Priority', 'Feature', 'Status', 'Story Point', 'Cumulative Story Point']
		context['rows'] = PBI.objects.all().order_by('priority')
		#context['product'] = Product.objects.get(pk=1)
		context['product'] = Product.objects.filter(pk=self.kwargs.get('pk'))
		x = 1
		for i in context['rows']:
			if (i.priority != x):
				i.priority = x
				i.save()
			x+=1

		cumulative = 0
		for i in context['rows']:
			i.cumulative_story_point = 0

		for i in context['rows']:
			if (i.status != "DONE"):
				cumulative = cumulative + i.story_point
				i.cumulative_story_point = cumulative

		return context

class FullPBIView(TemplateView):
	template_name = 'pbi_full_view.html'

	def get_context_data(self, **kwargs):
		context = super(FullPBIView, self).get_context_data(**kwargs)
		context['title'] = ['Priority', 'Feature', 'Status', 'Story Point', 'Cumulative Story Point']
		context['rows'] = PBI.objects.all().order_by('priority')
		context['product'] = Product.objects.get(pk=1)
		x = 1
		for i in context['rows']:
			if (i.priority != x):
				i.priority = x
				i.save()
			x+=1

		cumulative = 0
		for i in context['rows']:
			i.cumulative_story_point = 0

		for i in context['rows']:
			cumulative = cumulative + i.story_point
			i.cumulative_story_point = cumulative

		return context

class AddProductView(CreateView):
	model = Product
	fields = '__all__'
	template_name = 'add_product.html'

	def get(self,request):
		form = ProductForm()
		self.Product = Product.objects.values()
		return render(request,self.template_name,{
            'Product': self.Product, \
			'form': form})

	def post(self, request):
		form = ProductForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form = ProductForm()
		return redirect('/viewPBI')

class AddPBIView(CreateView):
	model = PBI
	fields = '__all__'
	template_name = 'add_pbi.html'

	def get(self,request):
		form = PBIForm()
		self.PBI = PBI.objects.values()
		return render(request,self.template_name,{
            'PBI': self.PBI, \
			'form': form})

	def post(self, request):
		form = PBIForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form = PBIForm()
		return redirect('/viewPBI')

class DeletePBIView(DeleteView):
	model = PBI
	template_name = 'delete_pbi.html'
	success_url = '/viewPBI/'
	context_object_name = 'PBI'


class EditPBIView(UpdateView):
	model = PBI
	fields = ['name','priority','description','story_point']
	template_name = 'edit_pbi.html'
	success_url = '/viewPBI/'
	context_object_name = 'edit'


class PBIDetailView(DetailView):
	model = PBI
	template_name = 'detail_pbi.html'
	success_url = '/viewPBI/'
	context_object_name = 'PBI'

class addtoSprint(UpdateView):
	model = PBI
	fields = ['in_sprint']
	template_name = 'add_to_Sprint.html'
	success_url = '/viewPBI/'
	context_object_name = 'PBI'

class SprintBacklogView(TemplateView):
	template_name = 'sprint.html'

	def get_context_data(self, **kwargs):
		context = super(SprintBacklogView, self).get_context_data(**kwargs)
		context['title'] = ['PBI', 'Tasks', 'Total Effort Hours']
		context['pbis'] = PBI.objects.filter(in_sprint = True)
		context['tasks'] = Task.objects.all()
		context['product'] = Product.objects.get(pk=1)

		context['sprint_total_effort_hours'] = 0
		context['sprint_tatal_story_points'] = 0
		for i in context['pbis']:
			for j in context['tasks']:
				if (i.name == j.pbi.name and j.status != "DONE"):
					i.total_effort_hours += j.hour
			context['sprint_total_effort_hours'] += i.total_effort_hours
			context['sprint_tatal_story_points'] += i.story_point

		return context

class FullSprintBacklogView(TemplateView):
	template_name = 'sprint_full.html'

	def get_context_data(self, **kwargs):
		context = super(FullSprintBacklogView, self).get_context_data(**kwargs)
		context['title'] = ['PBI', 'Tasks', 'Total Effort Hours']
		context['pbis'] = PBI.objects.filter(in_sprint = True)
		context['tasks'] = Task.objects.all()
		context['product'] = Product.objects.get(pk=1)
		context['sprint_total_effort_hours'] = 0
		context['sprint_tatal_story_points'] = 0
		for i in context['pbis']:
			for j in context['tasks']:
				if (i.name == j.pbi.name):
					i.total_effort_hours += j.hour
			context['sprint_total_effort_hours'] += i.total_effort_hours
			context['sprint_tatal_story_points'] += i.story_point

		return context

class AddTaskView(CreateView):
	model = Task
	fields = '__all__'
	template_name = 'add_task.html'

	def get(self,request):
		form = TaskForm()
		self.Task = Task.objects.values()
		return render(request,self.template_name,{
            'Task': self.Task, \
			'form': form})

	def post(self, request):
		form = TaskForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form = TaskForm()
		return redirect('/sprintBacklog/')

class changePBIStatus(UpdateView):
	model = Product
	fields = ['sprint_status']


class DeleteTaskView(DeleteView):
	model = Task
	template_name = 'delete_task.html'
	success_url = '/sprintBacklog/'
	context_object_name = 'Task'

class EditTaskView(UpdateView):
	model = Task
	fields = ['pbi','name','description','hour','status','owner']
	template_name = 'edit_task.html'
	success_url = '/sprintBacklog/'
	context_object_name = 'edit'

class TaskDetailView(DetailView):
	model = Task
	template_name = 'detail_task.html'
	success_url = '/sprintBacklog/'
	context_object_name = 'task'

def registerView(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/viewPBI')
    else:
        form = RegisterationForm()
    return render(request, 'reg_form.html', {'form': form})

def DevRegisterView(request):
    if request.method == 'POST':
        form = DevSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/viewPBI')
    else:
        form = DevSignUpForm()
    return render(request, 'dev_reg_form.html', {'form': form})

def PoRegisterView(request):
    if request.method == 'POST':
        form = POSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/viewPBI')
    else:
        form = POSignUpForm()
    return render(request, 'po_reg_form.html', {'form': form})

def SMRegisterView(request):
    if request.method == 'POST':
        form = SMSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/viewPBI')
    else:
        form = SMSignUpForm()
    return render(request, 'sm_reg_form.html', {'form': form})

def profile(request):
	args = {'user': request.user}
	return render(request,'profile.html',args)

def updateRole(request):
	sprint_status = request.GET.get('sprint_status','NOT_YET_START')
	product_id = request.GET.get('product_id', False)
	Product = Product.objects.get(pk=product_id)
	try:
		Product.sprint_status = sprint_status
		Product.save()
		return JsonResponse({"success": 'START'})
	except Exception as e:
		return JsonResponse({"success": 'NOT_YET_START'})
	return JsonResponse(data)
