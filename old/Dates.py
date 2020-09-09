import re

month_dict = {"Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12", "Jan":"01"}

def wolfe_to_date(wolfe_date):
    parts = re.findall("(\d{2})-(\w{3})-(\d{2})", wolfe_date)

    day = parts[0][0]
    month = month_dict[parts[0][1]]
    year = "20" + parts[0][2]

    return int(year), int(month), int(day)