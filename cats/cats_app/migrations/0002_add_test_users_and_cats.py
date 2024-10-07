from django.db import migrations, models

def create_test_data(apps, schema_editor):
    User = apps.get_model('cats_app', 'User')
    Kind = apps.get_model('cats_app', 'Kind')
    Cat = apps.get_model('cats_app', 'Cat')

    User.objects.create(
        username='testuser1',
        password='pbkdf2_sha256$600000$Wm1ImS26oMzCQvgTaqoOz4$/fITH7vJPXdBJUvxJNKaa/bfds67l5+TSvbexUSCo3g=', # password123
        email='test1@example.com',
        first_name='Test',
        last_name='User1'
    )

    User.objects.create(
        username='testuser2',
        password='pbkdf2_sha256$600000$ZCnlhk8wK1b1mHy3egJPYR$zq0J2ieCgzB0aistxlfURVeNrMzMoim4PPO3QkjY/OI=', # password456
        email='test2@example.com',
        first_name='Test',
        last_name='User2'
    )

    Kind.objects.create(
        name='Siamese'
    )

    Cat.objects.create(
        color='Gray',
        age=3,
        description='Test cat',
        kind_id=Kind.objects.first().id
    )

class Migration(migrations.Migration):

    dependencies = [
        ('cats_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_data),
    ]
