import unittest
from datetime import date
from egyid import EgyptianNationalId


class TestEgyptianNationalId(unittest.TestCase):
    def test_valid_id(self):
        # The last digit is a check digit, calculated using the standard Egyptian national ID algorithm.
        self.assertTrue(EgyptianNationalId.is_valid_id("29001011400014"))

    def test_invalid_id(self):
        self.assertFalse(EgyptianNationalId.is_valid_id("00000000000000"))

    def test_generate_valid(self):
        generated = EgyptianNationalId.generate({"year": 1990, "gender": "male", "governorate": "01"})
        self.assertTrue(EgyptianNationalId.is_valid_id(generated))


class TestEgyptianNationalIdComprehensive(unittest.TestCase):
    """Comprehensive test suite for Egyptian National ID validation and parsing."""

    def test_valid_ids(self):
        """Test various valid Egyptian National IDs."""
        valid_ids = [
            "29001011400014",  # 1990-01-01, Kalyubia, male
            "29010280165195",  # 1990-10-28, Cairo, male
            "30105201501238",  # 2001-05-20, Cairo, female
            "28801010100001",  # 1988-01-01, Cairo, male (adjusted checksum)
            "29512310123455",  # 1995-12-31, Cairo, female
        ]
        for id_str in valid_ids:
            with self.subTest(id=id_str):
                self.assertTrue(EgyptianNationalId.is_valid_id(id_str))
                eid = EgyptianNationalId(id_str)
                self.assertTrue(eid.is_valid())
                self.assertIsNotNone(eid.birth_date)
                self.assertIn(eid.gender, ['male', 'female'])
                self.assertIsNotNone(eid.governorate)

    def test_invalid_lengths(self):
        """Test IDs with wrong lengths."""
        invalid_lengths = [
            "123",           # Too short
            "2900101140001", # 13 digits
            "290010114000145", # 15 digits
            "",              # Empty
        ]
        for id_str in invalid_lengths:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_invalid_century_digits(self):
        """Test IDs with invalid century digits."""
        invalid_centuries = [
            "19001011400014",  # Starts with 1
            "49001011400014",  # Starts with 4
            "09001011400014",  # Starts with 0
        ]
        for id_str in invalid_centuries:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_invalid_dates(self):
        """Test IDs with invalid birth dates."""
        invalid_dates = [
            "29023011400014",  # Feb 30 (invalid)
            "29023111400014",  # Feb 31 (invalid)
            "29013211400014",  # Jan 32 (invalid)
            "29001311400014",  # Month 13 (invalid)
            "29010011400014",  # Month 00 (invalid)
            "29000111400014",  # Day 00 (invalid)
        ]
        for id_str in invalid_dates:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_future_dates(self):
        """Test IDs with future birth dates."""
        # Assuming current year is 2026, future dates should be invalid
        future_ids = [
            "33601011400018",  # 2033-01-01 (future)
        ]
        for id_str in future_ids:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_invalid_governorates(self):
        """Test IDs with invalid governorate codes."""
        invalid_govs = [
            "29001000400014",  # Gov 00 (invalid)
            "29001991400014",  # Gov 99 (invalid)
            "29001041400014",  # Gov 41 (invalid)
        ]
        for id_str in invalid_govs:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_invalid_checksums(self):
        """Test IDs with wrong check digits."""
        invalid_checksums = [
            "29001011400015",  # Wrong checksum
            "29001011400013",  # Wrong checksum
            "29001011400010",  # Wrong checksum
        ]
        for id_str in invalid_checksums:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_non_numeric_ids(self):
        """Test IDs with non-numeric characters."""
        non_numeric = [
            "2900101140001a",  # Letter
            "2900101140001 ",  # Space
            "2900101140001-",  # Dash
        ]
        for id_str in non_numeric:
            with self.subTest(id=id_str):
                self.assertFalse(EgyptianNationalId.is_valid_id(id_str))

    def test_arabic_numerals(self):
        """Test IDs with Arabic numerals (should be sanitized)."""
        arabic_id = "٢٩٠١٠٢٨٠١٦٥١٩٥"  # 29010280165195 in Arabic
        self.assertTrue(EgyptianNationalId.is_valid_id(arabic_id))

    def test_parsing_methods(self):
        """Test parsing methods for valid ID."""
        eid = EgyptianNationalId("29010280165195")
        self.assertEqual(eid.get_birth_year(), 1990)
        self.assertEqual(eid.get_birth_month(), 10)
        self.assertEqual(eid.get_birth_day(), 28)
        self.assertEqual(eid.birth_date, date(1990, 10, 28))
        self.assertEqual(eid.gender, "male")
        self.assertEqual(eid.governorate, "Cairo")
        self.assertEqual(eid.region_name, "Cairo")
        self.assertTrue(eid.is_male())
        self.assertFalse(eid.is_female())
        self.assertTrue(eid.is_adult())
        self.assertTrue(eid.is_inside_egypt())

    def test_generation(self):
        """Test ID generation."""
        generated = EgyptianNationalId.generate()
        self.assertTrue(EgyptianNationalId.is_valid_id(generated))
        self.assertEqual(len(generated), 14)

        # Test with options
        male_id = EgyptianNationalId.generate({"gender": "male", "year": 1990, "governorate": "01"})
        self.assertTrue(EgyptianNationalId.is_valid_id(male_id))
        eid = EgyptianNationalId(male_id)
        self.assertEqual(eid.get_birth_year(), 1990)
        self.assertEqual(eid.gender, "male")

    def test_to_dict(self):
        """Test dictionary output."""
        eid = EgyptianNationalId("29010280165195")
        data = eid.to_dict()
        expected = {
            "nationalId": "29010280165195",
            "birthYear": 1990,
            "birthMonth": 10,
            "birthDay": 28,
            "age": 35,  # As of 2025
            "gender": "male",
            "governorate": "Cairo",
            "region": "Cairo",
            "insideEgypt": True,
            "isAdult": True,
        }
        self.assertEqual(data, expected)

    def test_invalid_to_dict(self):
        """Test to_dict returns None for invalid IDs."""
        eid = EgyptianNationalId("00000000000000")
        self.assertIsNone(eid.to_dict())

    def test_class_methods(self):
        """Test class methods for quick checks."""
        self.assertTrue(EgyptianNationalId.check_is_male("29010280165195"))
        self.assertFalse(EgyptianNationalId.check_is_female("29010280165195"))
        self.assertTrue(EgyptianNationalId.check_is_adult("29010280165195"))

        self.assertFalse(EgyptianNationalId.check_is_male("30105201501220"))  # Female
        self.assertTrue(EgyptianNationalId.check_is_female("30105201501220"))

    def test_sanitization(self):
        """Test ID sanitization."""
        self.assertEqual(EgyptianNationalId.sanitize("29001011400014"), "29001011400014")
        self.assertEqual(EgyptianNationalId.sanitize("٢٩٠٠١٠١١٤٠٠٠١٤"), "29001011400014")
        self.assertEqual(EgyptianNationalId.sanitize("290-010-114-000-14"), "29001011400014")

    def test_edge_cases(self):
        """Test various edge cases."""
        # Leap year
        leap_id = "29602291400018"  # 1996-02-29
        self.assertTrue(EgyptianNationalId.is_valid_id(leap_id))

        # Non-leap year Feb 29
        invalid_leap = "29702291400014"  # 1997-02-29 (invalid)
        self.assertFalse(EgyptianNationalId.is_valid_id(invalid_leap))

        # Century boundary
        century_1900 = "29912311400019"  # 1999-12-31
        self.assertTrue(EgyptianNationalId.is_valid_id(century_1900))

        century_2000 = "30101011400014"  # 2001-01-01
        self.assertTrue(EgyptianNationalId.is_valid_id(century_2000))

    def test_foreign_governorate(self):
        """Test IDs from outside Egypt."""
        foreign_id = "29001018800018"  # Gov 88 (Outside Republic)
        eid = EgyptianNationalId(foreign_id)
        self.assertEqual(eid.governorate, "Outside the Republic")
        self.assertEqual(eid.region_name, "Foreign")
        self.assertFalse(eid.is_inside_egypt())


if __name__ == "__main__":
    unittest.main()
