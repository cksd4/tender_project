from django.db import migrations, models
import django.db.models.deletion


def copy_meal_names_to_orders(apps, schema_editor):
    Order = apps.get_model('catering', 'Order')
    database = schema_editor.connection.alias
    for order in Order.objects.using(database).select_related('meal_option').iterator():
        order.meal_name = order.meal_option.name
        order.save(update_fields=['meal_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0003_alter_userprofile_allergen_free_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='meal_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RunPython(copy_meal_names_to_orders, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='order',
            name='meal_option',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ordered_meals',
                to='catering.mealoption',
            ),
        ),
    ]