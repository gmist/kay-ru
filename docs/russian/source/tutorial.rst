==============
Введение в Kay
==============

Подготовка
-----------

Инсталируйте следующие зависимости::

  * Python-2.5
  * App Engine SDK/Python
  * Kay Framework
  * ipython (рекомендуется)

Если вы инсталируете python25 из macports, вы также должны установить::

  * py25-hashlib
  * py25-socket-ssl
  * py25-pil
  * py25-ipython (рекомендуется)

Если вы хотите забирать Kay из репозитория, вы должны установить mercurial::

  * mercurial

Получить исходные тексты Kay из репозитория можно следующим образом:

.. code-block:: bash

  $ hg clone https://kay-framework.googlecode.com/hg/ kay

Если вы хотите использовать стабильную версию Kay, вы можете скачать
ее в виде архива по следующей ссылке:
http://code.google.com/p/kay-framework/downloads/list и затем распаковать ее:

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz

.. Note::
    В этом руководстве используются примеры с использованием Kay-0.10.0
    или выше.Следовательно, для того, чтобы примеры работали,
    вы также должны использовать Kay-0.10.0 или выше
    (например, последнюю версию из репозитория).

Если вы инстталировали App Engine SDK из zip архива,
то вам необходимо создать символьную ссылку на него следующим образом:

.. code-block:: bash

   $ sudo ln -s /some/whare/google_appengine /usr/local/google_appengine

Если вы устанавливали App Engine SDK с помощью инсталятора,
то создавать символьную ссылку не нужно.

Быстрый страрт
--------------

Создание нового проекта
=======================

Для создания нового проекта, вы можете использовать скрипт ``manage.py``,
который используется в Kay для создания скелета вашего проекта.
Кроме создания нового проекта, вы можете использовать этот скрипт
для управления этим проектом (включая развертывание, тестирование,
создание i18n переводов и т.д и т.п.).


