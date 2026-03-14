from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import pandas as pd


class PDFExporter:

    def generate_report(self, mutations, therapy_plan,
                        tumor_plot=None, survival_plot=None):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)

        styles = getSampleStyleSheet()

        elements = []

        # -----------------------------
        # Title
        # -----------------------------

        elements.append(
            Paragraph(
                "PharmaTab Precision Oncology Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        # -----------------------------
        # Mutation Summary
        # -----------------------------

        elements.append(
            Paragraph(
                "Detected Tumor Mutations",
                styles["Heading2"]
            )
        )

        if isinstance(mutations, pd.DataFrame):

            table_data = [list(mutations.columns)]

            table_data += mutations.head(10).values.tolist()

            table = Table(table_data)

            elements.append(table)

        elements.append(Spacer(1, 20))

        # -----------------------------
        # Therapy Recommendation
        # -----------------------------

        elements.append(
            Paragraph(
                "Recommended Therapy Strategy",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                str(therapy_plan),
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # -----------------------------
        # Tumor Simulation Plot
        # -----------------------------

        if tumor_plot:

            elements.append(
                Paragraph(
                    "Tumor Evolution Simulation",
                    styles["Heading2"]
                )
            )

            elements.append(
                Image(tumor_plot, width=400, height=250)
            )

            elements.append(Spacer(1, 20))

        # -----------------------------
        # Survival Curve
        # -----------------------------

        if survival_plot:

            elements.append(
                Paragraph(
                    "Kaplan-Meier Survival Analysis",
                    styles["Heading2"]
                )
            )

            elements.append(
                Image(survival_plot, width=400, height=250)
            )

            elements.append(Spacer(1, 20))

        # -----------------------------
        # Clinical Notes
        # -----------------------------

        elements.append(
            Paragraph(
                "Clinical Interpretation",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                """
The recommended therapy strategy is derived from
genomic mutation analysis and therapy optimization models.

These predictions are intended for computational research
purposes and should be clinically validated before
medical decision making.
                """,
                styles["Normal"]
            )
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer