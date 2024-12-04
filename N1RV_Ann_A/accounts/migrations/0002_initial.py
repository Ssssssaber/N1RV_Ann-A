# Generated by Django 5.1.3 on 2024-12-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="hairdresser_preference",
            field=models.ManyToManyField(
                blank=True,
                to="services.hairdresser",
                verbose_name="Предпочтения по парикмахерам",
            ),
        ),
        migrations.AddField(
            model_name="useraccount",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]