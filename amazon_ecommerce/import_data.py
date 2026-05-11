import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, HTML
import base64
from io import BytesIO

df = pd.read_csv('./amazon_ecommerce/amazon_ecommerce_1M.csv')

# data exploration
df.head()
df.shape
df.columns
df.info()
# statistics summary
print(df.describe(include='all'))
# missing values
df.isnull().sum()
# distribution
df.hist(bins=50,figsize=(12,10),color='royalblue')
plt.show()


# outliers


# Kaggle like exploration
def mini_hist(serires, bins=50):
    """    Create a mini histogram for a given pandas Series."""
    s = serires.dropna()
    if s.empty:
        return ''
    
    fig, ax = plt.subplots(figsize=(1.6, 0.45))
    ax.hist(s, bins=bins, color='royalblue')
    ax.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    img = base64.b64encode(buffer.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img}"/>'

def kaggle_preview(df, n=10, save_html=True):
    preview = df.head(n).copy()
    header_rows = []
    for col in preview.columns:
        non_null = df[col].notna().sum()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            extra = mini_hist(df[col])
        else:
            extra = f"{df[col].nunique(dropna=True)} unique"
        header_rows.append(
            f"""
            <th>
                <div><b>{col}</b></div>
                <div style="font-size:11px; color:gray;">{non_null} non-null</div>
                <div style="font-size:11px;">{extra}</div>
            </th>
            """
        )
    body_rows = []
    for _, row in preview.iterrows():
        cells = "".join(f"<td>{row[col]}</td>" for col in preview.columns)
        body_rows.append(f"<tr>{cells}</tr>")
    html = f"""
    <div style="overflow-x:auto;">
    <table border="1" style="border-collapse:collapse; font-family:Arial; font-size:12px;">
        <thead>
            <tr>
                {''.join(header_rows)}
            </tr>
        </thead>
        <tbody>
            {''.join(body_rows)}
        </tbody>
    </table>
    </div>
    """
    if save_html:
        with open("./amazon_ecommerce/preview.html", "w") as f:
            f.write(html)
        print("Saved to preview.html")
    else:
        display(HTML(html))

kaggle_preview(df)