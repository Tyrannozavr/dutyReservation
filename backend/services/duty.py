from sqlmodel import Session


class DutiesServices:

    def __init__(self, queries):
        self.queries = queries

    def get_duties(self, db: Session):
        return self.queries.get_duties()

    def get_duty(self, duty_id, db: Session):
        return self.queries.get_duty(duty_id)

    def create_duty(self, duty, db: Session):
        return self.queries.create_duty(duty)

    def update_duty(self, duty_id, duty, db: Session):
        return self.queries.update_duty(duty_id, duty)

    def delete_duty(self, duty_id, db: Session):
        return self.queries.delete_duty(duty_id)


