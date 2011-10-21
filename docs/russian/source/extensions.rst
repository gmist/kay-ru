=============
Пакет kay.ext
=============

.. Note::
    Описываемая ниже функциональность является экспериментальной и может быть
    изменена в будущем.

Среда разработки Kay включает очень полезный пакет ``kay.ext``, который мы
сейчас рассмоторим.

.. module:: kay.ext

Пакет kay.ext.appstats
======================

.. module:: kay.ext.appstats

``kay.ext.appstats`` это пакет, который содержит утилиты для облегчения
использования Appstats. Для более подробной информации о том, что такое
Appstats и с чем его едят, смотрите раздел `Appstats for Python
<http://code.google.com/intl/en/appengine/docs/python/tools/appstats.html>`_
из документации по Google App Engine SDK.

.. class:: kay.ext.appstats.middleware.AppStatsMiddleware

Модуль ``appstats`` содержит класс ``AppStatsMiddleware``, который задействует
Appstats для вашего приложения. Просто добавьте
``kay,ext.appstats.middleware.AppStatsMiddleware`` в :attr:`settings.MIDDLEWARE`
для включения этого компонента:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'kay.ext.appstats.middleware.AppStatsMiddleware',
        # ...
    )

Также, вам будет необходимо включить интерфейс администратора Appstats в
``app.yaml`` вашего проекта, согласно документации Google App Engine SDK.

.. code-block:: yaml

    builtins:
    - appstats: on

При использовании приложением модуля :mod:`kay.ext.live_settings`,
AppStatsMiddleware может быть отключен без повторного развертывания приложения
- вы можете установить ``kay.ext.appstats.middleware`` в положение ``off``, для
 того чтобы его отключить или в положение ``on``, чтобы задействовать.

Модуль kay.ext.ereporter
========================

.. module:: kay.ext.ereporter

Модуль ``kay.ext.ereporter`` добавляет возможность накопления и просмотра
отчетов об ошибках генерируемых приложением. Этот модуль обеспечивает
сохранение информации об ошибках, просмотр отчетов по ошибкам и частоте их
возникновения. Отчеты доступны через консоль администрирования App Engine, а
также могут ежедневно отсылаться администраторам.

Установка
---------

Для использования ``kay.ext.ereporter`` просто добавьте `kay.ext.ereporter`
в кортеж :attr:`settings.INSTALLED_APPS` в settings.py вашего проета.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'kay.ext.ereporter',
        # ...

Установленный ``kay.ext.ereporter`` не отсылает администарторам отчеты по каждой
ошибке, которая может возникнуть в вашем приложении. Вместо этого он будет
записывать ошибки в хранилище, для последующего просмотра администраторами.
Для больших сайтов, которые могут генерировать большое количество ошибок, такое
поведение может значительно уменьшить нагрузку на ваш почтовый ящик.

Ежедневные отчеты
-----------------

Для включения ежедневных отчетов, вы должны добавить адреса ereporter в словарь
:attr:`settings.APP_MOUNT_POINTS` в ``settings.py`` вашего проекта, а так же в
``cron.yaml`` файл. Также вам будет нужно установить в консоли администрирования
Google App Engine права разработчика для аккаунта, с почтового ящика которого
будет производиться рассылка. Ниже приведен пример настройки ежедневного отчета:

**settings.py**:

.. code-block:: python

    APP_MOUNT_POINTS = {
      #...
      'kay.ext.ereporter': '/_kay/ereporter/',
      #...
    }

**cron.yaml**:

.. code-block:: yaml

    - description: Daily exception report
      url: /_kay/ereporter/?sender=system@example.com
      schedule: every day 00:00

Cron задача поддерживает несколько параметров, которые передаются ей с помощью
параметров URL:
The cron job supports several url parameters which can be added to the cron job url.

1. **sender**

Этот параметр передает адрес почтового ящика, с которого будет производиться
рассылка. Это почтовый адрес должен быть зарегистрирован как разработчик вашего
приложения.

2. **to**

Данный параметр указывает адрес почтового ящика на который необходимо отправить
отчет. По умолчанию, если этот парамет не задан, отчет будет отправлен всем, кто
зарегестрирован как разработчик.

3. **date**

Параметр ``date`` задает дату, для которой должен быть сгенерирован отчет.
Обычно этот параметр не используется и в этом случае используется вчерашняя
дата. Дата должна быть указана в формате YYYY-MM-DD.

4. **versions**

Когда развертывается обновленная версия приложения, App Engine увеличивает
минорную версию приложения. С помощью параметра ``versions`` можно генерировать
отчет для всех ранее загруженных версий или только для последней. Этот параметр
может иметь значение `all` или `latest`. Если используется значение `all`, то
будет сгенерирован отчет для всех версий, значение `latest` приведет к
генерации отчета только по текущей версии.

Пользовательская страница администратора
----------------------------------------

