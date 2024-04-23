from linkedin_scraper import DataExtractor

import unittest


class TestDataExtractor(unittest.TestCase):
    def test_get_company_name(self):
        extractor = DataExtractor('Data\Linkedin\jawher-jabri-b640b0176_profile_data.json')
        company_name = extractor.get_company_name()
        self.assertIsNotNone(company_name)
        print(f"Extracted Company Name: {company_name}")

    def test_get_current_position(self):
        extractor = DataExtractor('Data\Linkedin\jawher-jabri-b640b0176_profile_data.json')
        position = extractor.get_current_position()
        self.assertIsNotNone(position)
        print(f"Extracted Current Position: {position}")

if __name__ == '__main__':
    unittest.main()
