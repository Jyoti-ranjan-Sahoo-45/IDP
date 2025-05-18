# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_processor', '0003_update_processing_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='namedentity',
            name='page_number',
        ),
        migrations.RemoveField(
            model_name='namedentity',
            name='position_start',
        ),
        migrations.RemoveField(
            model_name='namedentity',
            name='position_end',
        ),
        migrations.AddField(
            model_name='namedentity',
            name='position_start',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='namedentity',
            name='position_end',
            field=models.IntegerField(blank=True, null=True),
        ),
    ] 