.. code-block:: bash

   $ python kay/manage.py startproject myproject
   $ tree myproject
   myproject
   !-- app.yaml
   !-- kay -> /Users/tmatsuo/work/tmp/kay/kay
   !-- manage.py -> /Users/tmatsuo/work/tmp/kay/manage.py
   !-- settings.py
   `-- urls.py

   1 directory, 4 files

.. Note::

	На платформах, которые поддерживают символьные ссылки, директория
	``kay`` и файл ``manage.py`` будут созданы в виде этих ссылок.


Создание приложения
=======================
Используя Kay необходимо создать по крайне мере одно приложение в вашем 
проекте.

Перейдите в только что созданную директорию проекта ``myproject`` и
создайте ваше первое приложение. В приведенном ниже примере, создаваемое 
приложение называется ``myapp``.

.. code-block:: bash

   $ cd myproject
   $ python manage.py startapp myapp
   $ tree myapp
   myapp
   !-- __init__.py
   !-- models.py
   !-- templates
   !   `-- index.html
   !-- urls.py
   `-- views.py

   1 directory, 5 files

После создания приложения, вам необходимо отредактировать файл ``settings.py``
для того, чтобы зарегистрировать созданное приложение в проекте.

Для начала добавьте ``myapp`` в кортеж ``settings.INSTALLED_APPS``. При
необходимости вы можете изменить URL для этого приложения изменив словарь
``APP_MOUNT_POINTS``. В приведенном ниже примере показано, как привязать
ваше приложение к URL '/'.

settings.py

.. code-block:: python

  #$/usr/bin/python
  #..
  #..

  INSTALLED_APPS = (
    'kay.auth',
    'myapp',
  )

  APP_MOUNT_POINTS = {
    'myapp': '/',
  }

Если не изменять настройку ``APP_MOUNT_POINTS``, то приложение будет
привязано к URL, который будет выглядеть как название приложения ``/myapp``.

В приведенном выше примере, как вы видите, мы добавили еще одно приложение
с именем ``kay.auth``, которое мы будем использовать в дальнейшем.


Запуск вашего приложения
========================

Давайте запустим ваше первое приложение. Вы можете запустить сервер
разработки следующей командой.

.. code-block:: bash

  $ python manage.py runserver
  INFO     2009-08-04 05:48:21,339 appengine_rpc.py:157] Server: appengine.google.com
  ...
  ...
  INFO     ... Running application myproject on port 8080: http://localhost:8080

Вы увидите просто 'Hello' в вашем браузере, если зайдете по адресу
http://localhost:8080/.


Развертывание
=============

Перед тем как погрузится в код, давайте развернем проект на appspot.
Сначала вы должны отредактировать ``app.yaml`` и указать идентификатор
вашего приложения (``appid``) в переменной ``application``. После этого
выполните следующую команду.

.. code-block:: bash

  $ python manage.py appcfg update

В процессе развертывания у вас будет запрошены имя пользователя и пароль,
пожалуйста введите их, чтобы подтвердить ваши полномочия. После окончания
развертывания вы можете получить доступ к приложению по
адресу http://your-appid.appspot.com/.



Быстрый обзор сгенерированного каркаса приложения
-------------------------------------------------

myapp/urls.py
=============

Первым делом рассмотрим сгенерированный файл ``urls.py``. В нем вы можете 
конфигурировать отображение между URLs и представлениями.

myapp/urls.py:

.. code-block:: python

   from kay.routing import (
     ViewGroup, Rule
   )

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]

В строке начинающейся с ``Rule``, создается отображение 
'/' -> 'myapp.views.index'


myapp/views.py
==============

Предназначен для описание логики приложения.

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   myapp.views
   """

   """
   import logging

   from google.appengine.api import users
   from google.appengine.api import memcache
   from werkzeug import (
     unescape, redirect, Response,
   )
   from werkzeug.exceptions import (
     NotFound, MethodNotAllowed, BadRequest
   )

   from kay.utils import (
     render_to_response, reverse,
     get_by_key_name_or_404, get_by_id_or_404,
     to_utc, to_local_timezone, url_for, raise_on_dev
   )
   from kay.i18n import gettext as _
   from kay.auth.decorators import login_required

   """

   from kay.utils import render_to_response


   # Create your views here.

   def index(request):
     return render_to_response('myapp/index.html', {'message': 'Hello'})

В начале этого файла есть импорт часто используемых модулей и вы можете 
копировать/вставлять/удалять эти строки при необходимости. 
Также в файле присутствуют функция представления index().

В основном, используя Kay, вы должны писать функции для описания логики 
приложения, но в приципе представление может быть объектом, 
который имеет метод __call__() (т.е. вызываемый объект или callable object). 
Но в этом руководстве мы будем использовать только функции.

index(request):
	Функции представления всегда должны принимать объект ``Request`` 
	в качестве первого аргумента. В зависимости от условий функция
	представления может иметь дополнительные аргументы, но данная 
	функция index() их не имеет.

	Функции представления всегда должны возвращать объект ``Response``. 
	В этом примере, мы используем функцию ``render_to_response`` для 
	создания объекта ``Response`` из HTML шаблона и контекстных 
	переменных.


myapp/templates/index.html
==========================

Последним файлом является HTML шаблон.

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
   {{ message }}
   </body>
   </html>

В качестве движка шаблонов Kay использует jinja2. Для начала, пожалуйста, 
помните две вещи о jinja2:

* Для отображения контектных переменных, предаваемых из функции представления,
  необходимо расположить имя переменной внутри конструкции ``{{}}`` 
  (например, {{ my_message }}). Добавляя скобки ``()``, вы также можете 
  вызывать функции (и конечно, вы можете добавлять аргументы внутри скобок), 
  для того чтобы отобразить возвращаемый имим результат.

* Вы можете испльзовать ``{% %}`` как специальные теги для описания управления 
  структурами и команд jinja2, таких как 
  ``{% if ... %}`` {% else %} {% ... endif %}``, для циклов или для команд 
  расширения базового шаблона ``{% extends "base_template.html" %}``.


Вот пример спользования тэга ``{% if %}``.

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
   {% if message %}
     <div id="message">
       {{ message }}
     </div>
   {% endif %}
   </body>
   </html>

В приведенном выше примере, мы обернули блочный элемент div, содержащий 
код для отображения сообщения, тэгом {% if %}. В результате этот юлок и 
сообщение будет отображены только тогда, когда пременная ``message`` имеет 
какое-нибудь значение. 

Для начала, пожалуйста, запомните эти две синтаксические конструкции.

Аутентификация
--------------

Для того, чтобы включить фунцию аутентификации пользователей, вы должны 
установить соответствующее middleware для аутентификации. Kay поддерживает 
различные варианты аутентификации. В этом руководстве мы будем использовать 
вариант аутентификации черех Google аккаунт.

Конфигурация
=============

Для начала, вы должны добавить кортеж ``MIDDLEWARE_CLASES`` включая 
элемент ``kay.auth.middleware.AuthenticationMiddleware``.

.. code-block:: python

   MIDDLEWARE_CLASSES = (
     'kay.auth.middleware.AuthenticationMiddleware',
   )

Не забудьте запятую после элемента 
``kay.auth.middleware.AuthenticationMiddleware``, т.к. в кортеже из 
одного элемента требуется конечная запятая

После этого модуль аутентификации будет работать, но если вы хотите хранить 
дополнительную информацию о пользователе, то можно легко определить свою 
модель для хранеия этой дополнительной информации.

Если вы используете аутентификацию через учетную запись Google и при этом вы 
хотите определить собственную модель, то вам необходимо расширить класс 
``kay.auth.models.GoogleUser`` и указать эту модель в строковой переменной 
``settings.AUTH_USER_MODEL``

myapp.models:

.. code-block:: python

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser

   class MyUser(GoogleUser):
     pass

settings.py

.. code-block:: python

   AUTH_USER_MODEL = 'myapp.models.MyUser'


Как использовать
================

request.user
++++++++++++

После включения middleware аутентификации, оно добавит атрибут ``user`` 
в объект ``request``. Если пользователь посещающий сайты залогонился, то 
атрибут ``user`` будет содержать объект модели описывающей пользователя 
(например, объект MyUser), в противном случае атрибут ``user`` будет 
содержать экземпляр объекта ``kay.auth.models.AnonymousUser``.

Эти классы имеют следующие общие методы и атрибуты:

* is_admin
  
  Этот логический (булевый) атрибут указывает является ли пользователь
  администратором.

* is_anonymous()

  Этот метод возвращает False если пользователь аутентифицирован,
  в противном случае возвращается True

* is_authenticated()
  Этот метод возвращает True если пользователь аутентифицирован, иначе
  возвращается False.


Пример использования в шаблоне
++++++++++++++++++++++++++++++

Скажем, фрагмент кода наподобие нижеследующего.

.. code-block:: html

   <div id="greeting">
     {% if request.user.is_anonymous() %}
       <a href="{{ create_login_url() }}">login</a>
     {% else %}
       Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
     {% endif %}
   </div>

Этот кусок кода будет показывать ссылку на экран аутентификации, если 
пользователь не аутентифицирован, в противном случае будет отображена 
ссылка для выхода.

Декораторы
++++++++++

Для защиты страницы от анонимного доступа, вы можете использовать 
следующие декораторы:

* ``kay.auth.decorators.login_required``

  вы можете использовать этот декоратор для страниц, которые требуют
  авторизации пользователя.

* ``kay.auth.decorators.admin_required``
  
  этот декоратор вы можете использовать если страница имеет
  администраторские ограничения.


Например:

.. code-block:: python

   from kay.utils import render_to_response
   from kay.auth.decorators import login_required

   # Create your views here.

   @login_required
   def index(request):
     return render_to_response('myapp/index.html', {'message': 'Hello'})

В этом примере, при доступе к индексной странице, осуществляется проверка, 
вошли ли вы в систему.

Реализация гостевой книги - Шаг 1
---------------------------------

В этом уроке, мы создадим простейшую гостевую книгу. Мы будем использовать
различные подходы и функциональность для того, чтобы урок был максимально полным и 
всеобъемлющим.

Во-первых, давайте рассмотрим использование моделей и форм.

Определение модели
==================

Для определения модели, вы можете использовать db модуль AppEngine.
Кроме того, есть еще дополнительные свойства описанные в модуле ``kay.db``.

Это простая модель для гостевой книги, описывающая коментарий:

myapp/models.py:

.. code-block:: python

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser
   import kay.db

   # ...

   class Comment(db.Model):
     user = kay.db.OwnerProperty()
     body = db.TextProperty(required=True)
     created = db.DateTimeProperty(auto_now_add=True)

``kay.db.OwnerProperty`` который определен как атрибут ``user`` - это 
свойство специально предлагаемое Kay, которое предназначено для хранения
ключа пользователя, который определяется автоматически из атрибута 
request.user (если пользователь неаутентифицирован, то поле будет содержать
None).

Атрибут ``body`` предназначен для хранения тела коментария, а атрибут
``created`` предназначен для хранения даты/времени создания коментария и
создается автоматически (за это отвечает параметр auto_now_add равный True).


Определние формы
================

Далее, создадим форму для отправки коментариев. Конечно, вы можете написать
эту форму непосредственно в HTML шаблоне, но рекомендуется создавать формы
с использованием модуля ``kay.utils.forms``.

В принципе не существует никаких ограничений в том, где определять формы, например
файл ``myapp/forms.py`` может быть одним из таких мест.

myapp/forms.py:

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms

   class CommentForm(forms.Form):
     body = forms.TextField("Your Comment", required=True)

Вы можете определить форму, создав класс, который расширяет класс
``kay.utils.forms.Form``. В этом примере, ``body`` - это экземпляр класса
``form.TextFiled``. Первый аргумент - это метка поля генерируемой формы, 
которая будет представлена в виде соответсвующего HTML тэга <label>.
Если вы укажете параметр ``required`` равный True, то данное поле будет
обязательным для заполнения.

Для более детальной информации об этой билиотеке форм, пожалуйста, обратитесь к 
`описанию <http://kay-docs-jp.shehas.net/forms_reference.html>`_ 
``kay.utils.forms`` модуля.


