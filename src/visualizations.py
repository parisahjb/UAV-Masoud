"""
Visualization Module
Creates static and interactive visualizations for UAV trajectories
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def create_visualizations(uav_system, num_intervals=500, color_scheme='hot'):
    """Create matplotlib visualizations"""
    
    # Generate trajectory
    trajectory, alphas = uav_system.generate_trajectory(num_intervals)
    
    # Process trajectory data
    r_values = [pt[0] for pt in trajectory]
    theta_values = [pt[1] for pt in trajectory]
    x_values = [r * np.cos(theta) for r, theta in zip(r_values, theta_values)]
    y_values = [r * np.sin(theta) for r, theta in zip(r_values, theta_values)]
    
    # Filter points within unit circle
    filtered_points = [(x, y, r, theta) for x, y, r, theta in 
                      zip(x_values, y_values, r_values, theta_values) 
                      if np.sqrt(x**2 + y**2) <= 1.0]
    if filtered_points:
        x_values, y_values, r_values, theta_values = zip(*filtered_points)
        x_values, y_values = list(x_values), list(y_values)
    
    # Create figure with subplots
    fig, axs = plt.subplots(3, 2, figsize=(14, 18))
    
    # 1. Position Density Heatmap
    heatmap, xedges, yedges = np.histogram2d(x_values, y_values, 
                                             bins=100, range=[[-1.0, 1.0], [-1.0, 1.0]])
    x_centers = (xedges[:-1] + xedges[1:]) / 2
    y_centers = (yedges[:-1] + yedges[1:]) / 2
    X, Y = np.meshgrid(x_centers, y_centers)
    mask = X**2 + Y**2 > 1.0
    heatmap_masked = np.ma.masked_where(mask.T, heatmap.T)
    
    extent = [-1.0, 1.0, -1.0, 1.0]
    im = axs[0, 0].imshow(heatmap_masked, extent=extent, origin='lower', 
                         cmap=color_scheme, norm=LogNorm(vmin=1, vmax=heatmap.max()), 
                         interpolation='bilinear')
    axs[0, 0].add_artist(plt.Circle((0, 0), 1.0, fill=False, color='white', linewidth=2))
    axs[0, 0].add_artist(plt.Circle((0, 0), uav_system.delta, fill=False, color='cyan', 
                                   linewidth=1, linestyle='--'))
    axs[0, 0].set_xlim(-1.1, 1.1)
    axs[0, 0].set_ylim(-1.1, 1.1)
    axs[0, 0].set_title('UAV Position Density', fontsize=14, fontweight='bold')
    axs[0, 0].set_xlabel('x')
    axs[0, 0].set_ylabel('y')
    axs[0, 0].set_aspect('equal')
    axs[0, 0].grid(True, alpha=0.2, linestyle=':', color='gray')
    fig.colorbar(im, ax=axs[0, 0], label='Count (log scale)')
    
    # 2. h_alpha function
    alpha_sample = uav_system.sample_alpha(1)[0]
    s_values = np.linspace(0, 1, 200)
    h_values = [uav_system.h_alpha(s, alpha_sample) for s in s_values]
    axs[0, 1].plot(s_values, h_values, 'b-', linewidth=2.5)
    axs[0, 1].fill_between(s_values, h_values, alpha=0.3)
    axs[0, 1].set_xlabel('s', fontsize=12)
    axs[0, 1].set_ylabel('h_alpha(s)', fontsize=12)
    axs[0, 1].set_title(f'h_alpha(s) for alpha = {alpha_sample:.3f}', fontsize=14, fontweight='bold')
    axs[0, 1].grid(True, alpha=0.3)
    
    # 3. h_alpha_inverse function
    t_values = np.linspace(0, uav_system.tau, 200)
    h_inv_values = [uav_system.h_alpha_inverse(t, alpha_sample) for t in t_values]
    axs[1, 0].plot(t_values, h_inv_values, 'g-', linewidth=2.5)
    axs[1, 0].fill_between(t_values, h_inv_values, alpha=0.3)
    axs[1, 0].set_xlabel('t', fontsize=12)
    axs[1, 0].set_ylabel('h_alpha_inv(t)', fontsize=12)
    axs[1, 0].set_title(f'h_alpha_inv(t) for alpha = {alpha_sample:.3f}', fontsize=14, fontweight='bold')
    axs[1, 0].grid(True, alpha=0.3)
    
    # 4. Alpha distribution
    axs[1, 1].hist(alphas, bins=50, density=True, alpha=0.7, color='purple', edgecolor='black')
    f_A_normalized = uav_system.f_A_values / np.trapz(uav_system.f_A_values, uav_system.alpha_range)
    axs[1, 1].plot(uav_system.alpha_range, f_A_normalized, 'r-', linewidth=2.5, label='True f_A(alpha)')
    axs[1, 1].set_title('Distribution of Sampled alpha', fontsize=14, fontweight='bold')
    axs[1, 1].set_xlabel('alpha', fontsize=12)
    axs[1, 1].set_ylabel('Density', fontsize=12)
    axs[1, 1].legend(fontsize=11)
    axs[1, 1].grid(True, alpha=0.3)
    
    # 5. Single trajectory
    single_traj = trajectory[:1000]
    x_single = [r * np.cos(theta) for r, theta in single_traj if r <= 1.0]
    y_single = [r * np.sin(theta) for r, theta in single_traj if r <= 1.0]
    valid_indices = [i for i, (r, theta) in enumerate(single_traj) if r <= 1.0]
    
    sc = axs[2, 0].scatter(x_single, y_single, c=valid_indices, cmap='viridis', s=2, alpha=0.8)
    axs[2, 0].add_artist(plt.Circle((0, 0), 1.0, fill=False, color='red', linewidth=2))
    axs[2, 0].add_artist(plt.Circle((0, 0), uav_system.delta, fill=False, color='orange', 
                                   linewidth=1, linestyle='--'))
    axs[2, 0].set_xlim(-1.1, 1.1)
    axs[2, 0].set_ylim(-1.1, 1.1)
    axs[2, 0].set_title('Single UAV Trajectory', fontsize=14, fontweight='bold')
    axs[2, 0].set_xlabel('x', fontsize=12)
    axs[2, 0].set_ylabel('y', fontsize=12)
    axs[2, 0].set_aspect('equal')
    axs[2, 0].grid(True, alpha=0.2, linestyle=':', color='gray')
    fig.colorbar(sc, ax=axs[2, 0], label='Time Step')
    
    # 6. Radial distribution
    r_all = [r for r in r_values if r <= 1.0]
    axs[2, 1].hist(r_all, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    axs[2, 1].set_title('Radial Distribution', fontsize=14, fontweight='bold')
    axs[2, 1].set_xlabel('r', fontsize=12)
    axs[2, 1].set_ylabel('Density', fontsize=12)
    axs[2, 1].axvline(x=uav_system.delta, color='r', linestyle='--', linewidth=2, 
                      label=f'delta = {uav_system.delta}')
    axs[2, 1].axvline(x=1.0,  color='g', linestyle='--', linewidth=2, label='rho = 1.0')
    axs[2, 1].set_xlim(0, 1.1)
    axs[2, 1].legend(fontsize=11)
    axs[2, 1].grid(True, alpha=0.3)
    
    plt.suptitle(f'{uav_system.distribution_name}', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    return fig, trajectory, alphas

def create_plotly_visualizations(uav_system, num_intervals=500, color_scheme='hot'):
    """Create interactive Plotly visualizations"""
    
    # Generate trajectory
    trajectory, alphas = uav_system.generate_trajectory(num_intervals)
    
    # Process trajectory data
    r_values = [pt[0] for pt in trajectory]
    theta_values = [pt[1] for pt in trajectory]
    x_values = [r * np.cos(theta) for r, theta in zip(r_values, theta_values)]
    y_values = [r * np.sin(theta) for r, theta in zip(r_values, theta_values)]
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('UAV Position Density', 'h_alpha(s) Function',
                       'h_alpha_inverse(t) Function', 'Alpha Distribution',
                       'Single UAV Trajectory', 'Radial Distribution'),
        specs=[[{'type': 'heatmap'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'bar'}]]
    )
    
    # 1. Position Density Heatmap
    heatmap, xedges, yedges = np.histogram2d(x_values, y_values, 
                                             bins=100, range=[[-1.0, 1.0], [-1.0, 1.0]])
    
    fig.add_trace(
        go.Heatmap(z=heatmap.T, x=xedges, y=yedges, 
                  colorscale=color_scheme, showscale=True),
        row=1, col=1
    )
    
    # Add circles
    theta_circle = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(
        go.Scatter(x=np.cos(theta_circle), y=np.sin(theta_circle),
                  mode='lines', line=dict(color='white', width=2),
                  showlegend=False),
        row=1, col=1
    )
    
    # 2. h_alpha function
    alpha_sample = uav_system.sample_alpha(1)[0]
    s_values = np.linspace(0, 1, 200)
    h_values = [uav_system.h_alpha(s, alpha_sample) for s in s_values]
    
    fig.add_trace(
        go.Scatter(x=s_values, y=h_values, mode='lines',
                  fill='tozeroy', line=dict(color='blue', width=2)),
        row=1, col=2
    )
    
    # 3. h_alpha_inverse function
    t_values = np.linspace(0, uav_system.tau, 200)
    h_inv_values = [uav_system.h_alpha_inverse(t, alpha_sample) for t in t_values]
    
    fig.add_trace(
        go.Scatter(x=t_values, y=h_inv_values, mode='lines',
                  fill='tozeroy', line=dict(color='green', width=2)),
        row=2, col=1
    )
    
    # 4. Alpha distribution
    fig.add_trace(
        go.Histogram(x=alphas, nbinsx=50, histnorm='probability density',
                    marker=dict(color='purple', line=dict(color='black', width=1))),
        row=2, col=2
    )
    
    # 5. Single trajectory
    single_traj = trajectory[:1000]
    x_single = [r * np.cos(theta) for r, theta in single_traj if r <= 1.0]
    y_single = [r * np.sin(theta) for r, theta in single_traj if r <= 1.0]
    
    fig.add_trace(
        go.Scatter(x=x_single, y=y_single, mode='markers',
                  marker=dict(size=2, color=list(range(len(x_single))),
                            colorscale='viridis', showscale=True)),
        row=3, col=1
    )
    
    # 6. Radial distribution
    r_all = [r for r in r_values if r <= 1.0]
    
    fig.add_trace(
        go.Histogram(x=r_all, nbinsx=50, histnorm='probability density',
                    marker=dict(color='blue', line=dict(color='black', width=1))),
        row=3, col=2
    )
    
    # Update layout
    fig.update_layout(height=1200, showlegend=False,
                     title_text=f"{uav_system.distribution_name}",
                     title_font_size=20)
    
    # Update axes
    fig.update_xaxes(title_text="x", row=1, col=1)
    fig.update_yaxes(title_text="y", row=1, col=1)
    fig.update_xaxes(title_text="s", row=1, col=2)
    fig.update_yaxes(title_text="h_alpha(s)", row=1, col=2)
    fig.update_xaxes(title_text="t", row=2, col=1)
    fig.update_yaxes(title_text="h_alpha_inv(t)", row=2, col=1)
    fig.update_xaxes(title_text="alpha", row=2, col=2)
    fig.update_yaxes(title_text="Density", row=2, col=2)
    fig.update_xaxes(title_text="x", row=3, col=1)
    fig.update_yaxes(title_text="y", row=3, col=1)
    fig.update_xaxes(title_text="r", row=3, col=2)
    fig.update_yaxes(title_text="Density", row=3, col=2)
    
    return fig, trajectory, alphas
