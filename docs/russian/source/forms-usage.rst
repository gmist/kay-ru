==================
Использование форм
==================

Введение
--------

Kay имеет специальные утилиты и средства, которые значительно облегчают работу
с формами. Они расположены в модулях ``kay.utils.forms`` и
``kay.utils.forms.modelfor``. Перед тем, как начать работать с этими утилитами,
рассмотрим следующие три концептуальных элемента:

* Widget - Виджет

    Класс, который переобразует поля формы и саму форму в HTML вид, например в
    <input type="text">, <textarea> или <form>...</form>. Если другими
    словами, то этот класс управляет рендерингом формы или ее полей в HTML и
    фактически является логикой представления.

* Field - Поле

    Этот класс описывает поля формы и отвечает за их валидацию, например
    класс ``FloatField`` гарантирует, что хранимые в нем данные совместимы с
    числом с плавающей точкой, т.е. реализует проверочную логику.

* Form - Форма

    Данный класс предназначен для описания формы с помощью ее атрибутов-полей,
    которые могут проверить себя и преобразовать в виджет.


Ваша первая форма
-----------------

Ниже приведен код, который реализует контактную форму, например для обратной
связи с пользователем:

.. code-block:: python

  from kay.utils import forms

  class ContactForm(forms.Form):
    subject = forms.TextField(required=True, max_length=100)
    message = forms.TextField(required=True)
    sender = forms.EmailField(required=True)
    cc_myself = forms.BooleanField(required=False)

Любая форма форма состоит несколько Field объектов, которые описывают ее поля.
В данном случае форма имеет четыре поля: ``subject``, ``message``, ``sender`` и
``cc_myself``, которые являются объектами трех классов: ``TextField``,
``EmailField`` и ``BooleanField``. С полным списком доступных классов полей вы
можете озназомится в разделе :doc:`forms_reference`.


Если ваша форма будет предназначена для простого прямого редактирования моделей
хранилища App Engine, то вы можете использовать специальный класс ``ModelForm``,
для того, чтобы не дублировать описание вашей модели в виде формы.

Использование формы в отображениии
----------------------------------

Обычно, обработка формы в перлставлении выглядит так (ну или как-то так):

.. code-block:: python

  def contact(request):
    form = ContactForm()
    if request.method == "POST":
      if form.validate(request.form):
    	# обработка данных
	    # ...
	    return redirect("/thanks/")
    return render_to_response("myapp/contact.html", {"form": form.as_widget()})

Этот код делает следующее:

1. Если форма не передается в функцию представления, то создается объект класса
   ``ContactForm``, из которого с помощью метода ``form.as_widget()`` создается
   виджет, который и предается в шаблон.

2. Если форма предается в функцию представления, данные формы проверются с
   помощью метода ``form.validate(request.form)``. Если принятые данные правильны
   (например, поле класса ``EmailField`` содержит допустимый адрес, а поля
   ``TextField`` не пусты), то данные как-то обрабатываются
   (к примеру - сохраняются в виде модели хранилища) и пользователь
   перенаправляется на страницу с адресом ``/thanks/``.

3. Если переданная форма содержит недопустимые или некорректные данные,
   то передаваемый в шаблон виджет будет содержать сообщения о найденных ошибках.


Обработка данных из форм
------------------------

Когда ``form.validate()`` возвращает True, вы можете безопасно обрабатывать
данные из формы, зная, что они прошли проверку правилами, определенными в вашей
форме. Несмотря на то, что вы можете обращаться к данным формым напрямую, через
``request.form``, таки рекомендуется использовать следующий стиль:
``form['subject']``, ``form['message']`` или ``form['sender']``, т.к. данные
полученные этим способом не только проверены, но и сконвертированы в соотвествующие типы языка Python. Например, в нашем случае ``cc_myself`` будет булеевой переменной, а значения полей ``IntegerField`` и ``FloatField`` будут преобразованы в типы языка Python - в ``int`` и ``float`` соответственно.

Расширим приведенный выше пример обработкой данных:

.. code-block:: python

  if form.validate(request.form):
    recipients = ["info@example.com"]
    if form["cc_myself"]:
      recipients.append(form["sender"])
    from google.appengine.api import mail
    mail.send_mail(sender=form["sender"], to=recipients,
                   subject=form["subject"], body=form["message"])
    return redirect("/thanks/")

Отображение формы с использованием шаблонов
-------------------------------------------

