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

   :jsonparam string username: password 
   :jsonparam string password: password

   :reqheader Content-type: mandatory header, must be `application/json`
   :statuscode 201: user created

   **Example request**:
 
   .. sourcecode:: http

      POST /api/v1/core/auth/signup HTTP/1.1
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 55
      Content-Type: application/json; charset=utf-8
      Host: derpeddit.herokuapp.com
      
      {
          "password": "derpedditftw",
          "username": "derpedditor"
      }


   **Example response**:
 
   .. sourcecode:: http

      HTTP/1.1 201 CREATED
      Allow: POST, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 05:57:32 GMT
      Server: gunicorn/19.1.0
      Set-Cookie: sessionid=38l4ehqzjq6cz1tbtus22dowdkqge753; expires=Mon, 18-Aug-2014 05:57:32 GMT; httponly; Max-Age=1209600; Path=/
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "id": 2,
          "username": "derpedditor"
      }


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
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 55
      Content-Type: application/json; charset=utf-8
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      
      {
          "password": "derpedditftw",
          "username": "derpedditor"
      }

   **Example response - incorrect login and password**:

   .. sourcecode:: http

      HTTP/1.1 401 UNAUTHORIZED
      Content-Type: application/json
           
      {"non_field_errors": "Login and password do not match"}

   **Example response - correct login and password**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: POST, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 06:04:58 GMT
      Server: gunicorn/19.1.0
      Set-Cookie: sessionid=zjherkdqlx9byq1o4lvlh2hil05siafc; expires=Mon, 18-Aug-2014 06:04:58 GMT; httponly; Max-Age=1209600; Path=/
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "id": 2,
          "username": "derpedditor"
      }

Logging out
~~~~~~~~~~~

.. http:post:: /api/v1/core/auth/logout

   De-authenticates current user 

   **Example request**:

   .. sourcecode:: http

      POST /api/v1/core/auth/logout HTTP/1.1
      Accept: */*
      Accept-Encoding: gzip, deflate
      Content-Length: 0
      Cookie:  sessionid=qn010o0pgx75qbz1umvo15hxc425nep5
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: POST, OPTIONS
      Connection: keep-alive
      Date: Mon, 04 Aug 2014 06:22:07 GMT
      Server: gunicorn/19.1.0
      Set-Cookie: sessionid=uvg092xpk5g50aeuhqn5nfec0t3mvnxv; expires=Mon, 18-Aug-2014 06:22:07 GMT; httponly; Max-Age=1209600; Path=/
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur



Current user profile
~~~~~~~~~~~~~~~~~~~~

.. http:get:: /api/v1/core/auth/profile

   Returns current user profile 

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/core/auth/profile HTTP/1.1
      Accept: */*
      Accept-Encoding: gzip, deflate
      Cookie:  sessionid=qn010o0pgx75qbz1umvo15hxc425nep5
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: GET, HEAD, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 06:03:50 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "id": 2,
          "username": "derpedditor"
      }

-----
Posts
-----

Get all posts
~~~~~~~~~~~~~

