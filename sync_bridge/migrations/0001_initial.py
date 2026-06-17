from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SyncExecution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("direction", models.CharField(choices=[("bitrix_to_1c", "Bitrix -> 1C"), ("1c_to_bitrix", "1C -> Bitrix"), ("both", "В обе стороны")], max_length=32)),
                ("status", models.CharField(choices=[("pending", "В процессе"), ("success", "Успешно"), ("failed", "Ошибка")], default="pending", max_length=16)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("pulled_count", models.PositiveIntegerField(default=0)),
                ("pushed_count", models.PositiveIntegerField(default=0)),
                ("message", models.TextField(blank=True)),
            ],
            options={"ordering": ["-started_at"]},
        ),
    ]