Виджеты форм очень просты для отображения. В вышеприведенном примере, мы передаем представление виджета формы ContactForms в шаблон, как переменную
``form``. Вот простой пример шаблона, который отображает форму:

.. code-block:: html

  <body>
    {{ form()|safe }}
  </body>

Как вы могли заметить - виджет представляет собой вызываемый объект и если вы
его вызовете, то получите форму в виде HTML. Результат вызова будет
представлен в виде экранированного (HTML escaped), поэтому вы должны добавить
фильтр ``safe`` после этого вызова. Ниже приведен вывода нашего шаблона:

.. code-block:: html

  <form action="" method="post">
    <div style="display: none">
      <input type="hidden" name="_csrf_token" value="c345asdf.........">
    </div>
    <dl>
      <dt><label for="f_subject">Subject</label></dt>
      <dd><input type="text" id="f_subject" value="" name="subject"></dd>
      <dt><label for="f_message">Message</label></dt>
      <dd><input type="text" id="f_message" value="" name="message"></dd>
      <dt><label for="f_sender">Sender</label></dt>
      <dd><input type="text" id="f_sender" value="" name="sender"></dd>
      <dt><label for="f_cc_myself">Cc myself</label></dt>
      <dd><input type="checkbox" id="f_cc_myself" name="cc_myself"></dd>
    </dl>
    <div class="actions"><input type="submit" value="submit"></div>
  </form>


Настройка и модификация шаблона формы
--------------------------------------

Если сгенерированный по-умолчанию HTML код вас не устраивает, то вы можете полностью изменить способ отображения формы с помощью тэга jinja2 ``call``. Когда вы используете тэг ``call``, вы должны разместить содержимое вашей формы
(включая кнопки отправки) между {% call form()} и {% endcall %}. Ниже приведен пример, как можно изменить отображение вашей формы.
If the default generated HTML is not to your taste, you can completely
customize the way a form is presented using ``call`` tag of
jinja2. When you use ``call`` tag, you need to put your form's
contents(including submit buttons) between {% call form() %} and {%
endcall %}. Here's an example of how to customize the representation
of our form.

.. code-block:: html

  <body>
  {% call form() %}
    <div class="fieldWrapper">
      {{ form['subject'].label(class_="myLabel")|safe }}
      {{ form['subject']()|safe }}
    </div>
    <div class="fieldWrapper">
      {{ form['message'].errors()|safe }}
      {{ form['message'].label()|safe }}
      {{ form['message'].render()|safe }}
    </div>
    <div class="fieldWrapper">
      {{ form['sender'].label()|safe }}
      {{ form['sender'].render()|safe }}
      {% if form['sender'].errors %}
	<span class="errors">
	  {% for error in form['sender'].errors %}
	    {{ error }}&nbsp;
	  {% endfor %}
	</span>
      {% endif %}
    </div>
    <div class="fieldWrapper">
      {{ form['cc_myself'].label()|safe }}
      {{ form['cc_myself'].render()|safe }}
      {{ form['cc_myself'].errors(class_="myErrors")|safe }}
    </div>
    {{ form.default_actions()|safe }}
  {% endcall %}
  </body>

The example above shows four different ways to display one field
widget. You can access each field through the root widget's
attribute. Let's take a look in turn.

1. First example

.. code-block:: html

    <div class="fieldWrapper">
      {{ form['subject'].label(class_="myLabel")|safe }}
      {{ form['subject']()|safe }}
    </div>

This code renders the label of the ``subject`` field in ``myLabel``
class. The word ``class`` is reserved, so you need to add an
underscore to avoid error in order to specify the class. The
``subject`` field widget is also callable, and if you call it, you can
get HTML for both of the input field and error messages at a time.

2. Second example

.. code-block:: html

    <div class="fieldWrapper">
      {{ form['message'].errors()|safe }}
      {{ form['message'].label()|safe }}
      {{ form['message'].render()|safe }}
    </div>

The second example shows you how to separate HTMLs of input field and
error messages. If you call render() method instead of just call the
field widget, you only get the HTML of input field. So in most cases,
you need to put codes for displaying error messages. In this example,
you will get this HTML for error messages:

.. code-block:: html

  <ul class="errors"><li>This field is required.</li></ul>

What if you don't like <ul> tags?

3. Third example

