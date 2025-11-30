# utils/charts.py
"""Plot charts for StudyBot dashboard."""

import plotly.express as px
import plotly.graph_objects as go

def plot_topic_frequency(topics_list):
    if not topics_list:
        return None
    fig = px.bar(
        x=list(topics_list),
        y=[topics_list.count(t) for t in topics_list],
        labels={"x": "Topic", "y": "Frequency"},
        title="Most Studied Topics"
    )
    return fig

def plot_weakpoint_frequency(weak_list):
    if not weak_list:
        return None
    fig = px.bar(
        x=weak_list,
        y=[weak_list.count(w) for w in weak_list],
        labels={"x": "Weak Point", "y": "Frequency"},
        title="Weak Points Over Time"
    )
    return fig

def plot_usage_count(count):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number",
        value=count,
        title="Total Sessions"
    ))
    return fig
