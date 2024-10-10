import pandas as pd
import plotly.express as px

df = pd.read_csv("Data/Historical NBA Performance.csv")
df = df.pivot("Team", "Year", "Winning Percentage")
print(df[:10])

df = df[df.index.isin(["Warriors", "Knicks", "Celtics", "Bulls", "76ers"])]
fig = px.imshow(
    df,
    color_continuous_scale=px.colors.sequential.YlOrBr,
    title="NBA Season Winning Percentage",
)
fig.update_layout(title_font={"size": 27}, title_x=0.5)
fig.update_traces(
    hoverongaps=False,
    hovertemplate="Team: %{y}" "<br>Year: %{x}" "<br>Winning %: %{z}<extra></extra>",
)
fig.show()
