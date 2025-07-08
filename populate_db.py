import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Update if your settings path is different
django.setup()

# Import models
from category.models import Category
from participant.models import Participant
from event.models import Event

def populate_event_data():
    fake = Faker()
    
    # Create Categories
    print("Creating categories...")
    category_names = ['Conference', 'Workshop', 'Seminar', 'Networking']
    categories = []
    for name in category_names:
        cat = Category.objects.create(
            name=name,
            description=fake.paragraph()
        )
        categories.append(cat)
    print(f"✅ {len(categories)} categories created.")

    # Create Participants
    print("Creating participants...")
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        participants.append(participant)
    print(f"✅ {len(participants)} participants created.")

    # Create Events
    print("Creating events...")
    for i in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date='today', end_date='+30d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories),
        )

        # Assign 3 to 6 random participants
        event.participants.set(random.sample(participants, random.randint(3, 6)))

    print("✅ 10 events created with participants assigned.")
    print("🎉 Database populated successfully!")


if __name__ == '__main__':
    populate_event_data()
