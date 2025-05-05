from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_ticket_assigned_to_alter_ticket_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(default='Ramallah', max_length=50),
        ),
    ]
