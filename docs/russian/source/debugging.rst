=======
Отладка
=======

Отладчик werkzeug
=================

Kay имеет интегрированный отладчик werkzeug's и используется по умолчанию
в локальном сервере разработки. К сожалению, он не может быть использован
на стороне сервера AppEngine.

Этот отладчик работает в браузере разработчика и запускается когда какое-либо
приложение бросает исключение, которое затем не перехватывается. Вы можете
использовать интерактивную консоль и просматривать исходный код на каждом шаге
трассировки стека вызовов.

Кроме того, вы также можете видеть трассировку стека в виде простого текста
при хостинге вышего сервиса в сети Интернет.


Отображеие отладчика
--------------------

При разработке, после броска исключения, вы можете увидеть следующий экран:

.. image:: images/debugger.png
   :scale: 80

На котором отображены строчки исходного кода и стек вызова. В правой части,
когда вы наведете курсор "мыши" на строку с исходным кодом, появятся
следующие иконки::

.. image:: images/debugger-icons.png

Если вы кликните по левой иконке, то появится интерактивная консоль. Если вы
кликните по правой иконке, то вы увидите исходный код и подсвеченной линией,
в которой возникло исключение.


Интерактивная консоль
---------------------

Это скриншот интерактивной консоли.

.. image:: images/debugger-console-startup.png
   :scale: 80

В этой консоли вы можете выполнять любой код на python. Очень полезно то, что
этот код будет выполнени внутри фрейма информации на момент возникновения
исключения.

Например, выполните ``locals()`` и вы получите словарь с локальными
переменными.

.. code-block:: python

  [console ready]
  >>> locals()
  {'request': <Request 'http://localhost:8080/' [GET]>}
  >>>

Исправление опечатки и перезапуск вашего кода даст вам правильный результат.

.. code-block:: python

  [console ready]
  >>> comments = Comment.all().order('-created').fetch(100)
  >>> comments
  [<myapp.models.Comment object at 0x104c6c8d0>]
  >>> 

Если вы кликните по иконке еще раз, то вы скроете интерактивную консоль.


Просмотр исходного кода
-----------------------

Это исходный код вызвавший исключение. Линия вызвашая это исключение
подсвечена.

.. image:: images/debugger-view-source.png
   :scale: 80

Есои вы снова кликните по заголовку ``View Source``, то вы скроете окно с
исходным кодом.


Просмотр стека вызовов в виде простого текста
---------------------------------------------

Если вам нужно вставить стек вызовов в e-mail или сделать еще что-то подобное,
то вы можете кликнуть по загловку ``Traceback`` как показано ниже:

.. image:: images/debugger-traceback-title.png
   :scale: 80

Если вы кликните по этому заголовку, то отображение стека вызовов изменится
на Debugger/Plaintext. Вот как выглядит экран просмотра трассировки в виде
простого текста.

.. image:: images/debugger-plaintext-view.png
   :scale: 80


Отсылка трассировки
-------------------

Когда вы видите трассировку в виде простого текста, там присутствует кнопка
с текстом ``create past``. Если вы кликните по этой кнопке, Kay отправит эту
трассировку на специальный сервис, который расположен по адресу:
http://paste.shehas.net/ . Если отправка трассировки будет успешной, то будет
показана ссылка на нее.

.. image:: images/debugger-paste-succeed.png
   :scale: 80

Это скриншот этого сервиса по обмену кусками кода.

.. image:: images/debugger-paste-service.png
   :scale: 80


Исключения в шаблонах Jinja2
----------------------------

If an exception occurs in Jinja2 template, you will see wired
traceback on the debugger. That is because of the restriction of
appengine( can not use ctypes). For a workaround, we can patch
dev_appserver.py in appengine SDK.

After adding 'gestalt' and '_ctypes' to the list
``_WHITE_LIST_C_MODULES``, you can see normal tracebacks on the
debugger.

Having said that, some python distribution has a broken ctypes(ex:
recent python25 in macports), and above workaround won't work with
broken ctypes. In such a case, copying _speedups.so into the directory
``kay/lib/jinja2`` from another jinja2 installation(not from bundled
in Kay), and adding '_speedups' to the list ``_WHITE_LIST_C_MODULES``
could be another workaround. If you're using MacOSX, the easiest way
to get compiled _speedups.so is to install py25-jinja2 with macports.


Using pdb
=========

You can also use pdb for debugging in dev environment. If you invoke
:func:`kay.utils.set_trace` anywhere on your code, the execution of
your program will stop. You can see a pdb prompt on the console in
which you invoked ``manage.py runserver``.

For example, you can execute your program step by step with a command
``step``. For more details how to use pdb, please refer to following
URL:

* http://www.python.org/doc/2.5.4/lib/debugger-commands.html
