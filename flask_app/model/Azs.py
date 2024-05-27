from config.config import db


class Azs(db.Model):
    __tablename__ = 'vkr_azs'
    __table_args__ = {"schema": "vkr_app"}
    azs_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    brand_name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    longitude = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.String(), nullable=False)


    def __repr__(self):
        return (f"{self.azs_id},"
                f"{self.brand_name},"
                f"{self.address},"
                f"{self.longitude},"
                f"{self.latitude}")
