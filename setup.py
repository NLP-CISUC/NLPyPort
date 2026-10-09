from setuptools import setup, find_packages
setup(
  name = 'NLPyPort',         # How you named your package folder (MyLib)
  packages = find_packages(include=['NLPyPort', 'NLPyPort.*']),
  include_package_data = True,
  package_data = {'NLPyPort': [
    'config/*.properties',
    'TokPyPort/resources/**/*',
    'TagPyPort/resources/**/*',
    'LemPyPort/resources/**/*',
    'CRF/*.pickle',
    'CRF/trainedModels/*.pickle',
  ]},
  python_requires = '>=3.8',
  version = '2.3.0',      # Start with a small number and increase it with every change you make
  license='cc0-1.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python NLP for Portuguese',   # Give a short description about your library
  author = 'Joao Ferreira',                   # Type in your name
  author_email = 'jdhtml5@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jdportugal/NLPyPort',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jdportugal/NLPyPort',    # I explain this later on
  keywords = ['NLP', 'PORTUGUESE', 'PYTHON'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
         "nltk>=3.4.5",
"pandas",
"sklearn-crfsuite",
"xmltodict",

      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: 3.14',
  ],
)