import plotly.express as px
import pandas as pd

def plot_topic_frequency(memory_data):
    """Plots a bar chart of most studied topics."""
    if not memory_data or "topics" not in memory_data:
        return None
    
    data = memory_data["topics"]
    df = pd.DataFrame(list(data.items()), columns=["Topic", "Count"])
    fig = px.bar(df, x="Topic", y="Count", title="Most Studied Topics")
    return fig

def plot_weak_points(memory_data):
    """Plots a pie chart of weak points."""
    if not memory_data or "weak_points" not in memory_data:
        return None
        
    data = memory_data["weak_points"]
    df = pd.DataFrame(list(data.items()), columns=["Concept", "Difficulty_Score"])
    fig = px.pie(df, names="Concept", values="Difficulty_Score", title="Weak Points Distribution")
    return fig
