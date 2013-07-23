
from zope import schema
from zope.interface import Interface
from zope.component import getUtility

from collective.socialpublish import SocialPublishMessageFactory as _

<<<<<<< HEAD
=======
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
    return SimpleVocabulary(types)

def types1(context):
    # return ['aaa', 'ggggg']
    # return [{'ddd' : 'ddd'}, {'bbb', 'bbb'}]
    return SimpleVocabulary([{'id' : 'ddd', 'title' : 'bbb'},
                             {'id' : "adaa", 'title' : 'adaa'}])

myVocabulary = SimpleVocabulary.fromItems((
    (u"Foo", "id_foo"),
    (u"Bar", "id_bar")))
>>>>>>> 4b64217a74171333e979984e2c08ba833b33dba5


class ISocialPublishControlPanel(Interface):
    """Social Publish setting interface
    """
<<<<<<< HEAD
=======
    # voca = selectable_types

    # profession = schema.Choice(source=selectable_types,
    #                            required=False,
    #                            title=_(u'content types'),
    #                            description=_(u'Select content types',
    #                                          default=u'Select content type'),
    # )
>>>>>>> 4b64217a74171333e979984e2c08ba833b33dba5

    content_types = schema.Set(
        required=False,
        title=_(u'content types'),
        description=_(u'Select content types',
                      default=u'Select content type'),
        default=set(),
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"),
        )

    workflow_transitions = schema.Set(
        required=False,
        title=_(u'workflow transitions'),
        description=_(u'Select workflow transitions',
                      default=u'Select workflow transitions'),
        default=set(),
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.WorkflowTransitions"),

        )



