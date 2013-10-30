# -*- coding:utf-8 -*-
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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