import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)

# Figure 1: Emergence - scatter with clustering
np.random.seed(0)
# generate two clusters
x1 = np.random.normal(loc=2, scale=0.5, size=100)
y1 = np.random.normal(loc=2, scale=0.5, size=100)

x2 = np.random.normal(loc=5, scale=0.5, size=100)
y2 = np.random.normal(loc=5, scale=0.5, size=100)

plt.figure(figsize=(4,4))
plt.scatter(x1, y1, color='steelblue', alpha=0.7, label='Cluster A')
plt.scatter(x2, y2, color='orange', alpha=0.7, label='Cluster B')
plt.title('Emergence of Clusters')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.tight_layout()
plt.savefig('figures/emergence.png')
plt.savefig('figures/emergence.svg')
plt.close()

# Figure 2: Gradient - heatmap of a simple gradient function
x = np.linspace(0, 1, 200)
y = np.linspace(0, 1, 200)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X-0.5)**2 - (Y-0.5)**2)  # Gaussian hill as gradient example

plt.figure(figsize=(4,4))
cp = plt.contourf(X, Y, Z, cmap='viridis')
plt.title('Spatial Gradient (Gaussian Hill)')
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar(cp, label='Intensity')
plt.tight_layout()
plt.savefig('figures/gradient.png')
plt.savefig('figures/gradient.svg')
plt.close()

# Figure 3: Constrained vs Unconstrained - line fitting example
# Generate synthetic data
np.random.seed(1)
X = np.linspace(0, 10, 30)
true_slope = 1.5
true_intercept = 2.0
Y = true_slope * X + true_intercept + np.random.normal(scale=2.0, size=X.shape)

# Unconstrained linear regression (ordinary least squares)
coeffs = np.polyfit(X, Y, 1)
Y_pred_uncon = np.polyval(coeffs, X)

# Constrained regression: slope forced to >= 0 (here we just clip for demonstration)
# We'll perform simple non-negative least squares using scipy if available; fallback to clipping.
# For simplicity, reuse OLS but enforce non-negative slope
slope_constrained = max(coeffs[0], 0)
intercept_constrained = coeffs[1]  # keep same intercept
Y_pred_con = slope_constrained * X + intercept_constrained

plt.figure(figsize=(5,3))
plt.scatter(X, Y, label='Data', color='gray')
plt.plot(X, Y_pred_uncon, label='Unconstrained Fit', color='blue')
plt.plot(X, Y_pred_con, label='Constrained Fit (slope≥0)', color='red', linestyle='--')
plt.title('Constrained vs Unconstrained Linear Fit')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.tight_layout()
plt.savefig('figures/constrained_unconstrained.png')
plt.savefig('figures/constrained_unconstrained.svg')
plt.close()
