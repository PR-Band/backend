from datetime import datetime

from backend.db import db_session
from backend.models import Slot


class SlotStorage():
    def add(self, product_id: int, slot: datetime) -> Slot:
        add_slots = Slot(
            product_id=product_id,
            slot=slot,
        )
        db_session.add(add_slots)
        db_session.commit()
        return add_slots
