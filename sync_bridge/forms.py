from django import forms

from .models import SyncExecution


class ManualSyncForm(forms.Form):
    action = forms.ChoiceField(
        label="Действие",
        choices=[
            ("fetch", "Получить список"),
            ("sync", "Запустить синхронизацию"),
        ],
        initial="fetch",
    )
    direction = forms.ChoiceField(
        label="Направление синхронизации",
        choices=SyncExecution.DIRECTION_CHOICES,
    )
    date_from = forms.DateField(
        label="Дата с",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    date_to = forms.DateField(
        label="Дата по",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    inn = forms.CharField(label="ИНН", required=False, max_length=32)


class InvoiceListForm(forms.Form):
    date_from = forms.DateField(
        label="Дата с",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    date_to = forms.DateField(
        label="Дата по",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    inn = forms.CharField(label="ИНН", required=False, max_length=32)
