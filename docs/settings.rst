Settings
========

.. note::
   Every time you change settings related to the database, you should then
   generate and run database migrations.

All the settings of *django-admin* have default values, which can get
overriden. This is done by defining a ``PASTE`` dict in your Django project's
settings file, whith any of the following keys:

.. confval:: DEFAULT_EMBED_TITLE

   :type: ``bool``
   :default: ``True``

   Whether the title of a snippet should be included in its highlight view, in
   case the relative field is not set for it.

.. confval:: DEFAULT_LANGUAGE

   :type: ``str``
   :default: ``'text'``

   The Pygments lexer name (programming language) used for the highlighting of
   a snippet, in case the relative field is not set for it, and the
   :confval:`GUESS_LEXER` setting is ``False``.

.. confval:: DEFAULT_LINE_NUMBERS

   :type: ``bool``
   :default: ``True``

   Whether line numbers should be shown in a snippet's highlight view, in case
   the relative field is not set for it.

.. confval:: DEFAULT_PRIVATE

   :type: ``bool``
   :default: ``False``

   Whether a snippet should be only viewable by its owner and staff users, in
   case the relative field is not set for it.

.. confval:: DEFAULT_STYLE

   :type: ``str``
   :default: ``'default'``

   The Pygments style for the highlighting of a snippet, in case the relative
   field is not set for it.

.. confval:: FORBID_ANONYMOUS

   :type: ``bool``
   :default: ``False``

   Whether to forbid any API access to unauthenticated users.

.. confval:: FORBID_ANONYMOUS_CREATE

   :type: ``bool``
   :default: ``False``

   Whether to forbid snippet creation to unauthenticated users.

.. confval:: FORBID_ANONYMOUS_LIST

   :type: ``bool``
   :default: ``False``

   Whether to forbid snippet listing to unauthenticated users.

.. confval:: FORBID_LIST

   :type: ``bool``
   :default: ``False``

   Whether to forbid snippet listing to non-staff users.

.. confval:: GUESS_LEXER

   :type: ``bool``
   :default: ``True``

   Whether to let Pygments guess a lexer for the highlighting of a snippet, in
   case the ``language`` field is not set for it. If this setting is ``False``
   and a language is not set for a snippet, the :confval:`DEFAULT_LANGUAGE`
   setting is considered for its highlighting.

.. confval:: TITLE_MAX_LENGTH

   :type: ``int``
   :default: ``100``

   The maximum character length for the ``title`` field of snippets.
