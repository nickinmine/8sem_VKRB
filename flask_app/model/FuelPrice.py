from config.config import db


class FuelPrice(db.Model):
    __tablename__ = 'vkr_fuel_price'
    __table_args__ = {"schema": "vkr_app"}
    price_id = db.Column(db.Integer(), nullable=False, primary_key=True)
    azs_id = db.Column(db.Integer(), db.ForeignKey('vkr_app.vkr_azs.azs_id'), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    ai_92 = db.Column(db.Float(), nullable=True)
    ai_95 = db.Column(db.Float(), nullable=True)
    ai_98 = db.Column(db.Float(), nullable=True)
    ai_100 = db.Column(db.Float(), nullable=True)
    dt = db.Column(db.Float(), nullable=True)
    gas = db.Column(db.Float(), nullable=True)

    def __repr__(self):
        return (f"{self.price_id},"
                f"{self.azs_id},"
                f"{self.date},"
                f"{self.ai_92},"
                f"{self.ai_95},"
                f"{self.ai_98},"
                f"{self.ai_100},"
                f"{self.dt},"
                f"{self.gas}")
