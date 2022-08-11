import email
import random
from faker import Faker
import logging

from models.models import (
    User,
    Card,
)
import utils

logger = logging.getLogger(__name__)
class Generator:
    def __init__(self) -> None:
        self.fake = Faker()

    def generation_users(self):
        user_count = User.query.count()
        while user_count <= 500:
            user: User = User(
                name=self.fake.name(),
                iin=utils.generate_user_id(User.get_all()),
                email=self.fake.email(),
                password="qwerty"
            )
            user.save()
            user_count += 1

        logger.info("users is successful generate")


    def generation_card(self):
        card_count = Card.query.count()
        user_id_list = [u.id for u in User.get_all()]
        while card_count <= 500:
            random_user_id = random.choice(user_id_list)
            card: Card = Card(
                owner_id=random_user_id,
                number=utils.generate_card_number(Card)
            )
            card.save()
            card_count += 1
            user_id_list.remove(random_user_id)

        logger.info("cards is successful generate")


    def generation(self):
        self.generation_users()
        self.generation_card()
