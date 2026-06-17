from django import forms

from .models import SyncExecution


class ManualSyncForm(forms.Form):
    direction = forms.ChoiceField(
        label="Направление синхронизации",
        choices=SyncExecution.DIRECTION_CHOICES,
    )
