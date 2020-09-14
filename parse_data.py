from csv import writer
from csv import reader
from datetime import date, timedelta
import os

def update_and_save(csv_filename, remove_old = True):
    default_text = '-'
    output_filename = csv_filename + "_data"

    with open(csv_filename, 'r') as read_obj, \
            open(output_filename, 'w', newline='') as write_obj:

        csv_reader = reader(read_obj)

        csv_writer = writer(write_obj)

        dates_prices = {}

        # Dictionary to keep the data about days and price
        data = list(csv_reader)

        NUMBER_OF_ROWS = len(data)

        for i,row in enumerate(data):
            # Adding new column title to the first string
            if i==0:
                row.append(r'3day_before_change')
                continue

            #Adding 'current' date to dictionary with close price
            dates_prices[row[0]] = float(row[4])

            row_date = row[0].split("-")
            row_date_days = int(row_date[0])
            row_date_months = int(row_date[1])
            row_date_years = int(row_date[2])

            row_date_datime = date(row_date_days,row_date_months,row_date_years)
            price_date_3_days_before = (row_date_datime - timedelta(days=3)).strftime("%Y-%m-%d")

            #if we have already met a day 3 days earlier adding stats
            if price_date_3_days_before in dates_prices.keys():
                current_price = float(row[3])
                price_3_days_before = dates_prices[price_date_3_days_before]
                row.append(str(current_price/price_3_days_before))
            else: # adding default "-"
                row.append(default_text)

            #writing updated row to new file
            csv_writer.writerow(row)


        #delete old file
        os.remove(csv_filename)
        os.rename(output_filename, csv_filename)

def save_news(news_data, output_filename):

    with open(output_filename, 'w', newline='') as write_obj:

        csv_writer = writer(write_obj)
        csv_writer.writerow(["title","link"])
        for n in news_data:
            csv_writer.writerow([n["title"],n["link"]])
