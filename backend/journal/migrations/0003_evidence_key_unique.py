from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0002_evidence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evidence",
            name="key",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
