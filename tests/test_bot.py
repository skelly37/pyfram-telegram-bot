import unittest
from api_calls import WolframBot
import os

class BotsTests(unittest.TestCase):
    API_KEYS = [x.strip() for x in open("./api_key.txt").readlines()]
    wb = WolframBot(API_KEYS)

    def __get_image(self, query, step_by_step=False, force=False):
        if step_by_step:
            return self.wb.get_step_by_step(query)
        else:
            return self.wb.query_wolfram(query, force)

    def __get_image_data(self, query, step_by_step=False, force=False):
        filename = self.__get_image(query, step_by_step, force)
        if filename.startswith(self.wb.RESULT_SAVED_MSG):
            filename = filename.replace(self.wb.RESULT_SAVED_MSG, "")
            file_size = os.path.getsize(filename)
            return dict(name=filename, empty=(file_size==0))

        return filename


    def test_wolframbot(self):
        self.assertEqual(self.wb.query_wolfram("2+2"), "4")                                                                     # short answers
        self.assertEqual(self.__get_image_data("x^2 chart"),
                         {"name": "x^2 chart.png", "empty": False})                                                             # fallback to image in default mode correct


        self.assertEqual(self.wb.query_wolfram("2+2", inline_mode=True), "4")                                                   # inline mode correct
        self.assertEqual(self.wb.query_wolfram("x^2 chart", inline_mode=True), self.wb.NO_SHORT_MSG)                            # inline mode incorrect


        self.assertEqual(self.__get_image_data("x^2 chart", force=True),
                         {"name": "x^2 chart.png", "empty": False})                                                             # forced image correct
        self.assertEqual(self.__get_image_data("2qi42df3bf328yf2d wpqd32 9e7 31 3c", force=True), self.wb.ERROR_MSG)            # forced image incorrect

        print("Testing step-by-step solutions... Be patient.")
        self.assertEqual(self.__get_image_data("2+2", step_by_step=True),
                         {"name": "2+2.png", "empty": False})                                                                   # step by step correct
        print("Testing second step-by-step solution...")
        self.assertEqual(self.__get_image_data("x^2 chart", step_by_step=True), self.wb.NO_STEPS_MSG)                           # step by step incorrect

    def test_pyfram_bot(self):
        pass
        #TODO pyfram_bot.py tests


if __name__ == '__main__':
    unittest.main()
