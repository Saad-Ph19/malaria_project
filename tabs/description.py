from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        "Project Description",
                        className="fw-bold text-primary mb-3"
                    ),
                    html.P(
                        "The Siaya County Disease and Climate Monitoring Dashboard is an interactive geospatial surveillance platform that integrates malaria epidemiology, climate, and health system data to support infectious disease research and public health decision-making in western Kenya.",
                        className="text-muted"
                    ),
                    html.P(
                        "Beyond tracking malaria incidence, the dashboard visualizes the distribution and availability of key malaria control resources, including Rapid Diagnostic Tests (RDTs), Artemisinin-based Combination Therapies (ACTs), and Insecticide-Treated Bed Nets (ITNs). These indicators allow users to evaluate disease burden alongside healthcare resource allocation and intervention coverage.",
                        className="text-muted"
                    ),
                    html.P(
                        "The platform supports investigations into malaria and other febrile illnesses by identifying transmission hotspots, assessing preparedness, and exploring environmental and operational factors that influence disease dynamics.",
                        className="text-muted"
                    ),
                    html.P(
                        "This project is a collaboration between Indiana University School of Medicine (IUSM), Indiana University Indianapolis (IUI), Jaramogi Oginga Odinga University of Science and Technology (JOOUST), and the Siaya County Public Health Department.",
                        className="text-muted"
                    ),

                    html.H5("Key Features", className="mt-4"),

                    html.Ul([
                        html.Li("Malaria surveillance and disease burden monitoring"),
                        html.Li("Climate and environmental data integration"),
                        html.Li("Commodity stock monitoring (RDTs, ACTs, ITNs)"),
                        html.Li("Interactive visualizations and forecasting tools"),
                        html.Li("Decision-support for public health planning"),
                    ], className="text-muted"),
                ]
            ),
            className="shadow-sm border-0 mt-4",
        ),
    ],
    fluid=True,
)
