from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Project Description",className="fw-bold text-primary mb-3"),
                    html.P("The Siaya County Disease and Climate Monitoring Dashboard is an interactive geospatial surveillance platform that integrates malaria epidemiology, climate, and health system data to support infectious disease research and public health decision-making in western Kenya.",
                        className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}
                    ),
                    html.P("Beyond tracking malaria incidence, the dashboard visualizes the distribution and availability of key malaria control resources, including rapid diagnostic tests (RDTs), artemisinin-based combination therapies (ACTs), and insecticide-treated bed nets (ITNs), allowing users to evaluate disease burden alongside healthcare resource allocation and intervention coverage.",
                        className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}
                    ),
                    html.P("This integrated approach supports investigations into malaria and other febrile illnesses by identifying transmission hotspots, assessing preparedness, and exploring the environmental and operational factors influencing disease dynamics. The inclusion of commodity stock monitoring aligns with WHO recommendations for integrated malaria surveillance systems that combine epidemiologic, environmental, and supply chain data.",
                        className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}
                    ),
                    html.P("This project is in collaboration between researchers from Indiana University School of Medicine [IUSM] and Indiana University Indianapolis [IUI] (Indianapolis, Indiana, USA), Jaramogi Oginga Odinga University of Science and Technology [JOOUST] (Bondo, Kenya), and Siaya County Public Health Department. See the Project Contributors tab for more information. ",
                        className="text-muted", style={"fontSize": "20px", "lineHeight": "1.8"}
                    ),

                    html.H5("Key Features: ", className="mt-4"),
                    html.Ul([
                        html.Li("Malaria surveillance and disease burden monitoring"),
                        html.Li("Climate and environmental data integration"),
                        html.Li("Commodity stock monitoring (RDTs, ACTs, ITNs)"),
                        html.Li("Interactive visualizations and forecasting tools"),
                        html.Li("Decision-support for public health planning"),
                    ], className="text-muted", style={"fontSize": "18px", "lineHeight": "1.8"}),
                ]
            ),
            className="mt-4 shadow-sm",
        ),
    ],
    fluid=True,
    className="px-0",
)
