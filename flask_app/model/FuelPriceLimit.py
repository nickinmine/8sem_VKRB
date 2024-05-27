from config.config import db


class FuelPriceLimit(db.Model):
    __tablename__ = 'vkr_price_limit'
    __table_args__ = {"schema": "vkr_app"}
    limit_id = db.Column(db.Integer(), nullable=False, primary_key=True)
    ai_92_min = db.Column(db.Float(), nullable=False)
    ai_92_max = db.Column(db.Float(), nullable=False)
    ai_95_min = db.Column(db.Float(), nullable=False)
    ai_95_max = db.Column(db.Float(), nullable=False)
    ai_98_min = db.Column(db.Float(), nullable=False)
    ai_98_max = db.Column(db.Float(), nullable=False)
    ai_100_min = db.Column(db.Float(), nullable=False)
    ai_100_max = db.Column(db.Float(), nullable=False)
    dt_min = db.Column(db.Float(), nullable=False)
    dt_max = db.Column(db.Float(), nullable=False)
    gas_min = db.Column(db.Float(), nullable=False)
    gas_max = db.Column(db.Float(), nullable=False)
    limits_updating_date = db.Column(db.DateTime(), nullable=False)
    prices_updating_date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return (f"{self.ai_92_min},"
                f"{self.ai_92_max},"
                f"{self.ai_95_min},"
                f"{self.ai_95_max},"
                f"{self.ai_98_min},"
                f"{self.ai_98_max},"
                f"{self.ai_100_min},"
                f"{self.ai_100_max},"
                f"{self.dt_min},"
                f"{self.dt_max},"
                f"{self.gas_min},"
                f"{self.gas_max},"
                f"{self.limits_updating_date},"
                f"{self.prices_updating_date}")
