import streamlit as st
from datetime import datetime
import calendar

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

def render_month(
    year,
    month,
    timeline
):

    cal = calendar.monthcalendar(
        year,
        month
    )

    month_name = calendar.month_name[month]

    html = (
        f"<div style='border:1px solid #333;"
        f"padding:10px;"
        f"border-radius:8px;"
        f"background:#111827;'>"
        f"<h4 style='text-align:center;'>"
        f"{month_name} {year}"
        f"</h4>"
        f"<table style='width:100%;"
        f"text-align:center;"
        f"font-size:12px;"
        f"border-collapse:collapse;'>"
        f"<tr>"
        f"<th>M</th>"
        f"<th>T</th>"
        f"<th>W</th>"
        f"<th>T</th>"
        f"<th>F</th>"
        f"<th>S</th>"
        f"<th>S</th>"
        f"</tr>"
    )

    for week in cal:

        html += "<tr>"

        for day in week:

            if day == 0:

                html += "<td></td>"

            else:

                current_date = datetime(
                    year,
                    month,
                    day
                ).date()

                colour = "#1f2937"

                if (
                    timeline["full_pay_start"]
                    <= current_date
                    <= timeline["full_pay_end"]
                ):
                    colour = "#66BB6A"

                elif (
                    timeline["smp_start"]
                    <= current_date
                    <= timeline["smp_end"]
                ):
                    colour = "#FFA726"

                elif (
                    timeline["unpaid_start"]
                    <= current_date
                    <= timeline["unpaid_end"]
                ):
                    colour = "#EF5350"

                html += (
                    f"<td style='"
                    f"background:{colour};"
                    f"padding:4px;"
                    f"border:1px solid #222;'>"
                    f"{day}"
                    f"</td>"
                )

        html += "</tr>"

    html += "</table></div>"

    return html

from calculations import (
    calculate_pay_schedule,
    calculate_return_date,
    calculate_qualifying_week,
    qualifies_for_smp,
    qualifies_for_oxford_scheme,
    calculate_maternity_timeline
)

st.set_page_config(
    page_title="Oxford University Maternity Dashboard",
    layout="wide"
)

st.title("Oxford University Maternity Pay Calculator")
st.caption("Version 1.0 Dashboard")

st.info(
    """
    This calculator provides an estimate only.

    Please confirm maternity leave and pay entitlements
    with Oxford University HR and Payroll.

    This tool is not an official University system.
    """
)

with st.expander("Employee Details", expanded=True):

    annual_salary = st.number_input(
        "Annual Salary (£)",
        min_value=0.0,
        value=45000.0,
        step=1000.0
    )

    fte = st.number_input(
        "FTE",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.1
    )

    employment_start_text = st.date_input(
        "Employment Start Date",
    )

    due_date_text = st.date_input(
        "Expected Due Date",
    )

    leave_start_text = st.date_input(
        "Maternity Leave Start Date",
    )

    pdf_filename = st.text_input(
    "Employee Name for PDF",
    value=""
)

    intends_to_return = st.checkbox(
        "I intend to return to work",
        value=True
    )

calculate = st.button(
    "Calculate",
    type="primary",
    use_container_width=True
)

