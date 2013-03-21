
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import Interface
from zope.component import getUtility
from zope.i18n import translate
from five import grok
# from plone.registry import field
from plone.directives import form
# from Products.CMFCore.interfaces import ISiteRoot

from collective.socialpublish import SocialPublishMessageFactory as _

@grok.provider(IContextSourceBinder)
def selectable_types(context):
    vocab_factory = getUtility(IVocabularyFactory,
                        name="plone.app.vocabularies.ReallyUserFriendlyTypes")
    types = []
    for v in vocab_factory(context):
        if v.title:
            title = translate(v.title, context=context.request)
        else:
            title = translate(v.token, domain='plone', context=context.request)
        types.append(dict(id=v.value, title=title) )
    def _key(v):
        return v['title']
    types.sort(key=_key)
    return types
    return SimpleVocabulary(types)

def types1(context):
    # return ['aaa', 'ggggg']
    # return [{'ddd' : 'ddd'}, {'bbb', 'bbb'}]
    return SimpleVocabulary([{'id' : 'ddd', 'title' : 'bbb'},
                             {'id' : "adaa", 'title' : 'adaa'}])

myVocabulary = SimpleVocabulary.fromItems((
    (u"Foo", "id_foo"),
    (u"Bar", "id_bar")))


class ISocialPublishControlPanel(Interface):
    """Social Publish setting interface
    """
    voca = selectable_types

    content_types = schema.Set(
        required=False,
        title=_(u'content types'),
        description=_(u'Select content types',
                      default=u'Select content type'),
        default=set(),
        # value_type=schema.Choice(title=u"types", source=selectable_types),

        value_type=schema.TextLine(title=u"types"),
        # value_type=schema.Choice(title=u"types",
        #                          vocabulary=u'types1'),
        # source=selectable_types,
        # value_type=schema.Choice(values=[]),
        )

    workflow_transactions = schema.Text(
        required=False,
        title=_(u'workflow transactions'),
        description=_(u'Select workflow transactionss',
                      default=u'Select workflow transactions'),
        default=u"",
        )



