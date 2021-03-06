import factory
import itertools

from factory.django import DjangoModelFactory

from django.conf import settings
from django.db.models import get_model
from django.utils.translation import get_language

from fancypages.utils import get_page_model, get_node_model
from fancypages.compat import get_user_model


PAGE_GROUPS_NAMES = itertools.cycle(['Primary Navigation', 'Footer'])

FancyPage = get_page_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = 'peter.griffin'
    email = 'peter@griffin.com'
    is_staff = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
            if create:
                self.save()


class PageTypeFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'PageType')

    name = 'Sample page type'
    slug = 'sample-page-type'
    template_name = settings.FP_DEFAULT_TEMPLATE


class PageGroupFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'PageGroup')

    name = factory.LazyAttribute(lambda a: PAGE_GROUPS_NAMES.next())


class PageNodeFactory(DjangoModelFactory):
    class Meta:
        model = get_node_model()

    name = factory.Sequence(lambda n: "Node {}".format(n))

    @classmethod
    def _generate(cls, create, attrs):
        if not create:
            return cls._meta.model(**attrs)

        if 'parent' in attrs:
            parent = attrs.pop('parent')
            node = parent.node.add_child(**attrs)
        else:
            node = cls._meta.model.add_root(**attrs)
        return node


class FancyPageFactory(DjangoModelFactory):
    class Meta:
        model = FancyPage

    status = FancyPage.PUBLISHED
    node = factory.SubFactory(PageNodeFactory)


class ContainerFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'Container')

    name = factory.Sequence(lambda n: 'test-container {}'.format(n))
    language_code = get_language()


class TextBlockFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'TextBlock')

    text = 'This is a sample text in a text block.'
    container = factory.SubFactory(ContainerFactory)


class TitleTextBlockFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'TitleTextBlock')

    title = 'The title'
    text = 'This is a sample text in a text block.'


class HorizontalSeparatorBlockFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'HorizontalSeparatorBlock')


class TabBlockFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'TabBlock')

    container = factory.SubFactory(ContainerFactory)


class TwoColumnLayoutBlockFactory(DjangoModelFactory):
    class Meta:
        model = get_model('fancypages', 'TwoColumnLayoutBlock')

    container = factory.SubFactory(ContainerFactory)