.. code-block:: html

    <div class="fieldWrapper">
      {{ form['sender'].label()|safe }}
      {{ form['sender'].render()|safe }}
      {% if form['sender'].errors %}
	<span class="errors">
	  {% for error in form['sender'].errors %}
	    {{ error }}&nbsp;
	  {% endfor %}
	</span>
      {% endif %}
    </div>

The third example shows you how to iterate over error messages. Isn't
is easy?

4. Forth example

.. code-block:: html

    <div class="fieldWrapper">
      {{ form['cc_myself'].label()|safe }}
      {{ form['cc_myself'].render()|safe }}
      {{ form['cc_myself'].errors(class_="myErrors")|safe }}
    </div>

The last example show you how to specify a class attribute on error
messages(be sure its 'class_', not 'class'). Actually, you can specify
any attribute on any renderable widget by passing keyword argument on
rendering.


Handling file upload
--------------------

If your form contains ``FileField`` or Field class drived from it, the
widget automatically rendered with necessary attribute in its form
tag. You need to pass ``request.files`` as well as ``request.form`` to
``validate()`` method. Here's an example that shows you how to handle
file upload.

.. code-block:: python

  # forms.py
  class UploadForm(forms.Form):
    comment = forms.TextField(required=True)
    upload_file = forms.FileField(required=True)

  # views.py
  form = UploadForm()
  if request.method == "POST":
    if form.validate(request.form, request.files):
      # process the data
      # ...
      return redirect("/thanks")


Customizing form validation
---------------------------

To put validation method on particular field, you can define a method
named ``validate_FIELDNAME``. e.g. To check if a value submitted as
``password`` field is stronger enough, you can set
``validate_password`` method in the class definition of the Form. If
validation fails, you need to raise
:class:`kay.utils.validators.ValidationError` with appropriate error
message.

Here's an example:

.. code-block:: python

  from kay.utils import forms
  from kay.utils.validators import ValidationError

  class RegisterForm(forms.Form):
    username = forms.TextField(required=True)
    password = forms.TextField(required=True, widget=forms.PasswordInput)

    def validate_password(self, value):
      if not stronger_enough(value):
	raise ValidationError(u"The password you specified is too weak.")

What if adding a field for password confirmation? To do that, you have
to check the values among plural fields, creating the method named
``context_validate``. Here's an example:

.. code-block:: python

  from kay.utils import forms
  from kay.utils.validators import ValidationError

  class RegisterForm(forms.Form):
    username = forms.TextField(required=True)
    password = forms.TextField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.TextField(required=True, widget=forms.PasswordInput)

    def validate_password(self, value):
      if not stronger_enough(value):
	raise ValidationError(u"The password you specified is too weak.")

    def context_validate(self, data):
      if data['password'] != data['password_confirm']:
	raise ValidationError(u"The passwords don't match.")


Using ModelForm
---------------

:class:`kay.utils.forms.modelform.ModelForm` is a very convenient
class for creating a form automatically from particular model
definition.

Let's say you have a model like bellow:

.. code-block:: python

  class Comment(db.Model):
    user = db.ReferenceProperty()
    body = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

You can create a form automatically from above definition like:

.. code-block:: python

  from kay.utils.forms.modelform import ModelForm
  from myapp.models import Comment

  class CommentForm(ModelForm):
    class Meta:
      model = Comment
      exclude = ('user', 'created')

You can configure your ModelForm's subclass by defining inner class
named ``Meta``. ``Meta`` class can have these class attributes:

.. class:: Meta

   .. attribute:: model

      Model class to refer to

   .. attribute:: fields

      A list of field names to be included in the form. If ``fields``
      is set and non empty, properties not listed here are excluded
      from the form, and following ``exclude`` attribute will be
      ignored.

   .. attribute:: exclude

      A list of field names to be excluded from the form.

   .. attribute:: help_texts

      A dictionary which has field names as its key and help texts as
      its values.

Once created, you can use this form as follows:

.. code-block:: python

  from myapp.models import Comment
  from myapp.forms import CommentForm

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    form = CommentForm()
    if request.method == 'POST':
      if form.validate(request.form):
        if request.user.is_authenticated():
          user = request.user
        else:
          user = None
        new_comment = form.save(user=user)
        return redirect('/')
    return render_to_response('myapp/index.html',
                              {'comments': comments,
                               'form': form.as_widget()})

Above code shows how to asign values not specified in the forms on
saving a new entity with this form. ModelForm.save method accepts
keyword arguments and these arguments will be passed to the
constructor of the new entity on creation.
