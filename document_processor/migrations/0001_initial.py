# Generated by Django 5.0 on 2025-03-20 17:29

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("file", models.FileField(upload_to="documents/")),
                ("file_type", models.CharField(blank=True, max_length=100)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("extracted_text", models.TextField(blank=True, null=True)),
                ("processing_time", models.FloatField(blank=True, null=True)),
                ("page_count", models.IntegerField(default=0)),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="document_processor.documenttype",
                    ),
                ),
            ],
            options={
                "ordering": ["-uploaded_at"],
            },
        ),
        migrations.CreateModel(
            name="NamedEntity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                (
                    "entity_type",
                    models.CharField(
                        choices=[
                            ("person", "Person"),
                            ("organization", "Organization"),
                            ("location", "Location"),
                            ("date", "Date"),
                            ("money", "Money"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("confidence_score", models.FloatField(default=1.0)),
                ("page_number", models.IntegerField(default=1)),
                ("position_start", models.PositiveIntegerField(blank=True, null=True)),
                ("position_end", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entities",
                        to="document_processor.document",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProcessingResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("language", models.CharField(blank=True, max_length=50, null=True)),
                ("sentiment_score", models.FloatField(blank=True, null=True)),
                ("keyword_summary", models.TextField(blank=True, null=True)),
                ("processed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "document",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analysis_result",
                        to="document_processor.document",
                    ),
                ),
            ],
        ),
    ]
