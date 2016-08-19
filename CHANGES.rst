6.0.0
-----

* When resolving a repository scheme, the default command is now
  ``hg debugexpandscheme``, as that's the official command that
  is included with Mercurial 3.8.

  For compatibility with the previous behavior, set
  ``SCHEME_EXPAND_COMMAND=hg expand-scheme`` in the
  environment.

5.3.0
-----

* #201 Add support for NewRelic

5.0.1
-----

* Additional model garbage collection to troubleshoot memory leak in UI.

5.0.0
-----

* Removed dependency on Flower. Deployments should include
  the Flower dependency in their deployment if they wish
  to provide that service.
