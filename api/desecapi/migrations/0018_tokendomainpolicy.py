# Generated by Django 3.2.10 on 2021-12-17 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):
    dependencies = [
        ("desecapi", "0017_alter_user_limit_domains"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="TokenDomainPolicy",
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
                ("perm_dyndns", models.BooleanField(default=False)),
                ("perm_rrsets", models.BooleanField(default=False)),
                (
                    "domain",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="desecapi.domain",
                    ),
                ),
                (
                    "token",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="desecapi.token"
                    ),
                ),
                (
                    "token_user",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="token",
            name="domain_policies",
            field=models.ManyToManyField(
                through="desecapi.TokenDomainPolicy", to="desecapi.Domain"
            ),
        ),
        migrations.AddConstraint(
            model_name="tokendomainpolicy",
            constraint=models.UniqueConstraint(
                fields=("token", "domain"), name="unique_entry"
            ),
        ),
        migrations.AddConstraint(
            model_name="tokendomainpolicy",
            constraint=models.UniqueConstraint(
                condition=models.Q(("domain__isnull", True)),
                fields=("token",),
                name="unique_entry_null_domain",
            ),
        ),
        # The remaining operations ensure that domain.owner and token.user can't be inconsistent
        migrations.AlterModelOptions(
            name="token",
            options={},
        ),
        migrations.AddConstraint(
            model_name="token",
            constraint=models.UniqueConstraint(
                fields=("id", "user"), name="unique_id_user"
            ),
        ),
        migrations.AddConstraint(
            model_name="domain",
            constraint=models.UniqueConstraint(
                fields=("id", "owner"), name="unique_id_owner"
            ),
        ),
        migrations.RunSQL(
            "ALTER TABLE desecapi_tokendomainpolicy"
            " ADD FOREIGN KEY ( domain_id, token_user_id ) REFERENCES desecapi_domain ( id, owner_id ),"
            " ADD FOREIGN KEY ( token_id, token_user_id ) REFERENCES desecapi_token ( id, user_id );",
            migrations.RunSQL.noop,
        ),
    ]
