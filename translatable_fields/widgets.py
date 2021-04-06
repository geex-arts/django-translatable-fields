import json

from django import forms
from django.conf import settings


class TranslatableWidget(forms.MultiWidget):
    template_name = 'translatable_fields/multiwidget.html'
    widget = forms.Textarea

    class Media:
        js = (
            settings.STATIC_URL + 'translatable_fields/translatable_fields.js',
        )
        css = {
            'all': (
                settings.STATIC_URL + 'translatable_fields/translatable_fields.css',
            )
        }

    def __init__(self, widget=None, *args, **kwargs):
        if widget:
            self.widget = widget

        initial_widgets = [
            self.widget
            for _ in settings.LANGUAGES
        ]

        super().__init__(initial_widgets, *args, **kwargs)

        for ((lang_code, lang_name), sub_widget) in zip(settings.LANGUAGES, self.widgets):
            sub_widget.attrs['lang'] = lang_code
            sub_widget.lang_code = lang_code
            sub_widget.lang_name = lang_name

    def decompress(self, value):
        """
        Returns a list of decompressed values for the given compressed value.
        The given value can be assumed to be valid, but not necessarily
        non-empty.
        """

        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                value = {}

        result = []
        for lang_code, _ in settings.LANGUAGES:
            if value:
                result.append(value.get(lang_code))
            else:
                result.append(None)

        return result

    def value_from_datadict(self, data, files, name):
        result = dict([
            (widget.lang_code, widget.value_from_datadict(data, files, name + '_%s' % i))
            for i, widget in enumerate(self.widgets)
        ])
        if all(map(lambda x: x == '', result.values())):
            return ''
        return json.dumps(result)

    def get_context(self, name, value, attrs):
        context = super(forms.MultiWidget, self).get_context(name, value, attrs)
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)

        final_attrs = context['widget']['attrs']
        input_type = final_attrs.pop('type', None)
        id_ = final_attrs.get('id')
        subwidgets = []

        for i, widget in enumerate(self.widgets):
            if input_type is not None:
                widget.input_type = input_type
            widget_name = '%s_%s' % (name, i)
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                widget_attrs = final_attrs.copy()
                widget_attrs['id'] = '%s_%s' % (id_, i)
            else:
                widget_attrs = final_attrs
            widget_attrs = self.build_widget_attrs(widget, widget_value, widget_attrs)
            widget_context = widget.get_context(widget_name, widget_value, widget_attrs)['widget']
            widget_context.update(dict(
                lang_code=widget.lang_code,
                lang_name=widget.lang_name
            ))

            widget_context['html'] = widget.render(widget_name, widget_value, widget_attrs)
            subwidgets.append(widget_context)
        context['widget']['subwidgets'] = subwidgets

        return context

    @staticmethod
    def build_widget_attrs(widget, value, attrs):
        attrs = dict(attrs)  # Copy attrs to avoid modifying the argument.

        if (not widget.use_required_attribute(value) or not widget.is_required) \
                and 'required' in attrs:
            del attrs['required']

        return attrs
