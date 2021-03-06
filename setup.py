from setuptools import setup, find_packages
import os

version = '1.0a2'

setup(name='collective.socialpublish',
      version=version,
      description="Automate content publishing to social networks for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone facebook twitter',
      author='Manabu TERADA, Takanori Suzuki',
      author_email='',
      url='https://github.com/takanory/collective.socialpublish',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'five.grok',
          'plone.directives.form',
          'tweepy',
          'facebook-sdk',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
