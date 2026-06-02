import streamlit as st
from datetime import datetime

from calculations import (
    calculate_pay_schedule,
    calculate_return_date,
    calculate_qualifying_week,
    qualifies_for_smp,
    qualifies_for_oxford_scheme
)

st.set_page_config(
    page_title="Oxford Maternity Pay Calculator",
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

    smp_eligible = qualifies_for_smp(
        employment_start_date,
        due_date
    )

    oxford_eligible = qualifies_for_oxford_scheme(
        employment_start_date,
        due_date,
        intends_to_return
    )

    st.subheader("Eligibility Assessment")

    st.write(
        f"Oxford Enhanced Scheme: {'✓ Eligible' if oxford_eligible else '✗ Not Eligible'}"
    )

    st.write(
        f"SMP Eligibility: {'✓ Eligible' if smp_eligible else '✗ Not Eligible'}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Weekly Salary",
            f"£{results['weekly_salary']:,.2f}"
        )

    with col2:
        st.metric(
            "Estimated Total Maternity Pay",
            f"£{results['total_pay']:,.2f}"
        )

    st.subheader("Important Dates")

    st.write(
        f"Employment Start Date: "
        f"{employment_start_date.strftime('%d %B %Y')}"
    )

    st.write(
        f"Expected Due Date: "
        f"{due_date.strftime('%d %B %Y')}"
    )

    st.write(
        f"Maternity Leave Start Date: "
        f"{leave_start.strftime('%d %B %Y')}"
    )

    st.write(
        f"Expected Return Date: "
        f"{return_date.strftime('%d %B %Y')}"
    )

    st.subheader("Qualifying Week")

    st.write(
        f"{qualifying['qualifying_start'].strftime('%d %B %Y')} "
        f"to "
        f"{qualifying['qualifying_end'].strftime('%d %B %Y')}"
    )

    st.subheader("Payment Breakdown")

    st.write(
        f"26 Weeks Full Pay: £{results['full_pay_total']:,.2f}"
    )

    st.write(
        f"13 Weeks SMP: £{results['smp_total']:,.2f}"
    )
    st.divider()

    st.caption(
    "Version 0.1 | Released June 2026"
)