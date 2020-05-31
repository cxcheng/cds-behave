import csv
import io
import requests
from http import HTTPStatus


def read_rows(context):
    assert hasattr(context, "table") and len(context.table.headings) == 4
    csv_users = []
    csv_rows = []
    table = context.table
    for row in table.rows:
        csv_row = []
        for heading in table.headings:
            col = row.get(heading)
            csv_user = {}
            if heading == "salary":
                col = float(col)
            csv_user[heading] = col
            csv_row.append(col)
        csv_users.append(csv_user)
        csv_rows.append(csv_row)
    context.csv_headings = table.headings
    context.csv_users = csv_users
    context.csv_rows = csv_rows


def generate_file_from_rows(context):
    with io.StringIO() as csv_io:
        w = csv.writer(csv_io)
        w.writerow(context.csv_headings)
        for row in context.csv_rows:
            w.writerow(row)
        context.csv_text = csv_io.getvalue()


def upload_file(context):
    assert hasattr(context, "base_url") and hasattr(context, "csv_text")
    url = "{}/users/upload".format(context.base_url)
    files = {"file": ("users.csv", context.csv_text)}
    resp = requests.post(url, files=files)
    context.rs = resp.status_code
    context.rs_json = resp.json()


def fetch_users(context, **kwargs):
    assert hasattr(context, "base_url")
    url = "{}/users".format(context.base_url)
    resp = requests.get(url, params=kwargs)
    context.rs = resp.status_code
    if resp.status_code == HTTPStatus.OK:
        context.rs_json = resp.json()


def check_users_against_table(context):
    assert hasattr(context, "csv_users") and context.rs_json.has_key("results")
    # Check that each user in the table is accounted for in the results
    for csv_user in context.csv_users:
        csv_user_id = csv_user["id"]
        # Scan through the results
        found_user = False
        for result in context.rs_json["results"]:
            assert result.has_key("id")
            if csv_user["id"] == result["id"]:
                assert csv_user["login"] == result["login"] \
                    and csv_user["name"] == result["name"] \
                    and csv_user["salary"] == result["salary"]
                found_user = True
                break
        assert found_user
        



