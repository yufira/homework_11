from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value

    def __str__(self):
        return str(self._value)

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value


class Name(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value

    def __str__(self):
        return str(self._value)

    def is_valid(self, value):
        if value.isalpha():
            return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value

    def __str__(self):
        return str(self._value)

    def is_valid(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Invalid phone number format')
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value


class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value

    def __str__(self):
        return str(self._value)

    def is_valid(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError as e:
            raise ValueError(f"Wrong date format: {e}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        try:
            new_number = Phone(phone)
            self.phones.append(new_number)
        except ValueError as e:
            print(f'Error adding phone number: {e}')

    def remove_phone(self, phone):
        phones_to_remove = filter(lambda p: p.value == phone, self.phones)
        for phone in phones_to_remove:
            self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        found = False
        if not new_number.isdigit() or len(new_number) != 10:
            raise ValueError('Invalid phone number format')
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                found = True
                break

        if not found:
            raise ValueError(
                f"Phone number '{old_number}' not found in the record."
                )

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )

    def days_to_birthday(self):
        if self.birthday:
            current_date = datetime.now()
            birthday_this_year = datetime(
                current_date.year,
                self.birthday.value.month,
                self.birthday.value.day
            )
            difference = birthday_this_year - current_date
            if current_date > birthday_this_year:
                birthday_next_year = datetime(
                    current_date.year + 1,
                    self.birthday.value.month,
                    self.birthday.value.day
                )
                difference = birthday_next_year - current_date
            return difference.days
        else:
            return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, record_number):
        counter = 0
        while counter < len(self.data):
            records_slice = list(
                self.data.values()
            )[counter:counter + record_number]
            yield [str(record) for record in records_slice]
            counter += record_number


# address_book = AddressBook()

# records_generator = address_book.iterator(4)
# for i in records_generator:
#     print(i)
