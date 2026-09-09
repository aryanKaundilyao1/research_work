import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def set_style():
    plt.rcParams.update({
        'font.size': 14,
        'axes.labelsize': 16,
        'axes.titlesize': 18,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'legend.fontsize': 14,
        'figure.figsize': (8, 6),
        'axes.spines.top': False,
        'axes.spines.right': False
    })

def create_fig3(out_dir):
    # Figure 3: Macro AUROC Absolute vs Relative
    # Values from canonical registry
    labels = ['Absolute\nRepresentation', 'Baseline-Relative\nRepresentation']
    means = [0.4922, 0.7810]
    err_lower = [0.4922 - 0.3357, 0.7810 - 0.6526]
    err_upper = [0.5056 - 0.4922, 0.8894 - 0.7810]
    
    yerr = [err_lower, err_upper]
    
    fig, ax = plt.subplots(figsize=(7, 6))
    bars = ax.bar(labels, means, yerr=yerr, capsize=10, color=['#e74c3c', '#2ecc71'], alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.axhline(0.5, color='gray', linestyle='--', alpha=0.7, label='Random Chance')
    ax.set_ylabel('Macro Subject AUROC')
    ax.set_ylim(0, 1.0)
    ax.set_title('Cross-Dataset Generalization Performance')
    
    # Add text labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{yval:.3f}', ha='center', va='bottom', fontweight='bold')
        
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'Figure_3_Macro_AUROC_Comparison.pdf'), format='pdf', dpi=300)
    plt.savefig(os.path.join(out_dir, 'Figure_3_Macro_AUROC_Comparison.png'), format='png', dpi=300)
    plt.close()

def create_fig10(out_dir):
    # Figure 10: SHAP Rank Agreement
    metrics = ['Spearman $\\rho$', 'Kendall $\\tau$', 'Top-10 Jaccard', 'Top-5 Jaccard']
    values = [0.9847, 0.9333, 1.0000, 0.6667]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(metrics, values, color='#3498db', alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Agreement Score')
    ax.set_xlim(0, 1.1)
    ax.set_title('Cross-Dataset SHAP Feature Attribution Stability')
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.02, bar.get_y() + bar.get_height()/2, f'{width:.3f}', ha='left', va='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'Figure_10_SHAP_Rank_Comparison.pdf'), format='pdf', dpi=300)
    plt.savefig(os.path.join(out_dir, 'Figure_10_SHAP_Rank_Comparison.png'), format='png', dpi=300)
    plt.close()

def create_fig11(out_dir):
    # Figure 11: Protocol V1 vs V2
    labels = ['V1: Stroop First\n(N=18)', 'V2: Subtract First\n(N=17, Eligible=3)']
    means = [0.7634, 0.8864]
    
    # bounds from log: V1 CI: 0.6153, 0.8837. V2 CI: 0.6761, 1.0000
    err_lower = [0.7634 - 0.6153, 0.8864 - 0.6761]
    err_upper = [0.8837 - 0.7634, 1.0000 - 0.8864]
    
    yerr = [err_lower, err_upper]
    
    fig, ax = plt.subplots(figsize=(7, 6))
    bars = ax.bar(labels, means, yerr=yerr, capsize=10, color=['#9b59b6', '#f1c40f'], alpha=0.8, edgecolor='black')
    
    ax.axhline(0.5, color='gray', linestyle='--', alpha=0.7)
    ax.set_ylabel('Macro Subject AUROC')
    ax.set_ylim(0, 1.05)
    ax.set_title('Performance by Target Protocol Sequence')
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{yval:.3f}', ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'Figure_11_Protocol_V1_vs_V2.pdf'), format='pdf', dpi=300)
    plt.savefig(os.path.join(out_dir, 'Figure_11_Protocol_V1_vs_V2.png'), format='png', dpi=300)
    plt.close()

def main():
    set_style()
    out_dir = 'figures/final_submission'
    os.makedirs(out_dir, exist_ok=True)
    
    create_fig3(out_dir)
    create_fig10(out_dir)
    create_fig11(out_dir)
    
    print("All canonical vector figures generated successfully.")

if __name__ == '__main__':
    main()
