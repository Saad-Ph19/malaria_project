from dash import html
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Project Description"),
                    html.P(
                        "The Siaya County Disease and Climate Monitoring Dashboard is an interactive geospatial surveillance platform that integrates malaria epidemiology, climate, and health system data to support infectious disease research and public health decision-making in western Kenya.

Beyond tracking malaria incidence, the dashboard visualizes the distribution and availability of key malaria control resources, including rapid diagnostic tests (RDTs), artemisinin-based combination therapies (ACTs), and insecticide-treated bed nets (ITNs), allowing users to evaluate disease burden alongside healthcare resource allocation and intervention coverage.

This integrated approach supports investigations into malaria and other febrile illnesses by identifying transmission hotspots, assessing preparedness, and exploring the environmental and operational factors influencing disease dynamics. The inclusion of commodity stock monitoring aligns with WHO recommendations for integrated malaria surveillance systems that combine epidemiologic, environmental, and supply chain data.

This project is in collaboration between researchers from Indiana University School of Medicine [IUSM] and Indiana University Indianapolis [IUI] (Indianapolis, Indiana, USA), Jaramogi Oginga Odinga University of Science and Technology [JOOUST] (Bondo, Kenya), and Siaya County Public Health Department. See the Project Contributors tab for more information. ",
                        className="text-muted",
                    ),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