.. image:: images/ereporter.png

Пользовательская страница администратора, находящаяся в консоли
администрирования App Engine, отображает ошибки приложения в виде
простого интерфейса. Вы можете включить страницу администрирования ereporter,
добавив ereporter в словарь :attr:`settings.APP_MOUNT_POINTS` вашего приложения
и включив страницу администрирования в ``app.yaml``, как показано ниже:

**settings.py**:

.. code-block:: python

    APP_MOUNT_POINTS = {
      #...
      'kay.ext.ereporter': '/_kay/ereporter/',
      #...
    }

**app.yaml**

.. code-block:: yaml

    admin_console:
      pages:
      - name: Error Reporter Admin
        url: /_kay/ereporter/admin

Модуль kay.ext.nuke
===================

``nuke`` - это маленькая утилита, предназначенная для удаления всех ваших
данных в одно действие.

.. module:: kay.ext.nuke

Для использования ``kay.ext.nuke``, для начала, вы должны скачать копию
`bulkupdate` с `github
repository <http://github.com/arachnid/bulkupdate>`_, скопировать его в
директорию вашего проекта, добавить ``kay.ext.nuke`` в кортеж
:attr:`settings.INSTALLED_APPS` и вставить следующие строчки в файл
``app.yaml``:

.. code-block:: yaml

  admin_console:
    pages:
    - name: Bulk Update Jobs
      url: /_ah/bulkupdate/admin/
    - name: Nuke
      url: /_ah/nuke/

  handlers:
  - url: /_ah/nuke/.*
    script: kay/main.py
    login: admin

  - url: /_ah/bulkupdate/admin/.*
    script: bulkupdate/handler.py
    login: admin

После этого вы увидите меню ``Nuke`` в вашей консоли администрирования или
просто пройдите по ссылке ``/_ah/nuke``.

Пакет kay.ext.gaema
===================

Пакет ``kay.ext.gaema`` обеспечивает поддержку аутентификации через различные
социальные сервисы. На текущий момент поддурживаются следующие сервисы:

* google OpenID
* google OpenID/OAuth Hybrid
* Twitter OAuth
* Facebook Connect
* Yahoo OpenID

Модуль ``kay.ext.gaema.services`` содержит константы для этих сервисов
с именами:

* GOOG_OPENID
* GOOG_HYBRID
* TWITTER
* FACEBOOK
* YAHOO

Все функции, приведенные ниже, получают параметр ``service`` в качестве первого
аргумента, который может принимать значения описанные выше.

Для использования сервисов Twitter или Facebook, вы должны зарегистрировать ваше
приложение на веб-сайтах этих сервисов и добавить полученные ключи в словарь
:attr:`settings.GAEMA_SECRETS`.

Модуль kay.ext.gaema.utils
--------------------------
Модуль ``kay.ext.gaema.utils`` имеет следующие функции:

.. module:: kay.ext.gaema.utils

.. function:: create_gaema_login_url(service, nexturl)

    Функция для создания ссылки на форму входа через указанный социальный
    сервис. После удачного входа, пользователь будет перенаправлен на адрес,
    который передается в URL параметром ``nexturl``.

.. function:: create_gaema_logout_url(service, nexturl)

    Функция создания ссылки выхода для указанного социальноо сервиса. После
    выхода пользователь будет перенаправлен по адресу, которй передается в URL
    параметром ``nexturl``.

.. function:: get_gaema_user(service)
    Функция для получения информации о текущем пользователе в виде словаря. Если
    пользователь не вошел в социальный сервис, функция вернет ``None``.


Модуль ``kay.ext.gaema.decorators`` имеет следующие декораторы:

.. module:: kay.ext.gaema.decorators

.. function:: gaema_login_required(\*services)
    Декоратор для ограничения доступа к представлению только для пользователей,
    которые вошли через определенную социальный сервис. Сервис передается в
    виде константы из ``kay.ext.gaema.services``.


Ниже приведет пример, показывающий как аутентифицировать пользователя через
twitter OAuth. Для начала, вы должны зарегистрировать ваше приложение на
`веб-сайте Twitter <http://twitter.com/apps>`_ и добавить полученный ключ и
секрет в словарь `settings.GAEMA_SECRETS`, внести ``kay.ext.gema`` в кортеж
:attr:`settings.INSTALLED_APPS` и активировать, как показано ниже:
``kay.session.middleware.SessionMiddleware``

.. code-block:: python

  INSTALLED_APPS = (
    'myapp',
    'kay.ext.gaema',
  )

  GAEMA_SECRETS = {
    "twitter_consumer_key": "hogehogehogehogehogehoge",
    "twitter_consumer_secret": "fugafugafugafugafugafugafugafuga",
  }

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
  )

