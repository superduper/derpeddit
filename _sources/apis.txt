API Reference
=============

-------------------
General information
-------------------

API Endpoint
~~~~~~~~~~~~

API Server URL: https://derpeddit.heroku.com

Validation Errors
~~~~~~~~~~~~~~~~~

Invalid field value
   In cases when an invalid value specified for a field, or field is missing in supplied payload 

   **Example**:

   .. sourcecode:: http

     HTTP/1.1 400 BAD REQUEST

     {"password": ["This field is required."]}


Non-field errors
   In cases when payload was correct, but some constraint has been violated 

   **Example**:

   .. sourcecode:: http

     HTTP/1.1 401 UNAUTHORIZED 

     {"non_field_errors": "Login and password do not match"}




Invalid payload
   In cases when an invalid JSON payload supplied

   **Example**:

   .. sourcecode:: http

     HTTP/1.1 400 BAD REQUEST

     {"detail": "JSON parse error - Expecting ',' delimiter: line 1 column 19 (char 18)"}


-------------------------------
Authentication and registration
-------------------------------

Derpeddit uses **cookie based** authentication. In order to get auth cookie, you have to log in first.

Registration
~~~~~~~~~~~~

.. http:post:: /api/v1/core/auth/signup

   Registers a new user 

   :jsonparam string login: password 
   :jsonparam string password: password
   :jsonparam string name: users last name

   :reqheader Content-type: mandatory header, must be `application/json`
   :statuscode 201: user created

Logging in
~~~~~~~~~~

.. http:post:: /api/v1/core/auth/login

   Authenticates user against `login` and `password`.

   Before you can log in you'll have to sign up. 

   :jsonparam string login: login 
   :jsonparam string password: password

   :reqheader Content-type: mandatory header, which must be `application/json`
   
   **Example request**:

   .. sourcecode:: http

     POST /api/v1/core/auth/login HTTP/1.1
     Host: derpeddit.herokuapp.com
     Content-Type: application/json;charset=UTF-8

     {"username":"foo","password":"bar"}

   **Example response - incorrect login and password**:

   .. sourcecode:: http

     HTTP/1.1 401 UNAUTHORIZED
     Content-Type: application/json
          
     {"non_field_errors": "Login and password do not match"}


Logging out
~~~~~~~~~~~

.. http:post:: /api/v1/core/auth/logout

   De-authenticates user 


Current user profile
~~~~~~~~~~~~~~~~~~~~

.. http:get:: /api/v1/core/auth/profile

   Returns current user profile 

-----
Posts
-----

Get all posts
~~~~~~~~~~~~~

.. http:get:: /api/v1/posts

   Returns all posts
   :param string mode: to sort posts by vote score - `top`, to sort by create time - `newest`


Create a new post
~~~~~~~~~~~~~~~~~

.. http:post:: /api/v1/posts

   Creates a news :term:`post` 

   :jsonparam string title: Post title
   :jsonparam string link: URL if its a "Link post"
   :jsonparam string text: text if its a "Text post" 


Upvote a post
~~~~~~~~~~~~~

.. http:put:: /api/v1/posts/(post_id)/vote

   Creates a news :term:`post` 

   :arg number post_id: Post id
   :jsonparam bool positive: must be true 


Downvote a post
~~~~~~~~~~~~~~~

.. http:put:: /api/v1/posts/(post_id)/vote

   Creates a news :term:`post` 

   :arg number post_id: Post id
   :jsonparam bool negative: must be true 


Get post comments
~~~~~~~~~~~~~~~~~

.. http:get:: /api/v1/posts/(post_id)/comment

   Creates a news :term:`post` 

   :arg number post_id: Post id
   :jsonparam bool positive: must be true 


Make a new comment on a post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:post:: /api/v1/posts/(post_id)/comment

   Creates a news :term:`post` 

   :arg number post_id: Post id
   :jsonparam string text: comment text
