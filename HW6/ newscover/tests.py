import unittest
import sys
import newsapi

API_KEY = "22c05da432d1401a922f84a455e251b7"

class CheckNewsAPI(unittest.TestCase):
    def test_no_key_words_fail(self):
        keywords = []
        with self.assertRaises(Exception) as context: 
            newsapi.fetch_latest_news(API_KEY, keywords)
        self.assertTrue("unable to fetch articles" in str(context.exception))

    # def test_valid_timeframe(self):

    # def test_non_alpha_key_word_fail(self): 

if __name__ == ("__main__"):
    unittest.main()