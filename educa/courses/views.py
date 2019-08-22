# -*- coding:utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps

from .models import Course, Module, Content
from .forms import ModuleFormSet


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("courses:manage_course_list")
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    permission_required = "courses.delete_course"
    template_name = "courses/manage/course/delete.html"
    success_url = reverse_lazy("courses:manage_course_list")


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model,
            exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name,  id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name,  id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name,  id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
                return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)

