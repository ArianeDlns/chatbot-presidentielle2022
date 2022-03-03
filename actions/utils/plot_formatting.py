import pandas as pd
import matplotlib.pyplot as plt

def plot_poll(candidates_names, df_sondages):
    df_sondages = df_sondages.sort_values('date')
    fig, ax = plt.subplots(figsize=(9, 6))
    
    for candidate in candidates_names:
        #ax.plot(df_sondages.Date, df_sondages[candidate], color="#0b53c1", lw=2.4, zorder=10)
        ax.scatter(df_sondages.Date, df_sondages[candidate], fc="w", ec="#0b53c1", s=60, lw=2.4, zorder=12)  
        ax.plot(df_sondages.Date.unique(), df_sondages.groupby('date').agg({candidate:'mean'}), color="#BFBFBF", lw=1.5)
    title = f"Evolution de {' et '.join(candidates_names)} dans les sondages \n"
    ax.set_title(title, fontfamily="Inconsolata", fontsize=24, fontweight=500)
    plt.savefig('stat.png')
    return 0

def HTML_table_from_df(df):
    return '<pre> '+df.to_markdown(index=False)+' </pre>'