import os

import pandas as pd


class MainLogic:
    def __init__(self):
        self.df_gaps = None
        self.filter_df_gaps = None
        self.avi_file_name1 = None
        self.avi_file_name2 = None
        self.csv_file_name = None
        self.folder = None

        self.RAILS = ["обе нити", "левая нить", "правая нить"]
        self.current_rail = "обе нити"
        self.gap_limit = 0

    def open_avi(self, file_name1, file_name2, cadr_count):
        self.avi_file_name1 = file_name1
        self.avi_file_name2 = file_name2
        csv_file_name = self.generate_data(cadr_count)
        return csv_file_name

    def open_csv(self, file_name):
        if not os.path.exists(file_name):
            return
        self.csv_file_name = file_name
        self.folder = os.path.dirname(self.csv_file_name)
        self.df_gaps = pd.read_csv(
            self.csv_file_name,
            sep=";",
            names=["rail", "kilometer", "meter", "gap", "file_name", "cadr"],
            dtype={
                "rail": str,
                "kilometer": int,
                "meter": int,
                "gap": int,
                "file_name": str,
                "cadr": int,
            },
        )
        return True

    def filter(self):
        if self.df_gaps is None:
            return
        if self.current_rail == "обе нити":
            self.filter_df_gaps = self.df_gaps
        elif self.current_rail == "левая нить":
            self.filter_df_gaps = self.df_gaps[self.df_gaps["rail"] == "Л"]
        elif self.current_rail == "правая нить":
            self.filter_df_gaps = self.df_gaps[self.df_gaps["rail"] == "П"]
        self.filter_df_gaps = self.filter_df_gaps[
            self.filter_df_gaps["gap"] >= self.gap_limit
        ]

    def generate_data(self, cadr_count):
        from gaps_detection import generate_data

        return generate_data(self.avi_file_name1, self.avi_file_name2, cadr_count)
