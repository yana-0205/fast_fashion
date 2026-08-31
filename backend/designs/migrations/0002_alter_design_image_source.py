from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("designs", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="design",
            name="image_source",
            field=models.CharField(default="user-upload", max_length=40),
        )
    ]

