from django import views
from django import shortcuts as short
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ImageContent, QueryGroup, QueryImageRelation

# Create your views here.
class IndexView(views.View):
    def get(self, request):
        return short.render(request, 'base.html', { 'title': 'Index' })

class FullsetView(views.View):
    def get(self, request):
        context = {
            'title': 'Todas las imágenes',
            'images': ImageContent.objects.all()
        }
        return short.render(request, 'fullset.html', context)

class QueryGroupDetailView(views.View):
    def get(self, request, pk):
        qg = short.get_object_or_404(QueryGroup.objects, pk=pk)
        context = {
            'title': f'Lote {pk} ({qg.imagelist.count()}/{qg.get_max()})',
            'querygroup': qg,
            'qg_state': qg.get_state_str().capitalize(),
            'qg_size': qg.get_type_str()
        }
        return short.render(request, 'qgdetail.html', context)

class QueryGroupListView(views.View):
    def get(self, request: http.HttpRequest):
        all = request.GET.get('all') is not None
        context = {
            'title': 'Todos los lotes' if all else 'Lotes Activos',
            'querygroups': QueryGroup.objects.all() if all else QueryGroup.objects.exclude(printed=True),
        }
        return short.render(request, 'qglist.html', context)

class QueryGroupNewView(views.View):
    def get(self, request):
        from .forms import QueryGroupForm
        context = {
            'title': 'Crear nuevo Lote',
            'form': QueryGroupForm(),
        }
        return short.render(request, 'qgnew.html', context)
    def post(self, request):
        from .forms import QueryGroupForm
        form = QueryGroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            qg = QueryGroup()
            qg.type = cd['type']
            qg.save()
            return short.redirect(to='content:qglist')
            # return short.render(request, 'base.html', { 'title': 'Lote creado con exito.' })
        return short.render(request, 'base.html', { 'title': 'HA OCURRIDO UN ERROR.' })

class QueryGroupAddImageView(views.View):
    def get(self, request, pk):
        qg = short.get_object_or_404(QueryGroup.objects, pk=pk)
        from .forms import QueryGroupAddImageForm
        context = {
            'title': f'Agregar a Lote {pk}',
            'form': QueryGroupAddImageForm()
        }
        return short.render(request, 'qgaddimage.html', context)
    def post(self, request, pk):
        qg = short.get_object_or_404(QueryGroup.objects, pk=pk)
        from .forms import QueryGroupAddImageForm
        form = QueryGroupAddImageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            img = short.get_object_or_404(ImageContent.objects, pk=cd['image_pk'])
            link = QueryImageRelation()
            link.querygroup=qg
            link.imagecontent=img
            link.save()
            return short.redirect(to='content:qgdetail', pk=pk)
            # return short.render(request, 'base.html', { 'title': f'Imagen agregada con exito: L{pk} - {img.pk}' })
        return short.render(request, 'base.html', { 'title': 'HA OCURRIDO UN ERROR.' })

class QueryGroupPrintedView(views.View):
    def post(self, request, pk):
        qg = short.get_object_or_404(QueryGroup.objects, pk=pk)
        qg.printed = True
        qg.save()
        return short.redirect(to='content:qglist')
        # return short.render(request, 'base.html', { 'title': f'Marcado como impreso: Lote {pk}' })
