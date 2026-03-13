"""
PharmaTab Research Module
Tumor Growth Visualization
"""

import numpy as np
import plotly.graph_objects as go


class TumorVisualization:


    def plot_tumor_growth(self, tumor_history):

        """
        2D tumor growth curve
        """

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=tumor_history,
                mode="lines",
                name="Tumor Size"
            )
        )

        fig.update_layout(
            title="Tumor Growth Over Time",
            xaxis_title="Time Step",
            yaxis_title="Tumor Size"
        )

        fig.show()


    def plot_resistance(self,
                        sensitive_history,
                        resistant_history):

        """
        Plot resistant vs sensitive cells
        """

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=sensitive_history,
                mode="lines",
                name="Sensitive Cells"
            )
        )

        fig.add_trace(
            go.Scatter(
                y=resistant_history,
                mode="lines",
                name="Resistant Cells"
            )
        )

        fig.update_layout(
            title="Tumor Population Dynamics",
            xaxis_title="Time",
            yaxis_title="Cell Count"
        )

        fig.show()


    def plot_3d_tumor(self,
                      tumor_history):

        """
        3D tumor growth visualization
        """

        x = np.arange(len(tumor_history))

        y = tumor_history

        z = np.sqrt(tumor_history)

        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode='lines',
                    line=dict(width=6)
                )
            ]
        )

        fig.update_layout(
            title="3D Tumor Growth Visualization",
            scene=dict(
                xaxis_title="Time",
                yaxis_title="Tumor Size",
                zaxis_title="Growth Dimension"
            )
        )

        fig.show()