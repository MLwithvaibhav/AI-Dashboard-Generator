import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

def get_analysis(query):
    prompt = f"""
    You are a data analyst.

    Convert this query into JSON:
    {query}

    Include:
    - columns
    - aggregation
    - group_by
    - chart_type
    - filters

    Return JSON only.
    """

    response = model.generate_content(prompt)
    return response.text



import plotly.express as px

def generate_chart(df, config):
    chart = config["chart_type"]

    if chart == "line":
        fig = px.line(df, x=config["group_by"], y=config["columns"][1])
    elif chart == "bar":
        fig = px.bar(df, x=config["group_by"], y=config["columns"][1])

    return fig