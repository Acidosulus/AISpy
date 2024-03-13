import unittest
import data_sourses

import datetime

def test_positive_case():
    head, data = data_sourses.Agreement_Data(111494)
    print(head)



class TestAgreementData(unittest.TestCase):
    def test_positive_case(self):
        head, data = data_sourses.Agreement_Data(111494)
        self.assertIsNotNone(head)
        self.assertIsNotNone(data)

class TestAgreements_Search_Data(unittest.TestCase):
    def test_positive_case(self):
        head, data = data_sourses.Agreements_Search_Data('олнышко')
        self.assertIsNotNone(head)
        self.assertIsNotNone(data)

class TestPays_from_date_to_date(unittest.TestCase):
    def test_positive_case(self):
        head, data = data_sourses.Pays_from_date_to_date({'from':datetime.date(2023,12,1), 'to':datetime.date(2023,12,31)})
        self.assertIsNotNone(head)
        self.assertIsNotNone(data)

#    def test_negative_case(self):
#        pass


if __name__ == '__main__':
    unittest.main()