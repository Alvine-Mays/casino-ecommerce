from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_url',
            field=models.URLField(max_length=1000, blank=True, default=''),
        ),
    ]
