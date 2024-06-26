import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import logging
from src.analysis.phase_1.models import create_score_summaries, get_model_scores
from src.analysis.utils import dir_path, phase_1_vars, phase_1_log

output_path = os.path.join(dir_path, '../../output/figures/phase_1')

def plots_station_no_station(df: pd.DataFrame) -> None:
    """
    Create boxplot, swarmplot, and violin plot to compare m² prices by presence of train stations
    Also saves the plots to the output folder.

    Parameters:
        df: DataFrame with the main dataset
    
    Returns:
        None
    """
    df['has_station'] = df['has_station'].astype(int)

    # Create boxplot to visualize the difference in m² prices
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=df, x='has_station', y='m2_price', hue='has_station', palette='Set2')
    plt.xlabel('Has Train Station')
    plt.ylabel('Average m² Price')
    plt.title('Comparison of m² Prices by Presence of Train Stations')
    plt.grid(True)

    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, title='Has Train Station', loc='upper right', labels=['No', 'Yes'])

    plt.savefig(os.path.join(output_path, 'boxplot.png'))

def scatter_plots(df: pd.DataFrame) -> None:
    """
    Create scatter plots of variables along with distributions against m2_price and log variables against log_m2_price.

    Parameters:
        df: DataFrame with the main dataset
        output_path: Path to save the resulting plots

    Returns:
        None
    """
    variables = ['avg_income', 'homes_per_capita', 'multy_family', 'distance_to_urban_center']
    log_variables = ['log_avg_income', 'homes_per_capita', 'log_multy_family', 'log_distance']

    # First figure for original variables
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 22))

    palette = sns.color_palette('Set2')

    for i, var in enumerate(variables):
        # Scatter plot
        sns.scatterplot(x=df[var], y=df['m2_price'], ax=axes[i, 0], color=palette[1], edgecolor='k', alpha=0.7)
        axes[i, 0].set_xlabel(var)
        axes[i, 0].set_ylabel('m2_price')
        axes[i, 0].set_title(f'{var} vs m2_price')
        
        # Distribution plot
        sns.histplot(df[var], kde=True, ax=axes[i, 1], color=palette[0])
        axes[i, 1].set_xlabel(var)
        axes[i, 1].set_ylabel('Frequency')
        axes[i, 1].set_title(f'Distribution of {var}')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_path, 'scatter_plots_original.png'))

    # Second figure for log-transformed variables
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 22))

    for i, log_var in enumerate(log_variables):
        # Scatter plot
        sns.scatterplot(x=df[log_var], y=df['log_m2_price'], ax=axes[i, 0], color=palette[1], edgecolor='k', alpha=0.7)
        axes[i, 0].set_xlabel(log_var)
        axes[i, 0].set_ylabel('log_m2_price')
        axes[i, 0].set_title(f'{log_var} vs log_m2_price')
        
        # Distribution plot
        sns.histplot(df[log_var], kde=True, ax=axes[i, 1], color=palette[0])
        axes[i, 1].set_xlabel(log_var)
        axes[i, 1].set_ylabel('Frequency')
        axes[i, 1].set_title(f'Distribution of {log_var}')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_path, 'scatter_plots_log.png'))

def plot_distribution(df: pd.DataFrame) -> None:
    """
    Create a distribution plot of the m2_price variable against the log_m2_price variable.

    Parameters:
        df: DataFrame with the main dataset
    
    Returns:
        None
    """
    _, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    palette = sns.color_palette('Set2')

    sns.histplot(df['m2_price'], kde=True, ax=axes[0], bins=30, color=palette[0])
    axes[0].set_title('Distribution of m2_price')
    axes[0].set_xlabel('m2_price')
    axes[0].set_ylabel('Frequency')

    sns.histplot(df['log_m2_price'], kde=True, ax=axes[1], bins=30, color=palette[0])
    axes[1].set_title('Distribution of log_m2_price')
    axes[1].set_xlabel('log_m2_price')
    axes[1].set_ylabel('Frequency')

    plt.savefig(os.path.join(output_path, 'm2_price_distribution.png'))

def correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Create a heatmap of the correlation matrix of the variables.

    Parameters:
        df: DataFrame with the main dataset
    
    Returns:
        None
    """
    variables = ['has_station','avg_income', 'homes_per_capita', 'multy_family', 'unemp_rate', 'pop_density', 'net_labor_participation', 'distance_to_urban_center']

    plt.figure(figsize=(14, 12))
    sns.heatmap(df[variables].corr(), annot=True, fmt='.2f', 
                cmap='BrBG', linewidths=.5, vmin=-1, vmax=1)
    plt.xticks(rotation=45)
    # plt.title('Correlation Matrix of Variables')

    plt.savefig(os.path.join(output_path, 'corr_heatmap.png'))

def updated_log_corr_heatmap(df: pd.DataFrame) -> None:
    """
    Create a heatmap of the correlation matrix of the log-transformed variables.

    Parameters:
        df: DataFrame with the main dataset
    
    Returns:
        None
    """
    variables = phase_1_log

    plt.figure(figsize=(14, 12))
    sns.heatmap(df[variables].corr(), annot=True, fmt='.2f', 
                cmap='BrBG', linewidths=.5, vmin=-1, vmax=1)
    plt.xticks(rotation=45)
    # plt.title('Correlation Matrix of Log-Transformed Variables')

    plt.savefig(os.path.join(output_path, 'log_corr_heatmap.png'))

def visualize_model_scores(results: dict, title: str) -> None:
    """
    Visualize the VIFs, condition indices, and BIC scores for the models.

    Parameters:
        results: Dictionary with the results of the models.
        title: Title for the plots
    
    Returns:
        None
    """
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15), dpi=120)

    logging.info(f"Visualizing scores for {title}...")

    # VIFs
    vif_data_list = []
    for name, data in results.items():
        if 'vif' in data and not pd.DataFrame(data['vif']).empty:
            vif_data = pd.DataFrame(data['vif'])
            vif_data['log_VIF'] = np.log10(vif_data['VIF'])
            vif_data['Model'] = name
            vif_data_list.append(vif_data)

    if vif_data_list:
        full_vif_data = pd.concat(vif_data_list)
        sns.barplot(x='log_VIF', y='feature', hue='Model', data=full_vif_data, ax=axes[0])
        axes[0].set_title(f'Log-Scaled VIFs for {title}')
        axes[0].set_xlabel("Log10 (VIF)")
        axes[0].set_ylabel(" ")

        axes[0].axvline(x=0.699, color='#404040', linewidth=2, linestyle='--', label='VIF = 5')
        axes[0].legend()

    # Condition Indices
    cond_indices_list = [{
        "Model": name,
        "Condition Index": np.log10(data['cond_indices']).max()
    } for name, data in results.items() if 'cond_indices' in data]

    if cond_indices_list:
        cond_indices_data = pd.DataFrame(cond_indices_list)
        sns.barplot(x='Condition Index', y='Model', data=cond_indices_data, ax=axes[1], width=0.6, hue='Model')
        axes[1].set_title(f'Log-Scaled Largest Condition Indices for {title}')
        axes[1].set_xlabel("Log10 (Condition Index)")
        axes[1].set_ylabel(" ")
        axes[1].axvline(x=1.477, color='gray', linewidth=2, linestyle='--', label='Condition Index = 30')
        axes[1].legend()

    # BIC Scores
    bic_list = [{
        "Model": name,
        "BIC": data['bic']
    } for name, data in results.items() if 'bic' in data]

    if bic_list:
        bic_data = pd.DataFrame(bic_list)
        sns.barplot(x='BIC', y='Model', data=bic_data, ax=axes[2], width=0.6, hue='Model')
        axes[2].set_title(f'BIC Scores for {title}')
        axes[2].set_xlabel("BIC Score")
        axes[2].set_ylabel(" ")
        axes[2].set_xlim(bic_data['BIC'].min() - 5, bic_data['BIC'].max() + 5)
    
    plt.tight_layout()
    
    filename = title.lower().replace('-', '_').replace(' ', '_')

    plt.savefig(os.path.join(output_path, f'model_scores/{filename}_scores.png'))

def create_plots(df: pd.DataFrame) -> None:
    """
    Create plots for the Phase 1 analysis.

    Parameters:
        df: DataFrame with the main dataset
    
    Returns:
        None
    """
    logging.info("Creating and saving figures for Phase 1...")
    plots_station_no_station(df)
    scatter_plots(df)
    correlation_heatmap(df)
    updated_log_corr_heatmap(df)
    plot_distribution(df)

    non_log_scores, log_scores, dropped_outliers_scores, centered_log_scores = get_model_scores(df)
    visualize_model_scores(non_log_scores, 'Non-Log Models')
    visualize_model_scores(log_scores, 'Log Models')
    visualize_model_scores(dropped_outliers_scores, 'Log Models with Dropped Outliers')
    visualize_model_scores(centered_log_scores, 'Centered Log Models')

    plt.close('all')

    logging.info("Figures saved.")
