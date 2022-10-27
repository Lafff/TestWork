import re
class ShieldSymbol:
    def __init__(self, shielding_symbol = None):
        if shielding_symbol is None:
            raise ValueError('Не определен экранирующий символ')
        self.shielding_symbol = shielding_symbol

class Email(ShieldSymbol):
    def __call__(self, email):
        name, domain = email.split('@')
        name = self.shielding_symbol * len(name)
        return '@'.join((name,domain))
    

class PhoneNumber(ShieldSymbol):
    def __init__(self, shielding_symbol=None, quantity = 3):
        super().__init__(shielding_symbol)
        self.quantity = quantity
        
    def __call__(self, number):
        number = list(number.replace(' ',''))
        number[-1:-1 - self.quantity:-1] = [self.shielding_symbol for i in range(self.quantity)]
        number = ''.join(number)
        return ' '.join((number[:2], number[2:5], number[5:8], number[8:]))
        
class Skype:
    def __call__(self, skype):
        skype_parts = re.split(':|\?', skype)
        skype_parts[1] = 'x' * 3
        if len(skype_parts) == 2:
            return f'{skype_parts[0]}:{skype_parts[1]}'
        else:
            return f'{skype_parts[0]}:{skype_parts[1]}?{skype_parts[2]}'


