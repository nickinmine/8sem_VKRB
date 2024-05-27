from config.config import db


class Admin(db.Model):
    __tablename__ = 'vkr_admin'
    __table_args__ = {"schema": "vkr_app"}
    user_uuid = db.Column(db.String(), nullable=False, primary_key=True)
    user_login = db.Column(db.String(), unique=True, nullable=False)
    user_password = db.Column(db.String(), nullable=False)
    user_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"{self.user_uuid}, {self.user_login}, {self.user_name}"

    def create(self, user_uuid):
        self.user_uuid = user_uuid
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_uuid)

    def get(self):
        return Admin()