.. http:get:: /api/v1/posts

   Returns all posts
   :param string mode: to sort posts by vote score - `top`, to sort by create time - `newest`


   **Example request**:

   .. sourcecode:: http

      GET /api/v1/posts HTTP/1.1
      Accept: */*
      Accept-Encoding: gzip, deflate
      Cookie:  sessionid=kku4ymfeacxkknxbcma7yc0m9e1jz3bb
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0

   **Example response**:

   .. sourcecode:: http


      HTTP/1.1 200 OK
      Allow: GET, POST, HEAD, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 07:23:45 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      [
          {
              "comments_total": 0,
              "created": "2014-08-04T07:21:18.868Z",
              "id": 3,
              "link": "http://google.com",
              "owner": {
                  "id": 2,
                  "username": "derpedditor"
              },
              "score": 1,
              "text": null,
              "title": "yawn"
          },
          {
              "comments_total": 0,
              "created": "2014-08-04T07:20:55.254Z",
              "id": 2,
              "link": "http://bing.com",
              "owner": {
                  "id": 2,
                  "username": "derpedditor"
              },
              "score": 1,
              "text": null,
              "title": "ayawn"
          }
      ]


Create a new post
~~~~~~~~~~~~~~~~~

.. http:post:: /api/v1/posts

   Creates a news :term:`post` 

   :jsonparam string title: Post title
   :jsonparam string link: URL if its a "Link post"
   :jsonparam string text: text if its a "Text post" 

   **Example request**:

   .. sourcecode:: http

      POST /api/v1/posts HTTP/1.1
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 46
      Content-Type: application/json; charset=utf-8
      Cookie:  sessionid=kku4ymfeacxkknxbcma7yc0m9e1jz3bb
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      
      {
          "link": "http://google.com",
          "title": "yawn"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 CREATED
      Allow: GET, POST, HEAD, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 07:21:18 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "link": "http://google.com",
          "text": null,
          "title": "yawn"
      }


Upvote a post
~~~~~~~~~~~~~

.. http:put:: /api/v1/posts/(post_id)/vote

   Votes +1 post

   :arg number post_id: Post id
   :jsonparam bool positive: must be true 

   **Example request**:

   .. sourcecode:: http

      PUT /api/v1/posts/2/vote HTTP/1.1
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 18
      Content-Type: application/json; charset=utf-8
      Cookie:  sessionid=kku4ymfeacxkknxbcma7yc0m9e1jz3bb
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      
      {
          "positive": true
      }
      
   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: PUT, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 07:30:19 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "new_post_score": 1
      }



Downvote a post
~~~~~~~~~~~~~~~

.. http:put:: /api/v1/posts/(post_id)/vote

   Votes -1 a :term:`post` 

   :arg number post_id: Post id
   :jsonparam bool negative: must be true 

   **Example request**:

   .. sourcecode:: http

      PUT /api/v1/posts/2/vote HTTP/1.1
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 18
      Content-Type: application/json; charset=utf-8
      Cookie:  sessionid=kku4ymfeacxkknxbcma7yc0m9e1jz3bb
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      
      {
          "negative": true
      }
      
   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: PUT, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 07:30:19 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "new_post_score": 0
      }

Get post comments
~~~~~~~~~~~~~~~~~

.. http:get:: /api/v1/posts/(post_id)/comment

   Returns all comments left for term:`post` 

   :arg number post_id: Post id

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/posts/2/comment HTTP/1.1
      Accept: */*
      Accept-Encoding: gzip, deflate
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Allow: GET, POST, HEAD, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 08:01:32 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      [
          {
              "created": "2014-08-04T07:59:53.763Z",
              "id": 2,
              "owner": {
                  "id": 2,
                  "username": "derpedditor"
              },
              "post": 2,
              "text": "huh?"
          },
          {
              "created": "2014-08-04T07:59:43.340Z",
              "id": 1,
              "owner": {
                  "id": 2,
                  "username": "derpedditor"
              },
              "post": 2,
              "text": "meh"
          }
      ]


Make a new comment on a post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:post:: /api/v1/posts/(post_id)/comment

   Makes a new comments for a term:`post` 

   :arg number post_id: Post id
   :jsonparam string text: comment text

   **Example request**:

   .. sourcecode:: http

      POST /api/v1/posts/2/comment HTTP/1.1
      Accept: application/json
      Accept-Encoding: gzip, deflate
      Content-Length: 16
      Content-Type: application/json; charset=utf-8
      Cookie:  sessionid=kku4ymfeacxkknxbcma7yc0m9e1jz3bb
      Host: derpeddit.herokuapp.com
      User-Agent: HTTPie/0.8.0
      
      {
          "text": "huh?"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 CREATED
      Allow: GET, POST, HEAD, OPTIONS
      Connection: keep-alive
      Content-Type: application/json
      Date: Mon, 04 Aug 2014 07:59:53 GMT
      Server: gunicorn/19.1.0
      Transfer-Encoding: chunked
      Vary: Accept, Cookie
      Via: 1.1 vegur
      
      {
          "created": "2014-08-04T07:59:53.763Z",
          "id": 2,
          "owner": {
              "id": 2,
              "username": "derpedditor"
          },
          "post": 2,
          "text": "huh?"
      }
      
