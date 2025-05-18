# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_processor', '0002_alter_document_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processingresult',
            old_name='processed_at',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='processingresult',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='processingresult',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processingresult',
            name='groq_analysis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processingresult',
            name='groq_insights',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processingresult',
            name='model_used',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='processingresult',
            name='is_advanced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='namedentity',
            name='source',
            field=models.CharField(choices=[('spacy', 'spaCy'), ('groq', 'GROQ')], default='spacy', max_length=20),
        ),
        migrations.AddField(
            model_name='namedentity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='processingresult',
            name='sentiment_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='namedentity',
            name='entity_type',
            field=models.CharField(choices=[('person', 'Person'), ('organization', 'Organization'), ('location', 'Location'), ('date', 'Date'), ('money', 'Money'), ('percentage', 'Percentage'), ('product', 'Product'), ('event', 'Event'), ('other', 'Other')], default='other', max_length=20),
        ),
    ] 