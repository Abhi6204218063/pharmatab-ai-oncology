from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os


class PDFExporter:

    def export(self, report_text):

        styles = getSampleStyleSheet()

        story = []

        # report text

        for line in report_text.split("\n"):

            story.append(Paragraph(line, styles["Normal"]))

            story.append(Spacer(1,6))


        # ---------- Tumor Evolution ----------

        try:

            if os.path.exists("tumor_simulation.png"):

                story.append(Spacer(1,20))

                story.append(Paragraph("Tumor Evolution Simulation", styles["Heading2"]))

                story.append(Spacer(1,10))

                story.append(Image("tumor_simulation.png", width=450, height=280))

        except:
            pass


        # ---------- Resistance Evolution ----------

        try:

            if os.path.exists("tumor_resistance.png"):

                story.append(Spacer(1,20))

                story.append(Paragraph("Tumor Resistance Evolution", styles["Heading2"]))

                story.append(Spacer(1,10))

                story.append(Image("tumor_resistance.png", width=450, height=280))

        except:
            pass


        # ---------- Virtual Cohort ----------

        try:

            if os.path.exists("cohort_simulation.png"):

                story.append(Spacer(1,20))

                story.append(Paragraph("Virtual Patient Cohort Simulation", styles["Heading2"]))

                story.append(Spacer(1,10))

                story.append(Image("cohort_simulation.png", width=450, height=280))

        except:
            pass


        # ---------- Survival Curve ----------

        try:

            if os.path.exists("survival_curve.png"):

                story.append(Spacer(1,20))

                story.append(Paragraph("Kaplan-Meier Survival Prediction", styles["Heading2"]))

                story.append(Spacer(1,10))

                story.append(Image("survival_curve.png", width=450, height=280))

        except:
            pass


        pdf = SimpleDocTemplate("treatment_plan.pdf")

        pdf.build(story)