def generate_pdf_report(
    employment_start_date,
    due_date,
    leave_start,
    return_date,
    results,
    timeline,
    qualifying,
    oxford_eligible,
    smp_eligible
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Oxford University Maternity Pay Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Employment Start Date: "
            f"{employment_start_date.strftime('%d %B %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Expected Due Date: "
            f"{due_date.strftime('%d %B %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Maternity Leave Start Date: "
            f"{leave_start.strftime('%d %B %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Expected Return Date: "
            f"{return_date.strftime('%d %B %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Oxford Enhanced Scheme: "
            f"{'Eligible' if oxford_eligible else 'Not Eligible'}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"SMP Eligibility: "
            f"{'Eligible' if smp_eligible else 'Not Eligible'}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Weekly Salary: "
            f"£{results['weekly_salary']:,.2f}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Estimated Total Pay: "
            f"£{results['total_pay']:,.2f}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Leave Periods",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Full Pay: "
            f"{timeline['full_pay_start'].strftime('%d %b %Y')} "
            f"to "
            f"{timeline['full_pay_end'].strftime('%d %b %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"SMP: "
            f"{timeline['smp_start'].strftime('%d %b %Y')} "
            f"to "
            f"{timeline['smp_end'].strftime('%d %b %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Unpaid Leave: "
            f"{timeline['unpaid_start'].strftime('%d %b %Y')} "
            f"to "
            f"{timeline['unpaid_end'].strftime('%d %b %Y')}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Qualifying Week",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"{qualifying['qualifying_start'].strftime('%d %b %Y')} "
            f"to "
            f"{qualifying['qualifying_end'].strftime('%d %b %Y')}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

if calculate:

    try:

        employment_start_date = datetime.strptime(
            employment_start_text,
            "%d/%m/%Y"
        ).date()

        due_date = datetime.strptime(
            due_date_text,
            "%d/%m/%Y"
        ).date()

        leave_start = datetime.strptime(
            leave_start_text,
            "%d/%m/%Y"
        ).date()

    except ValueError:

        st.error(
            "Please enter all dates using DD/MM/YYYY format."
        )

        st.stop()

    results = calculate_pay_schedule(
        annual_salary=annual_salary,
        fte=fte
    )

    qualifying = calculate_qualifying_week(
        due_date
    )

    return_date = calculate_return_date(
        leave_start
    )

    timeline = calculate_maternity_timeline(
        leave_start
    )

    smp_eligible = qualifies_for_smp(
        employment_start_date,
        due_date
    )

    oxford_eligible = qualifies_for_oxford_scheme(
        employment_start_date,
        due_date,
        intends_to_return
    )
    pdf_data = generate_pdf_report(
        employment_start_date,
        due_date,
        leave_start,
        return_date,
        results,
        timeline,
        qualifying,
        oxford_eligible,
        smp_eligible
    )

    st.divider()

    card1, card2, card3, card4 = st.columns(4)

    with card1:

        with st.container(border=True):

            st.subheader("📅 Key Dates")

            st.write(
                f"Start: {employment_start_date.strftime('%d %b %Y')}"
            )

            st.write(
                f"Due: {due_date.strftime('%d %b %Y')}"
            )

            st.write(
                f"Leave: {leave_start.strftime('%d %b %Y')}"
            )

            st.write(
                f"Return: {return_date.strftime('%d %b %Y')}"
            )

    with card2:

        with st.container(border=True):

            st.subheader("✅ Eligibility")

            if oxford_eligible:
                st.success("Oxford Scheme Eligible")
            else:
                st.error("Oxford Scheme Not Eligible")

            if smp_eligible:
                st.success("SMP Eligible")
            else:
                st.error("SMP Not Eligible")

    with card3:

        with st.container(border=True):

            st.subheader("💷 Pay Summary")

            st.metric(
                "Weekly Salary",
                f"£{results['weekly_salary']:,.2f}"
            )

            st.metric(
                "Total Pay",
                f"£{results['total_pay']:,.2f}"
            )

    with card4:

        with st.container(border=True):

            st.subheader("🕒 Qualifying Week")

            st.write(
                qualifying["qualifying_start"].strftime(
                    "%d %b %Y"
                )
            )

            st.write("to")

            st.write(
                qualifying["qualifying_end"].strftime(
                    "%d %b %Y"
                )
            )

    st.divider()

    st.subheader("Leave Period Details")

    st.dataframe(
        {
            "Period": [
                "Full Pay",
                "SMP",
                "Unpaid Leave"
            ],
            "Start Date": [
                timeline["full_pay_start"].strftime("%d %b %Y"),
                timeline["smp_start"].strftime("%d %b %Y"),
                timeline["unpaid_start"].strftime("%d %b %Y")
            ],
            "End Date": [
                timeline["full_pay_end"].strftime("%d %b %Y"),
                timeline["smp_end"].strftime("%d %b %Y"),
                timeline["unpaid_end"].strftime("%d %b %Y")
            ]
        },
    )

    st.subheader("Maternity Leave Calendar")

    st.markdown(
    """
🟩 Full Pay &nbsp;&nbsp;&nbsp;
🟧 SMP &nbsp;&nbsp;&nbsp;
🟥 Unpaid Leave
""",
    unsafe_allow_html=True
)

    start_year = leave_start.year
    start_month = leave_start.month

    months = []

    for i in range(13):

        month = start_month + i
        year = start_year

        while month > 12:
            month -= 12
            year += 1

        months.append(
            (year, month)
        )

    for row in range(5):

        cols = st.columns(4)

        for col in range(4):

            idx = row * 4 + col

            if idx >= len(months):
                continue

            year, month = months[idx]

            with cols[col]:

                st.markdown(
                    render_month(
                        year,
                        month,
                        timeline
                    ),
                    unsafe_allow_html=True
                )

    st.divider()

    pdf_data = generate_pdf_report(
        employment_start_date,
        due_date,
        leave_start,
        return_date,
        results,
        timeline,
        qualifying,
        oxford_eligible,
        smp_eligible
    )

    if pdf_filename:

        filename = (
            f"{pdf_filename}_Maternity_Report.pdf"
        )

    else:

        filename = (
            "Oxford_Maternity_Report.pdf"
        )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_data,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )
