import pandas as pd
import numpy as np
from shiny import reactive

class DataManager:
    def __init__(self):
        self.data = reactive.Value(None)
        self.__default_data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGybeaYEQpfKUPm8Uj2i-1NJaWFTfOfW0azSCCGxprB2WBQzQOpzQ5gh9z8uojmKNM5w11xQrz_AHf/pub?output=csv"

    def load_default_data(self):
        self.load_data_from_url(self.get_default_data_url())

    def load_data_from_url(self, url):
        if not url:
            raise ValueError("No URL provided.")
        try:
            df = pd.read_csv(url)
            # Ensure required columns exist
            required_columns = {'Day', 'Exercise', 'Set', 'Weight', 'Reps', 'Cycle'}
            if not required_columns.issubset(df.columns):
                missing_cols = required_columns - set(df.columns)
                raise ValueError(f"Data is missing required columns: {missing_cols}")
            # Ensure correct data types
            df['Cycle'] = df['Cycle'].astype(int)
            df['Set'] = df['Set'].astype(int)
            df['Weight'] = df['Weight'].astype(float)
            df['Reps'] = df['Reps'].astype(int)
            df['Day'] = df['Day'].astype(str)
            df['Exercise'] = df['Exercise'].astype(str)
            self.data.set(df)
        except Exception as e:
            self.data.set(None)
            raise e

    def get_days(self):
        if self.data.get() is not None:
            return sorted(self.data.get()['Day'].unique())
        else:
            return []

    def get_exercises_for_day(self, day):
        if self.data.get() is not None and day is not None:
            return sorted(self.data.get()[self.data.get()['Day'] == day]['Exercise'].unique())
        else:
            return []

    def get_cycle_range(self):
        if self.data.get() is not None:
            return int(self.data.get()['Cycle'].min()), int(self.data.get()['Cycle'].max())
        else:
            return 0, 1

    def filter_data_progress_plot(self, day, exercise, cycle_range):
        df = self.data.get()
        filtered_df = df[
            (df['Day'] == day) &
            (df['Exercise'] == exercise) &
            (df['Cycle'] >= cycle_range[0]) &
            (df['Cycle'] <= cycle_range[1])
            ]
        df_grouped = filtered_df.groupby('Cycle')[['Weight', 'Reps']].mean().reset_index()
        return df_grouped

    def filter_data_summary_plot(self, day):
        df = self.data.get()
        df = df[df["Day"] == day]
        # Step 1: Calculate baseline weight and reps for every exercise during Cycle 1
        baseline = (
            df[df["Cycle"] == 1]
            .groupby("Exercise")[["Weight", "Reps"]]
            .mean()
            .rename(columns=lambda x: f"Baseline_{x}")
            .reset_index()
        )

        # Step 2: Calculate improvement in Weight and Reps over baseline as a percentage for every set
        df = df.merge(baseline, on="Exercise", how="left")
        df["Weight_Improvement"] = (df["Weight"] - df["Baseline_Weight"]) / df["Baseline_Weight"] * 100
        df["Reps_Improvement"] = (df["Reps"] - df["Baseline_Reps"]) / df["Baseline_Reps"] * 100

        # Step 3: Calculate average improvements across sets for Weight and Reps for each exercise and cycle
        average_improvement_df = (
            df.groupby(["Exercise", "Cycle"])[["Weight_Improvement", "Reps_Improvement"]]
            .mean()
            .reset_index()
        )

        # Step 4: Take the maximum of average weight improvement or reps improvement as the true improvement
        average_improvement_df["True_Improvement"] = average_improvement_df[
            ["Weight_Improvement", "Reps_Improvement"]
        ].max(axis=1)

        # Step 5: Final Output
        print(average_improvement_df)

        return average_improvement_df

    def filter_data(self, day, exercise, cycle_range):
        if self.data.get() is None or day is None or exercise is None or cycle_range is None:
            return pd.DataFrame()
        df = self.data.get()
        filtered_df = df[
            (df['Day'] == day) &
            (df['Exercise'] == exercise) &
            (df['Cycle'] >= cycle_range[0]) &
            (df['Cycle'] <= cycle_range[1])
        ].copy()
        if not filtered_df.empty:
            filtered_df['TotalWeightMoved'] = filtered_df['Weight'] * filtered_df['Reps']
        return filtered_df

    def filter_data_for_change_plot(self, day, cycle_range):
        if self.data.get() is None or day is None or cycle_range is None:
            return pd.DataFrame()
        df = self.data.get()
        filtered_df = df[
            (df['Day'] == day) &
            (df['Cycle'] >= cycle_range[0]) &
            (df['Cycle'] <= cycle_range[1])
        ].copy()
        if not filtered_df.empty:
            filtered_df['TotalWeightMoved'] = filtered_df['Weight'] * filtered_df['Reps']
        return filtered_df

    def data_loaded(self):
        if self.data.get() is None:
            return False
        else:
            return True

    def get_default_data_url(self):
        return self.__default_data_url