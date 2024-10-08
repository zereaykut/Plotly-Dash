import pandas as pd
import plotly.express as px

df = pd.read_csv("Data/customer_churn.csv")
df = df.groupby(["onboard_month", "weeks_subscribed"]).size().unstack(fill_value=0)

df = df.reindex(
    [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
)
print(df)

fig = px.imshow(
    df, color_continuous_scale=px.colors.sequential.Plasma, title="Subscription Churn"
)
fig.update_layout(title_font={"size": 27}, title_x=0.5)
fig.update_traces(
    hovertemplate="Membership bought: %{y}"
    "<br>Weeks subscribed: %{x}"
    "<br>Cancellations: %{z}<extra></extra>"
)
fig.show()

