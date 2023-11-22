#####################################################################################################################################################
# FOR RENDERING 
# Version 0.1                                                                                                                      
#####################################################################################################################################################

# Standard library imports
import warnings

# Third party library imports
import pandas as pd
from rich.box import SIMPLE
from rich.table import Table
from rich.style import Style
from rich.panel import Panel
from rich import print as pprint

# Local application imports
# --- NONE ---

# ===================================================================================================================================================
def render_df(df):


    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # instantiating various things, configuring
    warnings.simplefilter(action='ignore', category=FutureWarning) # just doing this for now I promise
    df.reset_index(inplace=True, drop=False)
    df.rename(columns={"Account": "ACCOUNT",
                       "Year": "YEAR",
                       "yoy_growth": "YOY\nGROWTH",
                       "gizmo_mix": "GIZMO\nMIX",
                       "Source": "SOURCE",
                       "Sales": "SALES\n(USD)",
                        }, inplace=True)
    df.fillna(" ", inplace=True)
    table = Table(show_footer=False, header_style='bright_white', box=SIMPLE)
    columns = df.columns
    rows = df.values
    rws = rows.copy() # need this for regime mgmt
    _format = Style(bgcolor="grey15")
    _other_format = Style(bgcolor="grey19")
    _red_green = ["YOY\nGROWTH"]
    _regime = ""
    _regime2 = ""

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # formatting each cell... I like the spaces for readability
    for row in range(len(rows)):
        
        # lol... obviously there must be a better way to do this (i.e. something that's readable), but this came to mind first...
        if row == 0:
            _regime = rows[row][0]
            _regime2 = rows[row][1]
        # first regime for SOURCE
        if rows[row][0] == _regime and row != 0:
            rows[row][0] = ""
        elif rows[row][0] != _regime and row != 0:
            _regime = rows[row][0]
        # second regime for ACCOUNT
        if rows[row][1] == _regime2 and row != 0:
            rows[row][1] = ""
        elif rows[row][1] != _regime2 and row != 0:
            _regime2 = rows[row][1]

        # this part is lit
        for cell in range(len(rows[row])):

            match rows[row][cell]:
                
                case str() if columns[cell] == "ACCOUNT" or columns[cell] == "YEAR":
                    rows[row][cell] = f'[bright_white]{rows[row][cell]}[/bright_white]'

                case str() if rows[row][cell] == " ":
                    rows[row][cell] = f"[bright_white]{f'N/A':>9}[/bright_white]"

                case float() if columns[cell] == "SALES\n(USD)":
                    rows[row][cell] = f"[bright_white]{f'{rows[row][cell]:,.2f}':>9}[/bright_white]"
                    
                case float() if columns[cell] in _red_green and rows[row][cell] < 0:
                    rows[row][cell] = f"[#FF5555]{f'({rows[row][cell]*-100:,.1f})%':>9}[/#FF5555]"

                case float() if columns[cell] in _red_green and rows[row][cell] > 0:
                    rows[row][cell] = f"[#50FA7B]{f'{rows[row][cell]*100:,.1f} %':>9}[/#50FA7B]"
                
                case float():
                    rows[row][cell] = f"[#FFFFA5]{f'{rows[row][cell]*100:,.1f} %':>9}[/#FFFFA5]"

                case _:
                    rows[row][cell] = f'[bright_white]{rows[row][cell]}[/bright_white]'

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # Formatting column widths and justifications
    for column in columns:
        if column == "YOY\nGROWTH" or column == "GIZMO\nMIX" or column == "SALES\n(USD)":
            table.add_column(str(column), justify="right", min_width=9, max_width=13)
        elif column == "YOY\nGROWTH" or column == "YEAR":
            table.add_column(str(column), justify="right", min_width=6, max_width=6)
        else:
            table.add_column(str(column), justify="left", min_width=9, max_width=11)

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # just don't ask okay... this is effed... but its for managing background color and spacing between rows
    for row in range(len(rws)):
        if row == 0:
            _regime = rws[row][0]
            _regime2 = rws[row][1]
        elif rws[row][0] != _regime:
            _regime = rws[row][0]
            table.add_row(style=_format) # this is just a spacer 
            _format, _other_format = _other_format, _format # main format switcher
        if rws[row][1] != _regime2:
            _regime2 = rws[row][1]
            if rws[(row-1)][0] == rws[row][0]:
                table.add_row(style=_format) # this is just a spacer 
        # okay lets actually write the row now:
        table.add_row(*list(rows[row]), style=_format)

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    pprint(Panel(table, expand=False, border_style= '#282A36'))
    