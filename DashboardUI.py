import pandas as pd
import shiny
from shiny import App, render, ui
import matplotlib.pyplot as plt
import seaborn as sns
import shinyswatch

def get_ui(data):

    app_ui = ui.page_fluid(
        ui.div(
            ui.h2("Training Dashboard", class_="text-light"),
            ui.h4("for workout data analysis", class_="text-light"),
            ui.column(
                5,
                ui.input_text(
                    id='data_url',
                    label=ui.h6('Enter Data URL:', class_="text-light"),
                    value='',
                    placeholder='Paste your CSV data URL here',
                    width='100%'
                ),
                ui.row(
                    ui.column(
                        6,
                        ui.input_action_button(
                            id='load_data',
                            label='Load Data',
                            width = '100%'
                        )
                    ),
                    ui.column(
                        6,
                        ui.input_action_button(
                            id='load_default_data',
                            label='Load Default Data',
                            width = '100%'
                        )
                    )
                )
            ),
            style="background-color: #008cba; padding: 20px; border-radius: 5px;"  # Add background color and padding
        ),
        ui.hr(),
        ui.output_ui('main_content'),
    theme=shinyswatch.theme.yeti
    )
    return app_ui


def get_main_content_ui(data_manager):
    return ui.navset_pill(
        ui.nav_panel(
            "Summary",
            ui.input_select(
                id='day_select_change',
                label='Select Day:',
                choices=data_manager.get_days()
            ),
            ui.output_plot('summary_plot')
        ),
        ui.nav_panel(
            "Exercise Analysis",
            ui.input_select(
                id='day_select',
                label='Select Day:',
                choices=data_manager.get_days()
            ),
            ui.output_ui('exercise_ui'),
            ui.input_slider(
                id='cycle_slider',
                label='Select Cycle Range:',
                min=data_manager.get_cycle_range()[0],
                max=data_manager.get_cycle_range()[1],
                value=data_manager.get_cycle_range(),
                step=1
            ),
            ui.input_checkbox_group(
                id='charts_select',
                label='Select Charts to Display:',
                choices={
                    'progress_plot': 'Progress Plot',
                    'weight_plot': 'Weight Plot',
                    'reps_plot': 'Reps Plot',
                    'total_weight_plot': 'Total Weight Moved Plot'
                },
                selected=['progress_plot', 'weight_plot', 'reps_plot', 'total_weight_plot']
            ),
            ui.output_ui('plots_ui'),
            ui.output_table("data_table") #todo remove
        ),
        ui.nav_panel(
            "Exercise Change Analysis",
            ui.input_select(
                id='day_select_change',
                label='Select Day:',
                choices=data_manager.get_days()
            ),
            ui.input_slider(
                id='cycle_slider_change',
                label='Select Cycle Range:',
                min=data_manager.get_cycle_range()[0],
                max=data_manager.get_cycle_range()[1],
                value=data_manager.get_cycle_range(),
                step=1
            ),
            ui.input_select(
                id='metric_select_change',
                label='Select Metric for Change Plot:',
                choices=['Avg. Weight', 'Avg. Reps', 'Total Weight Moved'],
                selected='Total Weight Moved'
            ),
            ui.output_plot("change_plot")
        )
    )

def get_main_ui(data_manager): #todo delete
    if not data_manager.data_loaded():
        return ui.h4("Please load data to proceed.")
    else:
        # Define the rest of the UI here, now that data is loaded
        return ui.TagList(
            ui.input_select(
                id='day_select',
                label='Select Day:',
                choices=data_manager.get_days()
            ),
            ui.input_select(
                id='exercise_select',
                label='Select Exercise:',
                choices=[]  # Will be updated based on selected day
            ),
            # Additional UI elements...
            ui.output_plot("my_plot"),
            ui.output_table("data_table")
        )

