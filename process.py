import sys
from decimal import Decimal, ROUND_HALF_EVEN

import bs4
import csv

csv_output = csv.writer(sys.stdout)


def process_table(table):
    region = None
    remark = None
    for row in table.select("tr"):
        cells = [
            c.get_text("\n").replace("\xa0", " ").strip() for c in row.select("td")
        ]
        if cells[0] and "\n" not in cells[0]:
            region = cells[0]
            remark = "-"
        if len(cells) == 2:
            # HACK
            if region == "Cuba" and cells[0] and cells[0][0].isdigit():
                cells.insert(0, "")
            else:
                remark = cells[1].strip(":")
                continue
        if len(cells) != 3:
            print("!!!!", cells, file=sys.stderr)
            continue
        region = cells[0] or region
        prices = cells[1].replace(" ", "\n").split("\n")
        descriptions = cells[2].split("\n")
        for price_str, description in zip(prices, descriptions):
            price_chf = Decimal(int(price_str))
            assert "\n" not in region
            csv_output.writerow([region, remark, description, price_chf])
        # print(cells)
    pass


def main():
    with open("./ind_taxes.html", "r") as infp:
        soup = bs4.BeautifulSoup(infp.read(), features="html.parser")

    content = soup.select_one(".content")

    for table in content.select("table"):
        process_table(table)
        return


if __name__ == "__main__":
    main()
