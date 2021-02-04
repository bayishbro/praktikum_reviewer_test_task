import datetime as dt


class Record:
    """docstring"""

    def __init__(self, amount, comment, date=dt.date.today()):
        """docstring"""

        self.amount = amount
        self.comment = str(comment)

        if not isinstance(date, dt.date):
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        else:
            self.date = date


class Calculator:
    """docstring"""

    def __init__(self, limit):
        """docstring"""

        self.limit = limit
        self.records = []

    def add_record(self, record):
        """docstring"""

        self.records.append(record)

    def get_stats(self, days_amount):
        """docstring"""

        count = 0
        past_date = dt.date.today() - dt.timedelta(days=days_amount)
        today = dt.date.today()

        for record in self.records:
            if past_date < record.date <= today:
                count += record.amount
        return count

    def get_today_stats(self):
        """docstring"""

        return self.get_stats(1)

    def get_week_stats(self):
        """docstring"""

        return self.get_stats(7)


class CaloriesCalculator(Calculator):
    """docstring"""

    def get_calories_remained(self):
        """docstring"""

        x = self.limit - self.get_today_stats()

        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'

        return f'Хватит есть!'


class CashCalculator(Calculator):
    """docstring"""

    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        """docstring"""

        cash_remained = self.limit - self.get_today_stats()

        if cash_remained == 0:
            return f"Денег нет, держись"

        if cash_remained < 0:
            return f"Денег нет, держись: твой долг - {str(cash_remained)}"

        currency_switch = {
            'rub': (self.RUB_RATE, "руб"),
            'usd': (self.USD_RATE, "USD"),
            'eur': (self.EURO_RATE, "Euro")
        }
        currency_str = f'{round(cash_remained / currency_switch[currency][0], 2)} {currency_switch[currency][1]}'

        return f"На сегодня осталось {currency_str}"


if __name__ == "__main__":
    cash_calculator = CashCalculator(7000.0)
    cash_calculator.add_record(
        Record(amount=5000, comment="test", date="04.02.2021"))
    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))

    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(amount=150, comment="test"))
    print(calories_calculator.get_calories_remained())
