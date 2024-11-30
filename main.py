import pandas as pd
import shiny
from shiny import App, render, ui, reactive
import matplotlib.pyplot as plt
import seaborn as sns
import Plotter
import DashboardUI
from DashboardUI import get_ui
from DataManager import DataManager




CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGybeaYEQpfKUPm8Uj2i-1NJaWFTfOfW0azSCCGxprB2WBQzQOpzQ5gh9z8uojmKNM5w11xQrz_AHf/pub?output=csv"

def load_data():
    data = pd.read_csv(CSV_URL)
    # Ensure 'Cycle' is an integer
    data['Cycle'] = data['Cycle'].astype(int)
    return data

# Initialize data
data = load_data()

#Publish Your Google Sheet to the Web:

#Open your Google Sheet.
#Go to File > Share > Publish to the web.
#Choose Entire Document and select Comma-separated values (.csv) as the format.
#Click Publish and confirm.

app_ui = get_ui(data)

# Define the server logic
def server(input, output, session):

    # Use reactive values to store data
    data_manager = DataManager()

    # Function to load data from a given URL
    """
    def load_data_from_url(url):
        if not url:
            ui.notification_show("Please enter a data URL.", type="warning")
            data_store.set(None)
            return
        try:
            df = pd.read_csv(url)
            # Ensure required columns exist
            required_columns = {'Day', 'Exercise', 'Set', 'Weight', 'Reps', 'Cycle'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Data must contain the following columns: {required_columns}")
            # Ensure correct data types
            df['Cycle'] = df['Cycle'].astype(int)
            df['Set'] = df['Set'].astype(int)
            df['Weight'] = df['Weight'].astype(float)
            df['Reps'] = df['Reps'].astype(int)
            df['Day'] = df['Day'].astype(str)
            df['Exercise'] = df['Exercise'].astype(str)
            data_store.set(df)
            ui.notification_show("Data loaded successfully!", type="message")

            # Update UI elements with new data
            # Update Day selectors
            session.send_input_message(
                'day_select',
                {'choices': sorted(df['Day'].unique()), 'selected': sorted(df['Day'].unique())[0]}
            )
            session.send_input_message(
                'day_select_change',
                {'choices': sorted(df['Day'].unique()), 'selected': sorted(df['Day'].unique())[0]}
            )
            # Update Cycle sliders
            min_cycle = int(df['Cycle'].min())
            max_cycle = int(df['Cycle'].max())
            session.send_input_message(
                'cycle_slider',
                {'min': min_cycle, 'max': max_cycle, 'value': [min_cycle, max_cycle]}
            )
            session.send_input_message(
                'cycle_slider_change',
                {'min': min_cycle, 'max': max_cycle, 'value': [min_cycle, max_cycle]}
            )
        except Exception as e:
            ui.notification_show(f"Error loading data: {str(e)}", type="error")
            data_store.set(None)
    """

    # Reactive expression to load data when 'Load Data' button is clicked
    @reactive.Effect
    @reactive.event(input.load_data, ignore_none=True)
    def handle_load_data():
        data_manager.load_data_from_url(input.data_url())
        #DashboardUI.get_main_ui(data_manager)
        update_ui()

    # Reactive expression to load default data when 'Load Default Data' button is clicked
    @reactive.Effect
    @reactive.event(input.load_default_data)
    def handle_load_default_data():
        session.send_input_message('data_url', {'value': data_manager.get_default_data_url()})
        data_manager.load_default_data()
        update_ui()


    @output
    @render.ui
    def main_content():
        df = data_manager.data.get()
        if df is None:
            return ui.h4("Please load data to proceed.")
        else:
            return DashboardUI.get_main_content_ui(data_manager)

    # Dynamic Exercise Selector based on selected Day
    @output
    @render.ui
    def exercise_ui():
        df = data_manager.data.get()
        if df is None:
            return ui.h4("Please load data to proceed.")
        selected_day = input.day_select()
        if selected_day is None:
            return ui.h4("Please select a Day.")
        exercises_in_day = data_manager.get_exercises_for_day(selected_day)
        if not exercises_in_day:
            return ui.h4("No exercises available for the selected Day.")
        return ui.input_select(
            id='exercise_select',
            label='Select Exercise:',
            choices=exercises_in_day,
            selected=exercises_in_day[0]
        )

    def update_ui():
        # Update Day selectors
        days = data_manager.get_days()
        if not days:
            return
        session.send_input_message(
            'day_select',
            {'choices': days, 'selected': days[0]}
        )
        session.send_input_message(
            'day_select_change',
            {'choices': days, 'selected': days[0]}
        )
        # Update Cycle sliders
        min_cycle, max_cycle = data_manager.get_cycle_range()
        session.send_input_message(
            'cycle_slider',
            {'min': min_cycle, 'max': max_cycle, 'value': [min_cycle, max_cycle]}
        )
        session.send_input_message(
            'cycle_slider_change',
            {'min': min_cycle, 'max': max_cycle, 'value': [min_cycle, max_cycle]}
        )

    def filter_data():
        df = data_manager.data.get()
        # Apply filters
        selected_exercise = input.exercise_select()
        cycle_range = input.cycle_slider()

        filtered_df = df[
            (df['Exercise'] == selected_exercise) &
            (df['Cycle'] >= cycle_range[0]) &
            (df['Cycle'] <= cycle_range[1])
            ]

        # Calculate Total Weight Moved for each set
        filtered_df = filtered_df.copy()
        filtered_df['TotalWeightMoved'] = filtered_df['Weight'] * filtered_df['Reps']
        print(filtered_df)

        return filtered_df

    @reactive.Effect
    @reactive.event(input.refresh_data)
    def _():
        # Reload data when the refresh button is clicked
        new_data = load_data()
        data_store.set(new_data)
        # Update UI components based on the new data
        ui.update_select(
            'exercise_select',
            choices=sorted(new_data['Exercise'].unique()),
            selected=input.exercise_select()
        )
        ui.update_slider(
            'cycle_slider',
            min=new_data['Cycle'].min(),
            max=new_data['Cycle'].max(),
            value=input.cycle_slider()
        )

    @output
    @render.plot
    def weight_plot():
        filtered_df = filter_data()
        if filtered_df.empty:
            return
        # Aggregate data by 'Cycle'
        df_grouped = filtered_df.groupby('Cycle')['Weight'].mean().reset_index()
        Plotter.weight_plot(df_grouped, input.exercise_select())

    @output
    @render.plot
    def reps_plot():
        filtered_df = filter_data()
        if filtered_df.empty:
            return
        # Aggregate data by 'Cycle'
        df_grouped = filtered_df.groupby('Cycle')['Reps'].mean().reset_index()
        Plotter.reps_plot(df_grouped, input.exercise_select())

    @output
    @render.plot
    def total_weight_plot():
        filtered_df = filter_data()
        if filtered_df.empty:
            # Return a blank figure or a message
            plt.figure()
            plt.text(0.5, 0.5, 'No data available for the selected filters.', horizontalalignment='center',
                     verticalalignment='center')
            plt.axis('off')
            return
        # Aggregate total weight moved by cycle
        df_grouped = filtered_df.groupby('Cycle')['TotalWeightMoved'].sum().reset_index()
        Plotter.total_weight_moved_plot(df_grouped, input.exercise_select())

    # Dynamic Plots UI based on selected charts
    @output
    @render.ui
    def plots_ui():
        selected_charts = input.charts_select()
        plot_outputs = []

        if 'weight_plot' in selected_charts:
            plot_outputs.append(ui.output_plot('weight_plot'))
        if 'reps_plot' in selected_charts:
            plot_outputs.append(ui.output_plot('reps_plot'))
        if 'total_weight_plot' in selected_charts:
            plot_outputs.append(ui.output_plot('total_weight_plot'))

        # If no charts are selected, display a message
        if not plot_outputs:
            return ui.h4("No charts selected.")

        return ui.TagList(*plot_outputs)

    # Change Plot (Second Tab)
    @output
    @render.plot
    def change_plot():
        plt.close('all')
        df = data_manager.data.get()
        selected_day = input.day_select_change()
        cycle_range = input.cycle_slider_change()

        filtered_df = df[
            (df['Day'] == selected_day) &
            (df['Cycle'] >= cycle_range[0]) &
            (df['Cycle'] <= cycle_range[1])
            ].copy()

        if filtered_df.empty:
            plt.figure()
            plt.text(0.5, 0.5, 'No data available for the selected filters.',
                     horizontalalignment='center', verticalalignment='center')
            plt.axis('off')
            return

        # Calculate Total Weight Moved for each set
        filtered_df['TotalWeightMoved'] = filtered_df['Weight'] * filtered_df['Reps']

        metric = input.metric_select_change()

        print(f"Selected metric: {metric}")

        # Determine the column to use based on selected metric
        if metric == 'Avg. Weight':
            metric_column = 'Weight'
        elif metric == 'Avg. Reps':
            metric_column = 'Reps'
        elif metric == 'Total Weight Moved':
            metric_column = 'TotalWeightMoved'
        else:
            metric_column = 'TotalWeightMoved'  # Default

        # Group data by Exercise and Cycle
        df_grouped = filtered_df.groupby(['Exercise', 'Cycle'])[metric_column].mean().reset_index()

        print(df_grouped)

        # Get the metric values for the first and last cycle for each exercise
        first_cycle = filtered_df['Cycle'].min()
        last_cycle = filtered_df['Cycle'].max()

        df_first = df_grouped[df_grouped['Cycle'] == first_cycle][['Exercise', metric_column]].rename(
            columns={metric_column: 'FirstValue'})
        df_last = df_grouped[df_grouped['Cycle'] == last_cycle][['Exercise', metric_column]].rename(
            columns={metric_column: 'LastValue'})

        # Merge and calculate the change
        df_change = pd.merge(df_first, df_last, on='Exercise')
        df_change['Percent Change'] = ((df_change['LastValue'] - df_change['FirstValue']) / df_change['FirstValue']) * 100

        # Sort exercises by change
        df_change = df_change.sort_values(by='Percent Change', ascending=False)

        # Plot the changes
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df_change['Exercise'], df_change['Percent Change'], color='purple')
        ax.set_xlabel('Percent Change in ' + metric)
        ax.set_ylabel('Exercise')
        ax.set_title(f'Percent Change in {metric} from Cycle {first_cycle} to {last_cycle} on {selected_day}')
        ax.invert_yaxis()  # Highest change on top
        plt.tight_layout()

# Create the Shiny app
app = App(app_ui, server)

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run()