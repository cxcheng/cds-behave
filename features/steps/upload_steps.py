from behave import *
from util import *
from http import HTTPStatus


@given(u'I upload CSV with the following rows')
def step_impl(context):
    read_rows(context)
    generate_file_from_rows(context)
    upload_file(context)


@given(u'I upload CSV with {ncols} instead of 4 columns')
def step_impl(context, ncols):
    n = int(ncols)
    assert 0 < n < 10
    csv_text = ""
    for line in range(4):
        l = "ID {}".format(line)
        for col in range(1, n):
            l += ",{:.2f}".format(col)
        csv_text += "{}\n".format(l)
    context.csv_text = csv_text
    upload_file(context)


@given(u'I upload CSV with the following text')
@then(u'I upload CSV with the following text')
def step_impl(context):
    context.csv_text = context.text
    upload_file(context)


@then(u'I upload the file with different salary')
def step_impl(context):
    assert hasattr(context, "csv_rows")
    for row in context.csv_rows:
        row[3] *= 2.0
    generate_file_from_rows(context)
    upload_file(context)


@then(u'I get success')
def step_impl(context):
    assert hasattr(context, "rs") and context.rs == HTTPStatus.OK


@then(u'I can find all users according to the rows')
def step_impl(context):
    fetch_users(context, minSalary=0, maxSalary=4000, offset=0,limit=30, sort="+id")
    check_users_against_table(context)


@then(u'I get failure')
def step_impl(context):
    assert hasattr(context, "rs") and context.rs != HTTPStatus.OK
