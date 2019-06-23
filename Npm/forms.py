from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from django import forms
from .models import NpmPackage


def typedefault():
    return "default"


class NpmDetailForm(forms.Form):
    name = forms.CharField(label='Package Name')
    version = forms.CharField(label='Package Version')
    type = forms.CharField(label='Package Type', initial="default")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('name', style="width:100%;"),
                    Field('version', style="width:100%;"),
                    Field('type', style="width:100%;"),
                    Submit('submit', 'Download', css_class='btn-success', style="margin-top:15px; width:100%;"),
                    css_class='form-group',
                    style="width:50%; margin: 0 auto; padding: 15px; border: solid 1px;"
                ),
                style="width:100%; margin:0 auto;",
            )
        )


class NpmDetailFormS(forms.ModelForm):
    class Meta:
        model = NpmPackage
        fields = ('name', 'version', 'type')
