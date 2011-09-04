======================================
Использование функциональности db_hook
======================================

.. Примечание::
    Описываемая функциональность находится в статусе бета-версии и ее
    реализация может быть измененена в будущем.

Обзор
=====

App Engine имеет собственный механизм ``ловушек`` - 
`Using hooks in Google App Engine
<http://code.google.com/intl/en/appengine/articles/hooks.html>`_. Однако, при 
его использовании ваши функции-ловушки просто получают низкоуровневые
запросы/ответы от объектов и поэтому его использование может быть трудоемким.

Kay имеет функциональность, которая делает этот механизм ``ловушек`` более
простым в использовании. Модуль ``kay.utils.db_hook`` соедержит несколько
функций для регистрации ваших функций-ловушек в apiproxy.

Функции
-------

.. модуль:: kay.utils.db_hook

.. функция:: register_pre_save_hook(func, model)
    
    Регистрация функции ``func`` в apiproxy PreCallHooks. Эта функция будет
    вызываться перед тем, как будет сохранен объект модели ``model``.

..  функция:: register_post_save_hook(func, model)
    
    Регистрация функции ``func`` в apiproxy PastCallHooks. Эта функция будет
    вызываться после того, как объект модели ``model`` будет сохранен.

Эти функции предназначены для регистрации, в которые вы должны передать
функции со следущей сигнатурой:

.. code-block:: python

   def your_hook_function(entity, put_type_id):
     # entity - объект модели, с которым производим каккие-то действия
     # put_type_id определен в kay.utils.db_hook.put_type

put_type_id - индикатор, который указывает на то, был ли объект только что
создан или нет. put_type определен в модуле ``kay.utils.db_hook.put_type``:

.. code-block:: python

   NEWLY_CREATED = 1
   UPDATED = 2
   MAYBE_NEWLY_CREATED = 3
   MAYBE_UPDATED = 4
   UNKNOWN = 5

   type_names = {
     1: "Newly Created",
     2: "Updated",
     3: "Maybe Newly Created",
     4: "Maybe Updated",
     5: "Unknown",
   }

   def get_name(type):
     return type_names.get(type, None)

Понятно, что из низкоуровневых запросов/ответов нельзя точно сказать, 
был ли объект только что создан или обновляется после каких-то изменений, 
не проверив ghtldfhbntkmyj хранилище на наличие объекта с таким же ключом.
Поэтому Kay делает предположение, проверя таймштамп создания/обновления объекта.

Сделать проверку хранилища, на наличие объекта с таким же ключом, вы можете 
вызвав ``db.get(entity.key())`` и проверив результат, как показано ниже:

.. code-block:: python

    # Этот фрагмент кода показывает, как написать функцию-ловушку,
    # которая будет что-то делать только перед созданием объекта.
    # Вы должны зарегистрировать эту фунцию используя register_pre_save_hook.

    import logging 

    from google.appengine.ext import db
    from kay.utils.db_hook import register_pre_save_hook

    from myapp.models import comment

    def log_on_creation(entity,put_type_id):
     if db.get(entity.key()) is None:
       # следовательно это только что созданный объект
       logging.debug("Entity: %s is going to be created." % entity.key())

.. функция:: register_pre_delete_hook(func, model)
    Регистрация функции ``func`` в apiproxy PreCallHooks. Эта функция будет
    вызвана перед удалением объекта модели ``model``.

В качестве функции-ловушки, которая будет вызвана перед удалением объекта, вы
должны использовать функцию со следующей сигнатурой:

.. code-block:: python

   def your_hook_function(key):
     # Что-то делаем с key
