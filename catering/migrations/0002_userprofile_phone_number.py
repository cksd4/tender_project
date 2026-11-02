from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='', help_text='Enter contact phone number', max_length=15),
        ),
    ]
