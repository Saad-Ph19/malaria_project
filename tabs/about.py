from dash import html
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Project Contributors",className="fw-bold text-primary mb-3"),
                    html.P("This work is conducted through a collaborative partnership involving: ",className="text-muted",style={"fontSize": "25px", "lineHeight": "1.8"}),
                    html.Ul([
                        html.Li([
                            html.Strong("Principal Investigators: "),
                            "Felix Pabon-Rodriguez (IUSM) and George Ayodo (JOOUST)"]),
                        html.Li([
                            html.Strong("Co-Investigator: "),
                            "Yan Zhuang (IUI)"]),
                        html.Li([
                            html.Strong("Indiana University Research Assistants: "),
                            "Saad Pharis, Mridul Banik, Nathaniel Maxey, and Taliyah Griffin"]),
                        html.Li([
                            html.Strong("Siaya County Public Health Officer: "),
                            "Moses Ombuoro"]),
                        html.Li([
                            html.Strong("App Developer: "),
                            "Saad Pharis"]),
                    ], className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}),
                    
                    html.P("The project integrates data from:",className="text-muted",style={"fontSize": "25px", "lineHeight": "1.8"}),
                    html.Ul([
                        html.Li("Kenya Health Information System (KHIS)"),
                        html.Li("Google Earth spatial datasets"),
                        html.Li("Climate and environmental information supporting geospatial disease surveillance"),
                    ], className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}),
                    html.P("In case of questions and/or requests, please contact PI Felix Pabon-Rodriguez via email at fpabonr@iu.edu.",className="text-muted",style={"fontSize": "25px", "lineHeight": "1.8"}),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
