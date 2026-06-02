from datetime import timedelta

SMP_RATE = 187.18


def weekly_salary(annual_salary, fte=1.0):
    return (annual_salary * fte) / 52


def calculate_return_date(leave_start):
    return leave_start + timedelta(weeks=52)


def calculate_pay_schedule(annual_salary, fte=1.0):
    weekly_pay = weekly_salary(annual_salary, fte)

    full_pay_total = weekly_pay * 26
    smp_total = SMP_RATE * 13

    total_pay = full_pay_total + smp_total

    return {
        "weekly_salary": round(weekly_pay, 2),
        "full_pay_total": round(full_pay_total, 2),
        "smp_total": round(smp_total, 2),
        "total_pay": round(total_pay, 2)
    }


def calculate_qualifying_week(due_date):
    days_since_sunday = (due_date.weekday() + 1) % 7

    ewc_start = due_date - timedelta(days=days_since_sunday)

    qualifying_start = ewc_start - timedelta(weeks=15)

    qualifying_end = qualifying_start + timedelta(days=6)

    return {
        "ewc_start": ewc_start,
        "qualifying_start": qualifying_start,
        "qualifying_end": qualifying_end
    }


def qualifies_for_smp(employment_start_date, due_date):

    qualifying = calculate_qualifying_week(due_date)

    service_days = (
        qualifying["qualifying_end"] -
        employment_start_date
    ).days

    service_weeks = service_days / 7

    return service_weeks >= 26


def qualifies_for_oxford_scheme(
    employment_start_date,
    due_date,
    intends_to_return
):

    if employment_start_date > due_date:
        return False

    if not intends_to_return:
        return False

    return True