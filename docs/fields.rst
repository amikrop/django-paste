Fields
======

The following fields of snippets have a value automatically generated for them
and hence clients are not supposed to explicitly provide them:

    - :confval:`id`
    - :confval:`created`
    - :confval:`updated`
    - :confval:`owner`

The rest of the fields are optional, except for :confval:`content`.

.. confval:: id

   :type: number
   :read only: yes

   The snippet's primary key in the database.

.. confval:: content

   :type: string
   :required: yes

   The source code of the snippet.

.. confval:: language

   :type: string

   The programming language of the snippet. Must be a valid Pygments lexer
   name.

.. confval:: style

   :type: string

   The style the snippet should be highlighted with. Must be a valid Pygments
   style name.

.. confval:: line_numbers

   :type: boolean
   :default: *from settings*

   Whether line numbers should be shown in the snippet's highlight view.

.. confval:: embed_title

   :type: boolean
   :default: *from settings*

   Whether the title of the snippet should be included in its highlight view.

.. confval:: private

   :type: boolean
   :default: *from settings*

   Whether the snippet should be only viewable by its owner and staff users.

.. confval:: created

   :type: string
   :read only: yes

   The datetime of the snippet's creation.

.. confval:: updated

   :type: string
   :read only: yes

   The datetime of the snippet's last modification.

.. confval:: owner

   :type: number / null
   :read only: yes

   The primary key in the database of the user who created the snippet. If
   that user was unauthenticated, this field is null.
