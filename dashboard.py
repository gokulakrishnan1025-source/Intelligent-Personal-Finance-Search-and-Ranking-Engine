"""Dashboard: charts and summary numbers for the app."""
import pandas as pd


def summary_metrics(df):
    """Return (total_transactions, total_spent, avg_amount)."""
    if df.empty:
        return 0, 0.0, 0.0
    return len(df), round(df["amount"].sum(), 2), round(df["amount"].mean(), 2)


def category_chart(df):
    """Amount spent per category (for a bar chart)."""
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)


def payment_chart(df):
    """Number of transactions per payment method (for a pie chart)."""
    if df.empty:
        return pd.Series(dtype=int)
    return df["payment_method"].value_counts()