Определение представления
=========================

Давайте напишем представление для вышериведенных модели и формы.

myapp/views.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   myapp.views
   """

   from werkzeug import redirect

   from kay.utils import (
     render_to_response, url_for
   )
   from kay.auth.decorators import login_required

   from myapp.models import Comment
   from myapp.forms import CommentForm

   # Create your views here.

   @login_required
   def index(request):
     form = CommentForm()
     if request.method == "POST" and form.validate(request.form):
       comment = Comment(body=form['body'])
       comment.put()
       return redirect(url_for('myapp/index'))
     return render_to_response('myapp/index.html',
			       {'form': form.as_widget()})

Вы можете видеть операторы импорта в четыерх линиях:
``werkzeug.redirect``, ``kay.utils.url_for`` и только что созданных
модели и формы. Вы можете увидеть, что это представлнеи создает форму
и проверяет значения формы, если request предается методом POST.

После успешной проверки данное представление создает новый объект
класса ``Comment`` и делает перенаправление на главную страницу.

``url_for`` - это функция для обратного поиска URL и возвращает этот
URL для конечной точки, которая передается в качестве аргумента. Теперь
давайте посмотрим на сгенерированыый по умолчанию файл ``urls.py``.

.. code-block:: python

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]

В ``urls.py`` мы устанавливаем 'index' как конечную точку. Конечно, когда
используется обратный поиск, то мы используем 'myapp/index'. Это необходимо
из-за того, что Kay автоматически добавляет в конечную точку названия приложений
и слэш. Это делается для избежания конфликтов между конечными точками различных
приложений и именно поэтому небходимо указывать конечную точку как 
``название_приложения/конечная_точка``.

Шаблон
======

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
     <div id="greeting">
       {% if request.user.is_anonymous() %}
	 <a href="{{ create_login_url() }}">login</a>
       {% else %}
	 Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
       {% endif %}
     </div>

     <div id="main_form">
       {{ form()|safe }}
     </div>
   </body>
   </html>

Теперь вы можете сохранять коментарии, отправленные из формы в хранилище.
Now you can store comments submitted from the form to the datastore.

Теперь давайте попробуем работу отправки коментариев на сервере разработки.
После отправки нескольких коментариев, вы можете зайти по адресу
http://localhost:8080/_ah/admin  для просмотра содержимого хранилища.

Тип называемый ``myapp_comment`` содержит объекты, которые вы только что создали.
Как вы видите, Kay добавляет имя приложения и знак подчеркивания '_' перед
именем класса и переводит имя в нижний регистр. Вы можете отключить это поведение,
установив параметр ``settings.ADD_APP_PREFIX_TO_KIND`` в значение False.


Реализация гостевой книги - Шаг 2
---------------------------------

В текущей реализации, если вы отсылаете коментарии, то вы не видите изменений.
Давайте добавим возможность отображения последних 20 коментариев на главной
странице.

Использование запросов
======================

myapp/views.py:

.. code-block:: python

   ITEMS_PER_PAGE = 20

   # Create your views here.

   @login_required
   def index(request):
     form = CommentForm()
     if request.method == "POST" and form.validate(request.form):
       comment = Comment(body=form['body'])
       comment.put()
       return redirect(url_for('myapp/index'))
     query = Comment.all().order('-created')
     comments = query.fetch(ITEMS_PER_PAGE)
     return render_to_response('myapp/index.html',
			       {'form': form.as_widget(),
				'comments': comments})

Этот код отсылает последние 20 коментариев в шаблон.

Цикл в шаблоне
==============

Теперь давайте добавим отображение этих коментариев в шаблоне.

myapp/templates/index.html:

.. code-block:: html

  {% if comments %}
    <div id="comment_list">
      <ul>
      {% for comment in comments %}
        <li>{{ comment.body }}
          <span class="author"> by {{ comment.user }}</span>
      {% endfor %}
      </ul>
    </div>
  {% endif %}

Пожалуйста, добавте этот код в описанный выше шаблон, сразу после части, которая
отображает форму. Теперь, обновив страницу, вы увидите последние 20 коментариев.

Реализация гостевой книги - Шаг 3
---------------------------------

Теперь давайте добавим возможность выбора категории из списка категорий, которые
будут пердварительно определены.


Использование ModelForm
=======================

Для начала, создадим модель для хранения категорий и добавим свойство для
категории в класс ``Comment``.

myapp/models.py:

.. code-block:: python

   class Category(db.Model):
     name = db.StringProperty(required=True)

     def __unicode__(self):
       return self.name

   class Comment(db.Model):
     user = kay.db.OwnerProperty()
     category = db.ReferenceProperty(Category, collection_name='comments')
     body = db.StringProperty(required=True, verbose_name=u'Your Comment')
     created = db.DateTimeProperty(auto_now_add=True)

Далее, поддержка обеих моделей и форм может быть немного громоздкой, поэтому вы
можете использовать возможность автоматического создания формы из сответсвующего
определения модели.

Для этого создайте класс формы расширяющий класс
``kay.utils.forms.modelform.ModelForm``.

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms
   from kay.utils.forms.modelform import ModelForm

   from myapp.models import Comment

   class CommentForm(ModelForm):
     class Meta:
       model = Comment
       exclude = ('user', 'created')

Во-первых, вы дожны определить класс расширяющий класс ``ModelForm`` и 
внутри этого класса определите внутренний класс с именем ``Meta``. У этого 
класса есть несколько атрибутув, предназначенных для конфигурации вашей
ModelForm:

* model
  определяет класс модели, на которой будет основываться новая форма.

* exclude
  
  кортеж, который определяет свойства, которые вы хотели бы исключить из формы.
  define properties which you want to exclude from a form as
  tuple. Этот атрибут ``exclude`` и следующий атрибут ``fields`` являются
  взаимно эксклюзивными, т.е. вы можете определить только один из них.

* fields
  кортеж, который предназначен для свойств модели, которые вы бы хотели 
  включить в форму.

* help_texts
  
  определяет тексты-подсказки, которые будут отображаться в форме. Описывается в
  виде словаря, ключами которого являются имена полей заданной модели.

И наконец нужно изменить способ сохранения объекта в функции представления в
``myapp/vews.py``.

.. code-block:: python

       comment = Comment(body=form['body'])
       comment.put()

Замените указанные выше строчки кода следующей строкой:

.. code-block:: python

       comment = form.save()


Пользовательские скрипты управления
===================================

Теперь, вы можете видеть форму для выбора категории, но она не содержит объеков
Category в хранилище данных и именно поэтому в выпадающем списке нет ни одной
позиции для выбора. Давайте теперь создадим пользовательскй скрипт управления,
который добавит категории в хранилище.

Пожалуйста, добавьте файл с названием ``myapp/management.py`` со следующим кодом.

.. code-block:: python

   # -*- coding: utf-8 -*-

   from google.appengine.ext import db

   from kay.management.utils import (
     print_status, create_db_manage_script
   )
   from myapp.models import Category

   categories = [
     u'Programming',
     u'Testing',
     u'Management',
   ]

   def create_categories():
     entities = []
     for name in categories:
       entities.append(Category(name=name))
     db.put(entities)
     print_status("Categories are created successfully.")

   def delete_categories():
     db.delete(Category.all().fetch(100))
     print_status("Categories are deleted successfully.")

   action_create_categories = create_db_manage_script(
     main_func=create_categories, clean_func=delete_categories,
     description="Create 'Category' entities")

После этого, вы можете видеть следующие записи в выводе команды
``manage.py``::

  create_categories:
    Create 'Category' entities

    -a, --appid                   string
    -h, --host                    string
    -p, --path                    string
    --no-secure
    -c, --clean

Вы можете добавить 3 объекта класс ``Category`` следующим образом:

* на appspot

.. code-block:: bash

  $ python manage.py create_categories

* на devserver

.. code-block:: bash

  $ python manage.py create_categories -h localhost:8080 --no-secure

Пожалуйста добавьте эти 3 объекта ``Category`` и обновите старницу вышего приложения. Теперь вы видите 3 варинта выбора в выпадающем списке?

.. Note::
   Для более детальной информации о том, как создавать пользовательские 
   скрипты управления обратитесь к `Adding your own management script
   <http://kay-docs.shehas.net/manage_py.html#adding-your-own-management-script>`_


Displaying category
===================

The code bellow allows you to show categories on the comment list page.

.. code-block:: python

     {% if comments %}
       <div id="comment_list">
	 <ul>
	 {% for comment in comments %}
	   <li>{{ comment.body }}
	     <span class="author"> by {{ comment.user }}</span>
	     {% if comment.category %}
	       <br>
	       <span class="category"> in {{ comment.category.name }}</span>
	     {% endif %}
	 {% endfor %}
	 </ul>
       </div>
     {% endif %}


Automatic CRUD creation
=======================

Let's create pages for managing the categories. Here, we're gonna
create pages for adding/deleting/modifying categories restricted only
to admins.

First, create a form for ``Category``.

myapp/forms.py:

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms
   from kay.utils.forms.modelform import ModelForm

   from myapp.models import (
     Comment, Category
   )

   class CommentForm(ModelForm):
     class Meta:
       model = Comment
       exclude = ('user', 'created')

   class CategoryForm(ModelForm):
     class Meta:
       model = Category

Import ``Category`` and create a new form named ``CategoryForm``.

Next, edit ``myapp/urls.py`` as follows:

.. code-block:: python

   from kay.generics import admin_required
   from kay.generics import crud
   from kay.routing import (
     ViewGroup, Rule
   )

   class CategoryCRUDViewGroup(crud.CRUDViewGroup):
     model = 'myapp.models.Category'
     form = 'myapp.forms.CategoryForm'
     authorize = admin_required

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     ),
     CategoryCRUDViewGroup(),
   ]

Lastly, add ``kay.utils.flash.FlashMiddleware`` to
``settings.MIDDLEWARE_CLASSES`` as follows:

.. code-block:: python

   MIDDLEWARE_CLASSES = (
     'kay.auth.middleware.AuthenticationMiddleware',
     'kay.utils.flash.FlashMiddleware',
   )

You can see a list of categories at: http://localhost:8080/category/list

.. Note::

   For more details about CRUD creation, refer to `Using generic view
   groups <http://kay-docs.shehas.net/generic_views.html>`_.


Cascade deletion with db_hook
=============================

As you may notice, if you delete a category which has one or more
comments in it, an error occurs when displaying those comments.

Here, we will use ``db_hook`` feature for implementing cascade
deletion.

If you got the error I mentioned above, please delete comments in
question, or stop a development server once, and restart it with
``-c`` option, and create desired entities again before going further.

First, you need to enable ``db_hook`` feature in the ``settings.py``.

.. code-block:: python

   USE_DB_HOOK = True

Next, register your hook function in ``myapp/__init__.py`` as follows:

myapp/__init__.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   # Kay application: myapp

   from google.appengine.ext import db

   from kay.utils.db_hook import register_pre_delete_hook

   from myapp.models import (
     Comment, Category
   )

   def cascade_delete(key):
     entities = Comment.all(keys_only=True).filter('category =', key).fetch(2000)
     db.delete(entities)

   register_pre_delete_hook(cascade_delete, Category)

In above example, cascade deletion is implemented in a very ad-hoc
way, so you might need to implement it more carefully if in production
code.

Then, if you delete any category, all the comments that belongs to the
category should be deleted.

.. Note::

   For more details about db_hook feature, refer to `Using db_hook
   feature <http://kay-docs.shehas.net/db_hook.html>`_.

