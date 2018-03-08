==========================
Django Translatable Fields
==========================

Translatable model fields for Django with admin integration. Uses PostgreSQL JSONField.

Installation
============


* Add application

.. code:: python

    INSTALLED_APPS = (
        ...
        'translatable_fields',
        ...
    )

* Add `TranslatableField` model fields

.. code:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    from translatable_fields.models import TranslatableField


    class Position(models.Model):
        ...
        title = TranslatableField(
            verbose_name=_('title')
        )
        description = TranslatableField(
            verbose_name=_('description')
        )
        ...
        
* Create custom model admin form

.. code:: python

    from django import forms
    from django.contrib.postgres.forms import JSONField
    from ckeditor_uploader.widgets import CKEditorUploadingWidget

    from careers.models.position import Position
    from translatable_fields.widgets import TranslatableWidget


    class PositionAdminForm(forms.ModelForm):
        title = JSONField(widget=TranslatableWidget(widget=forms.TextInput))
        description = JSONField(widget=TranslatableWidget(widget=CKEditorUploadingWidget))

        class Meta:
            model = Position
            fields = (
                ...
                'title',
                'description',
                ...
            )

* Create custom model admin with custom form

.. code:: python

    from django.contrib import admin

    from careers.forms.admin.position import PositionAdminForm


    class PositionAdmin(admin.ModelAdmin):
        form = PositionAdminForm

