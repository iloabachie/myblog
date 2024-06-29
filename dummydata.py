from app import *
import faker


fake = faker.Faker()

# for _ in range(100):
#     user = Users(name=fake.name(), email=fake.email(), location=fake.address())
#     db.session.add(user)
#     db.session.commit()

print(fake.address())
for _ in range(10):
    print(_, fake.name(), fake.address().replace('\n', ','), fake.email(), sep=' | ')