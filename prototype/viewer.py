"""
Latent Anamorph — Interactive Viewer

Explore a latent anamorph by searching through projection space.
Supports random projection search, guided search toward privileged views,
and direct reveal of embedded images.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from construct import LatentAnamorph, random_orthonormal_basis


class AnamorphViewer:
    """Interactive matplotlib viewer for exploring a latent anamorph."""

    def __init__(self, anamorph: LatentAnamorph):
        self.anamorph = anamorph
        self.X = anamorph.points
        self.d = anamorph.ambient_dim
        self.rng = np.random.default_rng()

        # Start with a random projection
        self.current_basis = random_orthonormal_basis(self.d, 2, self.rng)
        self.hint_progress = 0.0  # 0 = random, 1 = privileged

        self._setup_figure()
        self._update_plot()

    def _setup_figure(self):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(8, 8))
        plt.subplots_adjust(bottom=0.25)

        self.scatter = self.ax.scatter([], [], s=1.5, c="steelblue", alpha=0.5)
        self.ax.set_aspect("equal")
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Latent Anamorph — search for the hidden form", fontsize=13)

        # Buttons
        ax_random = plt.axes([0.15, 0.12, 0.18, 0.05])
        ax_hint = plt.axes([0.41, 0.12, 0.18, 0.05])
        ax_reveal = plt.axes([0.67, 0.12, 0.18, 0.05])

        self.btn_random = Button(ax_random, "Random View")
        self.btn_hint = Button(ax_hint, "Hint (warmer)")
        self.btn_reveal = Button(ax_reveal, "Reveal")

        self.btn_random.on_clicked(self._on_random)
        self.btn_hint.on_clicked(self._on_hint)
        self.btn_reveal.on_clicked(self._on_reveal)

        # Slider for interpolation
        ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
        self.slider = Slider(ax_slider, "Warmth", 0.0, 1.0, valinit=0.0)
        self.slider.on_changed(self._on_slider)

        # Status text
        self.status_text = self.fig.text(
            0.5, 0.97, "", ha="center", va="top", fontsize=10, color="gray"
        )

    def _project(self, basis: np.ndarray) -> np.ndarray:
        """Project points onto a 2D basis."""
        return self.X @ basis  # (N, d) @ (d, 2) = (N, 2)

    def _interpolate_basis(self, t: float) -> np.ndarray:
        """
        Interpolate between a random basis and the privileged basis.
        Uses geodesic interpolation on the Grassmannian (via SVD).
        """
        target = self.anamorph.bases[self.anamorph.privileged_index]
        source = self._random_basis_cache

        # Simple interpolation: blend and re-orthogonalize
        blended = (1 - t) * source + t * target
        Q, _ = np.linalg.qr(blended)
        return Q[:, :2]

    def _update_plot(self):
        projected = self._project(self.current_basis)
        self.scatter.set_offsets(projected)

        # Auto-scale
        margin = 0.5
        xmin, xmax = projected[:, 0].min() - margin, projected[:, 0].max() + margin
        ymin, ymax = projected[:, 1].min() - margin, projected[:, 1].max() + margin
        span = max(xmax - xmin, ymax - ymin) / 2
        cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
        self.ax.set_xlim(cx - span, cx + span)
        self.ax.set_ylim(cy - span, cy + span)

        self.fig.canvas.draw_idle()

    def _on_random(self, event):
        self.current_basis = random_orthonormal_basis(self.d, 2, self.rng)
        self._random_basis_cache = self.current_basis.copy()
        self.hint_progress = 0.0
        self.slider.set_val(0.0)
        self.status_text.set_text("Random projection")
        self._update_plot()

    def _on_hint(self, event):
        """Move 20% closer to the privileged projection."""
        if not hasattr(self, "_random_basis_cache"):
            self._random_basis_cache = self.current_basis.copy()

        self.hint_progress = min(1.0, self.hint_progress + 0.2)
        self.current_basis = self._interpolate_basis(self.hint_progress)
        self.slider.set_val(self.hint_progress)

        if self.hint_progress >= 1.0:
            self.status_text.set_text("Privileged view reached!")
        else:
            self.status_text.set_text(f"Getting warmer... ({self.hint_progress:.0%})")
        self._update_plot()

    def _on_reveal(self, event):
        """Jump directly to the privileged projection."""
        self.current_basis = self.anamorph.bases[self.anamorph.privileged_index]
        self.hint_progress = 1.0
        self.slider.set_val(1.0)
        label = self.anamorph.labels[self.anamorph.privileged_index]
        self.status_text.set_text(f'Revealed: "{label}"')
        self._update_plot()

    def _on_slider(self, val):
        if not hasattr(self, "_random_basis_cache"):
            self._random_basis_cache = random_orthonormal_basis(self.d, 2, self.rng)

        self.hint_progress = val
        self.current_basis = self._interpolate_basis(val)

        if val >= 0.99:
            label = self.anamorph.labels[self.anamorph.privileged_index]
            self.status_text.set_text(f'Revealed: "{label}"')
        elif val > 0:
            self.status_text.set_text(f"Interpolating... ({val:.0%})")
        else:
            self.status_text.set_text("Random projection")
        self._update_plot()

    def show(self):
        self._random_basis_cache = self.current_basis.copy()
        plt.show()


def view_all_embedded(anamorph: LatentAnamorph):
    """Show a grid of all embedded images under their privileged projections."""
    n = len(anamorph.bases)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    if n == 1:
        axes = [axes]

    for i, (basis, label) in enumerate(zip(anamorph.bases, anamorph.labels)):
        projected = anamorph.points @ basis
        ax = axes[i]
        ax.scatter(projected[:, 0], projected[:, 1], s=1.5, alpha=0.4, c="steelblue")
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

        marker = " *" if i == anamorph.privileged_index else ""
        ax.set_title(f'"{label}"{marker}', fontsize=11)

    fig.suptitle("All embedded views (privileged projections)", fontsize=13)
    plt.tight_layout()
    plt.show()


def view_random_grid(anamorph: LatentAnamorph, n_random: int = 8):
    """Show a grid of random projections alongside the privileged one."""
    rng = np.random.default_rng()
    n_total = n_random + 1
    cols = 3
    rows = (n_total + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes = axes.flatten()

    # First panel: privileged view
    priv_basis = anamorph.bases[anamorph.privileged_index]
    proj = anamorph.points @ priv_basis
    axes[0].scatter(proj[:, 0], proj[:, 1], s=1.5, alpha=0.4, c="crimson")
    axes[0].set_title("PRIVILEGED VIEW", fontsize=10, fontweight="bold", color="crimson")
    axes[0].set_aspect("equal")
    axes[0].set_xticks([])
    axes[0].set_yticks([])

    # Remaining panels: random projections
    for i in range(1, n_total):
        basis = random_orthonormal_basis(anamorph.ambient_dim, 2, rng)
        proj = anamorph.points @ basis
        axes[i].scatter(proj[:, 0], proj[:, 1], s=1.5, alpha=0.4, c="steelblue")
        axes[i].set_title(f"Random #{i}", fontsize=10, color="gray")
        axes[i].set_aspect("equal")
        axes[i].set_xticks([])
        axes[i].set_yticks([])

    # Hide unused axes
    for i in range(n_total, len(axes)):
        axes[i].set_visible(False)

    fig.suptitle("Can you spot which view is designed?", fontsize=13)
    plt.tight_layout()
    plt.show()
