""" test_transform_data.py

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import os
import unittest

from transform_data import parse_url, read_gdelt


class TestParseURL(unittest.TestCase):

    def test_general_urls(self):
        # Test cases with expected outputs
        test_cases = [
            (
                "https://www.yahoo.com/news/russian-military-convoy-blocked-entering.html",
                "russian military convoy blocked entering",
            ),
            (
                "https://www.den-ver-post.com/2025/02/11/king-soopers-union-strike-lawsuit-restraining-order-A9999999/",
                "king soopers union strike lawsuit restraining order",
            ),
            (
                "https://www.yahoo.com/news/russian---military--convoy-blocked-entering.html",
                "russian military convoy blocked entering",
            ),
            (
                "https://www.express.co.uk/showbiz/tv-radio/2013452/call-the-midwife-georgie-glen-miss-higgins",
                "call the midwife georgie glen miss higgins",
            ),
            (
                "https://www.springfieldnewssun.com/nation-world/spirit-airlines-rejects-takeover-bid-from-rival-frontier-again/SC5JH7FMUFFQ7AI3QNNLTXMW2Y/",
                "spirit airlines rejects takeover bid from rival frontier again",
            ),
            (
                "https://www.yahoo.com/news/elon-musk-deep-state-agent-191258196.html",
                None,
            ),
            (
                "https://www.finanznachrichten.de/nachrichten-2025-02/64536797-cyera-extends-leadership-team-with-key-executive-appointments-004.htm",
                None,
            ),
        ]

        for url, expected_title in test_cases:
            actual_title = parse_url(url)
            self.assertEqual(actual_title, expected_title, f"Failed for URL: {url}")

    def test_return_none(self):
        test_cases = [
            "https://www.yahoo.com/news/russian-military-convoy-blocked-entering-12345678.html",
            "https://www.den-ver-post.com/2025/02/11/king-soopers-union-strike-lawsuit-restraining-order-A89999999/",
            "https://www.example.com/",
            "https://www.example.com/short-url/",
        ]
        for url in test_cases:
            actual_title = parse_url(url)
            self.assertIsNone(actual_title, f"Failed for URL: {url}")

    def test_gdelt_urls(self):
        test_cases = [
            (
                "https://www.ulladullatimes.com.au/story/8890316/stephen-jones-reveals-hes-a-survivor-of-child-sex-abuse/?cs=300",
                "stephen jones reveals hes a survivor of child sex abuse",
            ),
            (
                "https://www.fox13memphis.com/news/man-accused-of-killing-jimmie-jay-lee-faces-new-charges-after-discovery-of-body/article_fa4742a4-e8ac-11ef-8781-5fdff75547ba.html",
                "man accused of killing jimmie jay lee faces new charges after discovery of body",
            ),
            (
                "https://www.jdsupra.com/legalnews/divided-ninth-circuit-panel-upholds-5555677/",
                "divided ninth circuit panel upholds",
            ),
            (
                "https://www.fairfieldsuntimes.com/news/state/personhood-bill-moves-to-montana-house-floor/article_0d73ddd8-4496-5d55-8010-da2c3205b0a1.html",
                "personhood bill moves to montana house floor",
            ),
            (
                "http://www.businessghana.com/site/news/business/322857/African-Energy-Week-2025-to-Highlight-MSGBC-Gas-Boom-as-Greater-Tortue-Ahmeyim-(GTA)-Achieves-...",
                "african energy week 2025 to highlight msgbc gas boom as greater tortue ahmeyim (gta) achieves",
            ),
            (
                "https://www.defenseone.com/threats/2025/02/the-d-brief-february-12-2025/402951/",
                "the d brief february 12 2025",
            ),
        ]
        for url, expected_title in test_cases:
            actual_title = parse_url(url)
            self.assertEqual(actual_title, expected_title, f"Failed for URL: {url}")


class TestReadGDELT(unittest.TestCase):

    def setUp(self):
        data_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )
        self.df1 = read_gdelt(data_folder, "20250212.export.CSV")
        self.df2 = read_gdelt(data_folder, "20250213.export.CSV")

        self.expected_columns = [
            "SQLDATE",
            "EventCode",
            "QuadClass",
            "GoldsteinScale",
            "ActionGeo_FullName",
            "SOURCEURL",
            "Text",
        ]

    def test_check_columns_df1(self):
        self.assertListEqual(list(self.df1.columns), self.expected_columns)

        # Check column types:
        # SQLDATE (str), EventCode (int), QuadClass (int), GoldsteinScale (float),
        # ActionGeo_FullName (str), and SOURCEURL (str)
        self.assertEqual(self.df1["SQLDATE"].dtype, object)
        self.assertEqual(self.df1["EventCode"].dtype, int)
        self.assertEqual(self.df1["QuadClass"].dtype, int)
        self.assertEqual(self.df1["GoldsteinScale"].dtype, float)
        self.assertEqual(self.df1["ActionGeo_FullName"].dtype, object)
        self.assertEqual(self.df1["SOURCEURL"].dtype, object)

    def test_check_columns_df2(self):
        self.assertEqual(self.df2["SQLDATE"].dtype, object)
        self.assertEqual(self.df2["EventCode"].dtype, int)
        self.assertEqual(self.df2["QuadClass"].dtype, int)
        self.assertEqual(self.df2["GoldsteinScale"].dtype, float)
        self.assertEqual(self.df2["ActionGeo_FullName"].dtype, object)
        self.assertEqual(self.df2["SOURCEURL"].dtype, object)

    def test_check_index(self):
        expected_rows_df1 = 20159
        expected_rows_df2 = 20363

        self.assertEqual(len(self.df1), expected_rows_df1)
        self.assertEqual(len(self.df2), expected_rows_df2)

    def test_check_entries_df1(self):
        event_id1 = str(1226184510)
        expected_event_code1 = 172
        self.assertEqual(self.df1.loc[event_id1]["EventCode"], expected_event_code1)

        event_id2 = str(1226184479)
        expected_event_code2 = 20
        self.assertEqual(self.df1.loc[event_id2]["EventCode"], expected_event_code2)

    def test_check_entries_df2(self):
        event_id1 = str(1226185180)
        expected_event_code1 = 841
        self.assertEqual(self.df2.loc[event_id1]["EventCode"], expected_event_code1)

        event_id2 = str(1226185426)
        expected_event_code2 = 40
        self.assertEqual(self.df2.loc[event_id2]["EventCode"], expected_event_code2)


if __name__ == "__main__":
    unittest.main()
