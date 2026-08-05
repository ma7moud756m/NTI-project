import plotly.graph_objects as go
import streamlit as st


PAGE_BG = "#FFFFFF"


def get_risk_level(probability, disease="the condition"):

    risk_percentage = probability * 100

    if risk_percentage < 20:

        return (
            "Low Risk 🟢",
            f"Your predicted risk for {disease} is relatively low. "
            f"Continue maintaining a healthy lifestyle and regular medical checkups."
        )

    elif risk_percentage < 30:

        return (
            "Moderate Risk 🟡",
            f"Some risk factors for {disease} were detected. Improving lifestyle "
            f"habits and monitoring health indicators are recommended."
        )

    else:

        return (
            "High Risk 🔴",
            f"Several risk factors for {disease} were detected. Consider "
            f"consulting a healthcare professional for further evaluation."
        )


def create_risk_gauge(probability, disease="Condition"):
    """
    Renders a professional Plotly gauge for the given risk probability,
    styled to match the app's medical theme (background, deep risk
    colors) instead of the flat progress-bar look.
    """

    percentage = probability * 100

    if percentage < 10:
        bar_color = "#15803D"   # deep green
    elif percentage < 30:
        bar_color = "#B45309"   # deep amber
    else:
        bar_color = "#B91C1C"   # deep red

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        number={"suffix": "%", "font": {"size": 42, "color": "#102A43"}},
        title={
            "text": f"Estimated {disease} Risk",
            "font": {"size": 18, "color": "#102A43"}
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickcolor": "#087E8B",
                "tickfont": {"color": "#4A4A4A", "size": 12}
            },
            "bar": {"color": bar_color, "thickness": 0.32},
            "bgcolor": PAGE_BG,
            "borderwidth": 0,
            "steps": [
                {"range": [0, 10], "color": "#E7F9EE"},
                {"range": [10, 30], "color": "#FFF3D6"},
                {"range": [30, 100], "color": "#FDECEA"},
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor=PAGE_BG,
        plot_bgcolor=PAGE_BG,
        height=320,
        margin=dict(l=30, r=30, t=60, b=10),
        font=dict(family="sans-serif")
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
