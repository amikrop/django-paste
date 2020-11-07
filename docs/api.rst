API
===

Endpoints
---------

.. confval:: /

   *Snippet list*

   :GET: List viewable snippets
   :POST: Create new snippet

.. confval:: /{snippet-id}/

   *Snippet detail*

   :GET: View queried snippet
   :PUT: Update queried snippet
   :PATCH: Partially update queried snippet
   :DELETE: Delete queried snippet

.. confval:: /user/{user-id}/

   *User snippet list*

   :GET: List queried user's viewable snippets

.. confval:: /{snippet-id}/highlight/

   *Snippet highlight*

   :GET: View an HTML page of queried snippet's highlighted content

Content Types
-------------

The API can parse data of the following content types:

    - application/json
    - application/x-www-form-urlencoded
    - multipart/form-data

It can render its responses in the following formats:

    - application/json
    - text/html

A client can request the response in a specific format either by sending an
``Accept`` header, or by appending ``.json`` or ``.api`` to the URL, for JSON
and HTML content, respectively.
