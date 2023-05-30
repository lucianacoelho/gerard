import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, MATCH

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "Search", "value": "search"},
                {"label": "Impact", "value": "impact"},
                {"label": "Crosstab", "value": "crosstab"},
                {"label": "Specific Approval", "value": "specific_approval"},
                {"label": "Share", "value": "share"},
                {"label": "Report", "value": "report"},
                {"label": "Decline", "value": "decline"},
                {"label": "Approval", "value": "approval"},
                {"label": "Bin Bank", "value": "bin_bank"},
            ],
        ),
        html.Button("Add", id="add-button", n_clicks=0),
        html.Div(id="card-container", className="card-container"),
    ]
)


def search(transaction_id):
        """
        Searches a transaction by Transaction ID
            Args:
            transaction_id: str, the Transaction ID of the transaction
        """
        with pd.option_context('display.max_rows', None):
            transaction = df[df['Transaction ID'] == transaction_id]
            transaction = transaction.dropna(axis=1).sort_values(by=self.response_column, ascending=False)

            # Get the list of column names and move 'Processor Response Text' to the front
            cols = transaction.columns.tolist()         
            cols.insert(0, cols.pop(cols.index('Processor Response Text')))

            # Reindex the columns
            transaction = transaction.reindex(columns=cols)
            pd.options.display.max_rows = None
            return transaction.T


def impact_method(filter_by, sub_filter):
    # Method implementation
    print("Impact Method")
    print("Filter By:", filter_by)
    print("Sub Filter:", sub_filter)


def crosstab_method(col1, col2):
    # Method implementation
    print("Crosstab Method")
    print("Column 1:", col1)
    print("Column 2:", col2)


def specific_approval_method(filter_by, sub_filter):
    # Method implementation
    print("Specific Approval Method")
    print("Filter By:", filter_by)
    print("Sub Filter:", sub_filter)


def share_method(filter_by, sub_filter):
    # Method implementation
    print("Share Method")
    print("Filter By:", filter_by)
    print("Sub Filter:", sub_filter)


def report_method():
    # Method implementation
    print("Report Method")


def decline_method(columns):
    # Method implementation
    print("Decline Method")
    print("Columns:", columns)


def approval_method(columns):
    # Method implementation
    print("Approval Method")
    print("Columns:", columns)


def bin_bank_method(bin):
    # Method implementation
    print("Bin Bank Method")
    print("Bin:", bin)


@app.callback(
    Output("card-container", "children"),
    Input("add-button", "n_clicks"),
    State("dropdown", "value"),
)
def add_card(n_clicks, dropdown_value):
    if n_clicks == 0:
        raise PreventUpdate

    card_id = f"card-{n_clicks}"


    
    card_content = []
    if dropdown_value == "search":
        card_content = [
        html.H4("Search"),
        html.Label("Transaction ID"),
        dcc.Input(id={"type": "input", "index": n_clicks}, type="text"),
        html.Pre(id={"type": "result", "index": n_clicks}),
    ]

    elif dropdown_value == "impact":
        card_content = impact_method_inputs()
    elif dropdown_value == "crosstab":
        card_content = crosstab_method_inputs()
    elif dropdown_value == "specific_approval":
        card_content = specific_approval_method_inputs()
    elif dropdown_value == "share":
        card_content = share_method_inputs()
    elif dropdown_value == "report":
        card_content = report_method_inputs()
    elif dropdown_value == "decline":
        card_content = decline_method_inputs()
    elif dropdown_value == "approval":
        card_content = approval_method_inputs()
    elif dropdown_value == "bin_bank":
        card_content = bin_bank_method_inputs()

    new_card = html.Div(
        id=card_id,
        children=[
            *card_content,
            html.Button(
                "Run",
                id={"type": "run-button", "index": n_clicks},
                n_clicks=0,
                style={"margin-top": "10px"},
            ),
        ],
        className="card",
        draggable=True,
        style={"padding": "10px", "margin": "10px", "border": "1px solid gray"},
    )

    return [new_card]


@app.callback(
    Output({"type": "run-button", "index": all}, "n_clicks"),
    Input({"type": "run-button", "index": all}, "n_clicks"),
    State("dropdown", "value"),
    State({"type": "card-content", "index": all}, "children"),
)
def run_method(n_clicks, dropdown_value, card_content):
    if n_clicks == 0:
        raise PreventUpdate

    if dropdown_value == "search":
        transaction_id = card_content[2].value
        transaction_result = search_method(transaction_id)
        card_content.append(html.Pre(transaction_result))

    elif dropdown_value == "impact":
        filter_by = card_content[1].value
        sub_filter = card_content[3].value
        impact_method(filter_by, sub_filter)
    elif dropdown_value == "crosstab":
        col1 = card_content[1].value
        col2 = card_content[3].value
        crosstab_method(col1, col2)
    elif dropdown_value == "specific_approval":
        filter_by = card_content[1].value
        sub_filter = card_content[3].value
        specific_approval_method(filter_by, sub_filter)
    elif dropdown_value == "share":
        filter_by = card_content[1].value
        sub_filter = card_content[3].value
        share_method(filter_by, sub_filter)
    elif dropdown_value == "report":
        report_method()
    elif dropdown_value == "decline":
        columns = [option["value"] for option in card_content[1].options if option["value"] in card_content[1].value]
        decline_method(columns)
    elif dropdown_value == "approval":
        columns = [option["value"] for option in card_content[1].options if option["value"] in card_content[1].value]
        approval_method(columns)
    elif dropdown_value == "bin_bank":
        bin = card_content[1].value
        bin_bank_method(bin)

    return 0


if __name__ == "__main__":
    app.run_server(port=8055)
