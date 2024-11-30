import pandas as pd
import shiny
from shiny import App, render, ui
import matplotlib.pyplot as plt
import seaborn as sns

def get_ui_preload():
    app_ui = ui.page_fluid(
        ui.h2("Workout Data Analysis"),
        ui.input_text(
            id='data_url',
            label='Enter Data URL:',
            value='',
            placeholder='Paste your CSV data URL here'
        ),
        ui.row(
            ui.column(
                4,
                ui.input_action_button(
                    id='load_data',
                    label='Load Data'
                )
            ),
            ui.column(
                4,
                ui.input_action_button(
                    id='load_default_data',
                    label='Load Default Data'
                )
            )
        ),
        ui.hr(),
        ui.output_ui('main_ui')  # Placeholder for main UI content
    )

    return app_ui

def get_main_content_ui(data_manager):
    return ui.navset_pill(
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
                    'weight_plot': 'Weight Plot',
                    'reps_plot': 'Reps Plot',
                    'total_weight_plot': 'Total Weight Moved Plot'
                },
                selected=['weight_plot', 'reps_plot', 'total_weight_plot']
            ),
            ui.output_ui('plots_ui'),
            ui.output_table("data_table")
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

def get_main_ui(data_manager):
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

def get_ui(data):
    app_ui = ui.page_fluid(
        ui.h2("Workout Data Analysis"),
        ui.input_text(
            id='data_url',
            label='Enter Data URL:',
            value='',
            placeholder='Paste your CSV data URL here'
        ),
        ui.row(
            ui.column(
                4,
                ui.input_action_button(
                    id='load_data',
                    label='Load Data'
                )
            ),
            ui.column(
                4,
                ui.input_action_button(
                    id='load_default_data',
                    label='Load Default Data'
                )
            )
        ),
        ui.hr(),
        ui.navset_pill(
            ui.nav_panel(
                "Exercise Analysis",
                # Inputs specific to this tab
                ui.input_select(
                    id='day_select',
                    label='Select Day:',
                    choices=sorted(data['Day'].unique()),
                    selected=sorted(data['Day'].unique())[0]
                ),
                ui.output_ui('exercise_ui'),
                ui.input_slider(
                    id='cycle_slider',
                    label='Select Cycle Range:',
                    min=data['Cycle'].min(),
                    max=data['Cycle'].max(),
                    value=(data['Cycle'].min(), data['Cycle'].max()),
                    step=1
                ),
                ui.input_checkbox_group(
                    id='charts_select',
                    label='Select Charts to Display:',
                    choices={
                        'weight_plot': 'Weight Plot',
                        'reps_plot': 'Reps Plot',
                        'total_weight_plot': 'Total Weight Moved Plot'
                    },
                    selected=['weight_plot', 'reps_plot', 'total_weight_plot']
                ),
                ui.output_ui('plots_ui'),
                ui.output_table("data_table")
            ),
            ui.nav_panel(
                "Exercise Change Analysis",
                # Inputs specific to this tab
                ui.input_select(
                    id='day_select_change',
                    label='Select Day:',
                    choices=sorted(data['Day'].unique()),
                    selected=sorted(data['Day'].unique())[0]
                ),
                ui.input_slider(
                    id='cycle_slider_change',
                    label='Select Cycle Range:',
                    min=data['Cycle'].min(),
                    max=data['Cycle'].max(),
                    value=(data['Cycle'].min(), data['Cycle'].max()),
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
    )

    return app_ui