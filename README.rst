Starred
=======

.. image:: https://travis-ci.org/1132719438/starred.svg?branch=master
    :target: https://travis-ci.org/1132719438/starred
    :alt: Travis CI Status

.. image:: https://requires.io/github/1132719438/starred/requirements.svg?branch=master
     :target: https://requires.io/github/1132719438/starred/requirements/?branch=master
     :alt: Requirements Status

Install
-------

starred requires Python version 3.x

.. code:: bash

    $ git clone https://github.com/1132719438/starred
    $ pip3 install ./starred
    $ starred --username 1132719438 --output README.md


Highlight
---------

#. Output your starred repositories in table or list

   - Output table(default)

    .. code:: bash

        starred --username <yourname> --output README.md [--type table]

   - Output list

    .. code:: bash

        starred --username <yourname> --output README.md --type list

#. Nice badges for total number of repositories and generated date

   See `Stars <https://github.com/1132719438/Stars>`__

#. Repositories can be sort by stars, starred date or name

   .. code:: bash

    starred --username <yourname> --output README.md --sort stars/date/name

#. Automatically create a repository for your stars, and update this
   repository when your stars changed, old stars will be archived.
   Your can install `starred`, use scheduled tasks to automatically
   update your stars repository.

   - Synology NAS: use `Task Scheduler` to run following script

    .. code:: bash

        LANG=en_US.UTF-8 GITHUB_TOKEN=<yourtoken> starred --username <yourname> --repository <repositoryname>

   - Linux: use `crontab` to run following script

    .. code:: bash

        export GITHUB_TOKEN=<yourtoken>
        starred --username <yourname> --repository <repositoryname>

   - Windows: use `Task Scheduler <https://www.ibm.com/support/knowledgecenter/en/SSZRWV_9.1.5/com.ibm.dc.develop.doc/dcdev474.htm>`__ to run following script (Anaconda3 needed)

    .. code:: bash

        @echo off
        C:\Users\<user>\AppData\Local\Continuum\anaconda3\Scripts\activate.bat C:\Users\<user>\AppData\Local\Continuum\anaconda3 & set GITHUB_TOKEN=<yourtoken> & starred --username <yourname> --repository <repositoryname>


Usage
-----

.. code:: bash

    $ starred --help

    Usage: starred [OPTIONS]

      GitHub starred

      creating your own Awesome List used GitHub stars!

      example:     starred --username 1132719438 --output README.md

    Options:
      --username TEXT           GitHub username  [required]
      --token TEXT              GitHub token
      --sort [stars|date|name]  sort by language with stars, date or name
      --repository TEXT         repository name
      --message TEXT            commit message
      --output TEXT             output file name with path(print to stdout if not
                                set)
      --http-proxy TEXT         http proxy (i.e. http://127.0.0.1:1080 or
                                socks5://127.0.0.1:1080)
      --https-proxy TEXT        https proxy (same as http proxy if not set)
      --launch                  launch to Github after update repository
      --type [table|list]       output repository information in table or list

Demo
----

.. code:: bash

    # automatically create the repository
    $ export GITHUB_TOKEN=<yourtoken>
    $ starred --username <yourname> --repository <repositoryname>

-  `Stars <https://github.com/1132719438/Stars>`__

FAQ
---

#. Generate new token

   goto `Personal access tokens <https://github.com/settings/tokens>`__

#. Why do I need a token?

   -  For unauthenticated requests, the rate limit is 60 requests per
      hour.
      see `Rate
      Limiting <https://developer.github.com/v3/#rate-limiting>`__
   -  The token must be passed together when you want to automatically
      create the repository.

