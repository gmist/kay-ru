
===============================
Использование медиа-компрессора
===============================

.. note::

   Эта фозможность находится в бета-статусе. Реализация может быть изменена
   в будующем.

Обзор
=====

Если ваше приложение имеет множество JavaScript и CSS файлов, то это может быть
весьма затратно для загрузки всех этих файлов. Для снижения расходов при
загрузке страницы, вы можете использовать ``media compressor``.

По умолчанию Kay использует встроенный jmin модуль для сжатия JavaScript и
объединяет CSS файлы в один для их "сжатия".

Также вы можете самостоятельно изменить способы и инструменты для сжатия JavaScript
и CSS файлов.

По умолчанию сжатые файлы сохраняются в директорию ``_generated_media``. Вы
должны добавить эту директорию в ``app.yaml`` в настройку статических файлов.


Media compressor, быстрый старт
===============================

Для использования медиа-компрессора вам нужно добавить context_processor в
переменную ``CONTEXT_PROCESSORS`` и добавить две конфигурационные переменные.

Допустим, что у вас есть следующие каталоги, которые содержат различные
медиа файлы - таблицы стилей и java скрипты:

.. code-block:: bash

   $ tree media
   media
   |-- css
   |   |-- base_layout.css
   |   |-- common.css
   |   |-- component.css
   |   |-- fonts.css
   |   |-- subpages.css
   |   `-- toppage.css
   |-- images
   `-- js
       |-- base.js
       |-- jquery-ui.min.js
       |-- jquery.min.js
       |-- subpage.js
       `-- toppage.js

Теперь предположим, что на главной странице вы используете jQuery, jQuery-UI,
base.js, toppage.js и все CSS файлы, за исключением subpages.css. Также
предположим, что в подстранице вы будете использовать base.js, subpage.js, и
все CSS файлы кроме toppage.css.

Вот простая конфигурация, для приведенной выше ситуации:

settings.py:

.. code-block:: python

   CONTEXT_PROCESSORS = (
     'kay.context_processors.request',
     'kay.context_processors.url_functions',
     'kay.context_processors.media_url',
     'kay.ext.media_compressor.context_processors.media_urls',
   )

   COMPILE_MEDIA_JS = {
     'toppage.js': {
       'output_filename': 'toppage.js',
       'source_files': (
	 'media/js/jquery.min.js',
	 'media/js/jquery-ui.min.js',
	 'media/js/base.js',
	 'media/js/toppage.js',
       ),
     },
     'subpages.js': {
       'output_filename': 'subpages.js',
       'source_files': (
	 'media/js/base.js',
	 'media/js/subpage.js',
       ),
     },
   }

   COMPILE_MEDIA_CSS = {
     'toppage.css': {
       'output_filename': 'toppage.css',
       'source_files': (
	 'media/css/common.css',
	 'media/css/component.css',
	 'media/css/fonts.css',
	 'media/css/base_layout.css',
	 'media/css/toppage.css',
       ),
     },
     'subpages.css': {
       'output_filename': 'subpages.css',
       'source_files': (
	 'media/css/common.css',
	 'media/css/component.css',
	 'media/css/fonts.css',
	 'media/css/base_layout.css',
	 'media/css/subpages.css',
       ),
     },
   }

название_вашего_приложения/templates/index.html:

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page</title>
   {{ compiled_css('toppage.css') }}
   {{ compiled_js('toppage.js') }}
   </head>
   <body>
   Your html goes here
   </body>
   </html>

В сервере разработки, сжатие по умолчанию отключено и тэги compiled_***
раскрываются следующим образом:

.. code-block:: html

   <link type="text/css" rel="stylesheet" href="/media/css/common.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/component.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/fonts.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/base_layout.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/toppage.css" /> 

   <script type="text/javascript" src="media/js/jquery.min.js"></script> 
   <script type="text/javascript" src="media/js/jquery-ui.min.js"></script> 
   <script type="text/javascript" src="media/js/base.js"></script> 
   <script type="text/javascript" src="media/js/toppage.js"></script> 

Для компилирования этих файлов вы должны вызвать подкоманду ``compile_media``
скрипта ``manage.py``.

.. code-block:: bash

   $ python manage.py compile_media
   Running on Kay-0.8.0
   Compiling css media [toppage.css]
    concat /Users/tmatsuo/work/mediatest/media/css/common.css
    concat /Users/tmatsuo/work/mediatest/media/css/component.css
    concat /Users/tmatsuo/work/mediatest/media/css/fonts.css
    concat /Users/tmatsuo/work/mediatest/media/css/base_layout.css
    concat /Users/tmatsuo/work/mediatest/media/css/toppage.css
   Compiling css media [subpages.css]
    concat /Users/tmatsuo/work/mediatest/media/css/common.css
    concat /Users/tmatsuo/work/mediatest/media/css/component.css
    concat /Users/tmatsuo/work/mediatest/media/css/fonts.css
    concat /Users/tmatsuo/work/mediatest/media/css/base_layout.css
    concat /Users/tmatsuo/work/mediatest/media/css/subpages.css
   Compiling js media [toppage.js]
   Compiling js media [subpages.js]

   $ tree _generated_media

   _generated_media
   `-- 1
       |-- css
       |   |-- subpages.css
       |   `-- toppage.css
       `-- js
	   |-- subpages.js
	   `-- toppage.js

   3 directories, 4 files

Для включения отдачи этих файлов с помошью App Engine, вы должны добавиь
директорию ``_generated_media`` как обработчик статических каталогов, как
показано ниже:

.. code-block:: yaml

   - url: /_generated_media
     static_dir: _generated_media

Теперь вы можете развернуть паше приложение и сжатые медиа файлы на appspot.
И на главной странице сслылки на них примут следующий вид:

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
   <html> 
   <head> 
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
   <title>Top Page - myapp</title> 
   <link type="text/css" rel="stylesheet" href="/_generated_media/1/css/toppage.css" /> 

   <script type="text/javascript" src="/_generated_media/1/js/toppage.js"></script> 

   </head> 
   <body> 
   Your contents go here.
   </body> 
   </html>

Дополнительные опции
====================

У этого иструмента, для JavaScript файлов, есть следующие дополнительные опции:

* ``concat``

	Просто объединяет все JavaScript файлы

* ``jsminify``

	Использует встроенный jsmin модуль для сжатия JavaScript файлов

* ``goog_calcdeps``

	Использует calcdeps.py из Google's Closure Library для сжатия/вычисления
	зависимостей

* ``goog_compiler``

	Использует Google's Closure Compiler для оптимизации JavaScript файлов


Доостыпные оции для CSS файлов:

* ``separate``
	Просто копирует все CSS файлы

* ``concat``

	Просто объединяет все CSS файлы

* ``csstidy``

	Использует csstidy для оптимизации CSS файлов. Вы должны иметь уже
	исталированный csstidy.


TODO
====

* Image handling
* More detailed references