И затем нужно создать представление:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views

  import logging

  from werkzeug import Response
  from kay.ext.gaema.utils import (
    create_gaema_login_url, create_gaema_logout_url, get_gaema_user
  )
  from kay.ext.gaema.decorators import gaema_login_required
  from kay.ext.gaema.services import TWITTER
  from kay.utils import (
    render_to_response, url_for
  )

  # Create your views here.

  def index(request):
    gaema_login_url = create_gaema_login_url(TWITTER,
					     url_for("myapp/secret"))
    return render_to_response('myapp/index.html',
			      {'message': 'Hello',
			       'gaema_login_url': gaema_login_url})

  @gaema_login_required(TWITTER)
  def secret(request):
    user = get_gaema_user(TWITTER)
    gaema_logout_url = create_gaema_logout_url(TWITTER,
					       url_for("myapp/index"))
    return render_to_response('myapp/secret.html',
			      {'user': user,
			       'gaema_logout_url': gaema_logout_url})


kay.ext.live_settings
======================

.. module:: kay.ext.live_settings

Многие (если не сказать - большинство) приложения имеют глобальные переменные,
которые переодически приходится изменять или подстраивать для быстродействия
и/или по каким-то бизнес причинам (например, нужно изменить email почтового
ящика, который используется для рассылки спама или включить/выключить режим
отладки). При этом, модификация того же ``settings.py`` приводит к необходимости
повторного развертывания приложения, что для высоко нагруженных сайтов может
привести к появлению задержек при отдаче контента и другим неприятным проблемам.

Для решения этой проблемы есть специальный модуль "меняющиеся настройки"
`live_settings` , который позволяет создавать глобальные переменные,
которые могут быть динамически изменены без необходимости переразвертывания
приложения. Например, вы можете включить или выключить ``ppstats`` или другие
компоненты и при этом вам не потребуется еще раз производить развертывание
вашего приложения. Звучит клево, не так ли?

Установка
---------

Расширение "меняющихся настроек" устанвливает устанавливает добавленим
``kay.ext.live_settings`` в кортеж :attr:`settings.INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'kay.ext.live_settings',
        # ...
    )

Использование
-------------

"Меняющиеся настройки" представляют собой строковый ключ на строковую пару
ключ-занчение. Эти пары ключ-значение постоянно находятся в хранилище и
кэшируются в памяти или в memcache. Именно из-за этого процесса кэширования,
распространение значений настроек по всем экземплярам приложения может занять
некоторое время. По умолчанию, переменные в памяти имеют таймаут на изменение
равный одной минутею. Переменные в memcache устанавливаются при смене значения
и никогда не истекают (тут нужно заметить, что ключи все-таки могут быть
удалены из memcache из-за нехватки памяти). Такой многоуровневый подход к
кэшированию позволяет приложениям получать значения измененных переменных так
быстро, как это только возможно.

Получить и установить занчение переменной очень легко:

.. code-block:: python

    from kay.ext.live_settings import live_settings

    value = live_settings.get("my.settings.key", "default_value")

    live_settings.set("my.settings.key", "new-value")

Также можно получить или установить значения сразу нескольких перменных:

.. code-block:: python

    # Get settings in batch
    value = live_settings.get_multi(["my.settings.key", "my.other.setting"])

    my_setting = value["my.settings.key"]
    other_setting = value["my.other.setting"]

    # Set settings in batch
    live_settings.set_multi({
        "my.settings.key": "new_value",
        "my.other.setting": "other_value",
    })

Так как функционал расширения  "меняющиеся настройки" базируется на memcache и
хранилищи, то это позволяет сохранять их в различных пространствах имен. По
умолчанию "меняющиеся настройки" сохраняются в пространстве имен, которое
задано по умолчанию и не зависят от текущего пространтсва имен. Тем не менее,
пространство имен может быть задано для каждой операции получения-уставки
значения:

.. code-block:: python

    from kay.ext.live_settings import live_settings

    value = live_settings.get("my.settings.key", "default_value", namespace="mynamespace")

    live_settings.set("my.settings.key", "new-value", namespace="mynamespace")

Пользовательская страница администрирования
-------------------------------------------

Изменение зачений "меняющихся настроек" может быть осуществлено через
пользовательскую страницу администрирования (не забудьте, что распространение
настроек на все экземпляры приложения может занять несколько минут:

.. image:: images/live_settings.png

Пользовательская страница администрирования включается добавлением
``kay.ext.live_settings`` в словарь :attr:`settings.APP_MOUNT_POINTS` и
добавлением секции ``admin_console`` в ваш ``app.yaml``:

**settings.py**:

.. code-block:: python

    APP_MOUNT_POINTS = {
        # ...
        'kay.ext.live_settings': '/_kay/live_settings/',
        # ...
    }

**app.yaml**:

.. code-block:: yaml

    admin_console:
      pages:
      - name: Live Settings Admin
        url: /_kay/live_settings/admin
