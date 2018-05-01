from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product


# Create your views here.

class ProductFeaturedListView(ListView):

    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    template_name = 'products/product_detail.html'

    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.featured()


class ProductListView(ListView):

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all()


class ProductDetailView(DetailView):
    queryset = Product.objects.all()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = get_object_or_404(Product, slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product Not exists")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Hmmmmmm...')

        return instance
# class ProductDetailView(DetailView):
#     # queryset = Product.objects.all()
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         return context
#
#     def get_object(self, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         print(instance)
#         if instance is None:
#             raise Http404("Product doesn't exist")
#         return instance
