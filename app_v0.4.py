import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from calculations import (
    calculate_pay_schedule,
    calculate_return_date,
    calculate_qualifying_week,
    qualifies_for_smp,
    qualifies_for_oxford_scheme,
    calculate_maternity_timeline
)

st.set_page_config(
    page_title="Oxford University Maternity Pay Calculator",
    layout="wide"
)

st.title("Oxford University Maternity Pay Calculator")
st.caption("Beta Version")

st.info(
    """
    This calculator provides an estimate only.

    Please confirm maternity leave and pay entitlements
    with Oxford University HR and Payroll.

    This tool is not an official University system.
    """
)

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

employment_start_text = st.text_input(
    "Employment Start Date (DD/MM/YYYY)",
    value="01/09/2024"
)

due_date_text = st.text_input(
    "Expected Due Date (DD/MM/YYYY)",
    value="03/06/2026"
)

leave_start_text = st.text_input(
    "Maternity Leave Start Date (DD/MM/YYYY)",
    value="11/06/2026"
)

intends_to_return = st.checkbox(
    "I intend to return to work",
    value=True
)

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
        "Please enter all dates as DD/MM/YYYY"
    )

    st.stop()

if st.button("Calculate"):

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

    st.subheader("Maternity Leave Schedule")

    timeline_data = pd.DataFrame([
        {
            "Period": "Full Pay",
            "Start": timeline["full_pay_start"],
            "Finish": timeline["full_pay_end"]
        },
        {
            "Period": "SMP",
            "Start": timeline["smp_start"],
            "Finish": timeline["smp_end"]
        },
        {
            "Period": "Unpaid Leave",
            "Start": timeline["unpaid_start"],
            "Finish": timeline["unpaid_end"]
        }
    ])

    fig = px.timeline(
        timeline_data,
        x_start="Start",
        x_end="Finish",
        y="Period",
        color="Period",
        color_discrete_map={
            "Full Pay": "#66BB6A",
            "SMP": "#FFA726",
            "Unpaid Leave": "#EF5350"
        }
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="",
        showlegend=True
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Pay Period Summary")

    summary1, summary2, summary3 = st.columns(3)

    with summary1:
        st.success(
            f"FULL PAY\n\n"
            f"{timeline['full_pay_start'].strftime('%d %b %Y')} → "
            f"{timeline['full_pay_end'].strftime('%d %b %Y')}"
        )

    with summary2:
        st.warning(
            f"SMP\n\n"
            f"{timeline['smp_start'].strftime('%d %b %Y')} → "
            f"{timeline['smp_end'].strftime('%d %b %Y')}"
        )

    with summary3:
        st.error(
            f"UNPAID LEAVE\n\n"
            f"{timeline['unpaid_start'].strftime('%d %b %Y')} → "
            f"{timeline['unpaid_end'].strftime('%d %b %Y')}"
        )

    st.subheader("Leave Period Details")

    leave_periods = pd.DataFrame(
        [
            {
                "Period": "🟩 Full Pay",
                "Start Date": timeline["full_pay_start"].strftime("%d %B %Y"),
                "End Date": timeline["full_pay_end"].strftime("%d %B %Y"),
                "Duration": "26 weeks (182 days)"
            },
            {
                "Period": "🟧 SMP",
                "Start Date": timeline["smp_start"].strftime("%d %B %Y"),
                "End Date": timeline["smp_end"].strftime("%d %B %Y"),
                "Duration": "13 weeks (91 days)"
            },
            {
                "Period": "🟥 Unpaid Leave",
                "Start Date": timeline["unpaid_start"].strftime("%d %B %Y"),
                "End Date": timeline["unpaid_end"].strftime("%d %B %Y"),
                "Duration": "13 weeks (92 days)"
            }
        ]
    )

    st.dataframe(
        leave_periods,
        hide_index=True,
        width="stretch"
    )

    st.write("")

    card1, card2, card3, card4 = st.columns(4)

    with card1:
        with st.container(border=True):

            st.subheader("📅 Key Dates")

            st.write("Employment Start Date")
            st.write(employment_start_date.strftime("%d %B %Y"))

            st.write("Expected Due Date")
            st.write(due_date.strftime("%d %B %Y"))

            st.write("Maternity Leave Start Date")
            st.write(leave_start.strftime("%d %B %Y"))

            st.write("Expected Return Date")
            st.write(return_date.strftime("%d %B %Y"))

    with card2:
        with st.container(border=True):

            st.subheader("✅ Eligibility")

            st.write("Oxford Enhanced Scheme")

            if oxford_eligible:
                st.success("Eligible")
            else:
                st.error("Not Eligible")

            st.write("SMP Eligibility")

            if smp_eligible:
                st.success("Eligible")
            else:
                st.error("Not Eligible")

    with card3:
        with st.container(border=True):

            st.subheader("💷 Pay Summary")

            st.metric(
                "Weekly Salary",
                f"£{results['weekly_salary']:,.2f}"
            )

            st.metric(
                "Total Maternity Pay",
                f"£{results['total_pay']:,.2f}"
            )

    with card4:
        with st.container(border=True):

            st.subheader("🕒 Qualifying Week")

            st.write(
                qualifying["qualifying_start"].strftime("%d %B %Y")
            )

            st.write("to")

            st.write(
                qualifying["qualifying_end"].strftime("%d %B %Y")
            )

            st.divider()

            st.subheader("💰 Breakdown")

            st.write(
                f"Full Pay: £{results['full_pay_total']:,.2f}"
            )

            st.write(
                f"SMP: £{results['smp_total']:,.2f}"
            )

st.divider()

st.caption(
    "Version 0.4 | Released June 2026"
)
