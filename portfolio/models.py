from django.db import models
from wagtail.images.models import Image, AbstractImage, AbstractRendition

# Create your models here.
from django import forms
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
    )
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel

from dianarice.blocks import BaseStreamBlock


@register_snippet
class Category(models.Model):
    """
    A Django model to store set of art categories.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/portfolio/categories/) In the BreadPage
    model you'll see we use a ForeignKey to create the relationship between
    Category and PorfolioPage. This allows a single relationship (e.g only one
    Category can be added) that is one-way (e.g. Categories will have no way to
    access related PorfolioPage objects).
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Artwork Categories"


class PortfolioPage(Page):
    """
    Detail view for a specific artwork
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        MultiFieldPanel(
            [
                FieldPanel(
                    'category',
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Additional Metadata",
            classname="collapsible collapsed"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    parent_page_types = ['PortfolioIndexPage']


class SketchbookPage(Page):
    """
    Detail view for a specific artwork
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        MultiFieldPanel(
            [
                FieldPanel(
                    'category',
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Additional Metadata",
            classname="collapsible collapsed"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    parent_page_types = ['SketchbookIndexPage']


class PortfolioIndexPage(Page):
    """
    Index page for artworks.

    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    # Can only have BreadPage children
    subpage_types = ['PortfolioPage']

    # Returns a queryset of PortfolioPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_artworks(self):
        return PortfolioPage.objects.live().descendant_of(
            self).order_by('-first_published_at')

    # Allows child objects (e.g. Porfolio objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_artworks(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request):
        context = super(PortfolioIndexPage, self).get_context(request)

        # PortfolioPage objects (get_breads) are passed through pagination
        artworks = self.paginate(request, self.get_artworks())

        context['artworks'] = artworks
        print(context)
        return context


class SketchbookIndexPage(Page):
    """
    Index page for artworks.

    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    # Can only have BreadPage children
    subpage_types = ['SketchbookPage']

    # Returns a queryset of PortfolioPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_artworks(self):
        return SketchbookPage.objects.live().descendant_of(
            self).order_by('-first_published_at')

    # Allows child objects (e.g. Porfolio objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_artworks(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request):
        context = super(SketchbookIndexPage, self).get_context(request)

        # PortfolioPage objects (get_breads) are passed through pagination
        artworks = self.paginate(request, self.get_artworks())

        context['artworks'] = artworks
        print(context)
        return context

class CustomImage(AbstractImage):
    # Add any extra fields to image here
        
    # eg. To add a caption field:

    caption = models.CharField(max_length=255, blank=True)
    admin_form_fields = Image.admin_form_fields + (
    # Then add the field names here to make them appear in the form:
    'caption',
    )

class CustomRendition(AbstractRendition):

   image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')
   class Meta:
      unique_together = (
      ('image', 'filter_spec', 'focal_point_key'),
      )
