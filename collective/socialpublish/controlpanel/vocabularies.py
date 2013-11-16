# -*- coding:utf-8 -*-
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel
from collective.socialpublish.controlpanel.utils import fb_page_info_str_to_dict

class FbPrivacyVocabulary(object):
    """Vocabulary factory for fb_privacy_settings.

    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            ("SELF", "SELF", u"SELF"),
            ("ALL_FRIENDS", "", u"ALL_FRIENDS"),
            ("FRIENDS_OF_FRIENDS", "FRIENDS_OF_FRIENDS", u"FRIENDS_OF_FRIENDS"),
            ("EVERYONE", "EVERYONE", u"EVERYONE"),
        ]
        return SimpleVocabulary([SimpleTerm(item[0], item[1], item[2]) for item in items])

FbPrivacyVocabularyFactory = FbPrivacyVocabulary()


class FbPushSelectVocabulary(object):
    """

    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        items = [
            ("MY_Wall", "MY_WALL", u"MY Wall"),
        ]
        items.extend(self._get_pages())
        return SimpleVocabulary([SimpleTerm(item[0], item[1], item[2]) for item in items])

    def _get_pages(self):
        items = []
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialPublishControlPanel)
        fb_page_info = settings.fb_page_info
        dic = fb_page_info_str_to_dict(fb_page_info)
        for key, value in dic.items():
            items.append((key, value['token'], value['title']))
        return items

FbPushSelectVocabularyFactory = FbPushSelectVocabulary()