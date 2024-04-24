import requests
import smtplib
import time

from termcolor import colored
from rich.progress import track
from datetime import datetime,timedelta

header = {

    "apikey":"Kc_AEXMcFMuCY0uK36bwuVK2m-XgKx4f",

    }

def main():
    flights = get_flights()
    best_deal = []
    print(colored("Finding cheapest flight deals......","light_yellow"))
    for flight in flights:
        response,price = get_best_price(flight['iataCode'],flight['lowestPrice'])
        if response:
            best_deal.append({"DEST":flight['iataCode'],"bestprice":price})
        else:
            pass

    if best_deal:
        print(colored(f"{len(best_deal)} cheap flights found","green"))
        send_email(best_deal)
    else:
        print(colored(f"No any new cheap flights :( ","red"))



    
def get_flights():

    url_endpoint = "https://api.sheety.co/d26a10727cb0bff8fbc3810183c86ffc/copyOfFlightDeals/prices"
    response = requests.get(url_endpoint)
    response.raise_for_status()
    data = response.json()
    return data['prices']

def get_best_price(IATA_CODE,price):

    current_date = datetime.now()
    six_months_from_now = current_date + timedelta(days=30*6)
    now = current_date.strftime("%d/%m/%Y")
    tequila_endpoint = "https://api.tequila.kiwi.com/v2/search"

    parameters = {

        "fly_from":"JNB",
        "fly_to":IATA_CODE,
        "date_from":now,
        "date_to":six_months_from_now.strftime("%d/%m/%Y"),
        "curr": "ZAR"
    }

   

    response = requests.get(tequila_endpoint,params=parameters,headers=header)
    response.raise_for_status()
    flight_data = response.json()
    current_price = 0
    initial_price = price
    
    
    for i in flight_data['data']:
        current_price = i['price']
        if current_price < price:
            price = current_price
        
    for i in track(range(5), description=f"Searching {IATA_CODE} for flights..."):
        time.sleep(0.5)

    if price != initial_price and price < initial_price:
        # print(colored(F"{IATA_CODE} FOUND","green"))
        return True,price
    
    else:
        # print(f"None found in {IATA_CODE}")
        return False,initial_price

def register_user():
    
    userreg_Endpoint = "https://api.sheety.co/d26a10727cb0bff8fbc3810183c86ffc/copyOfFlightDeals/users"
    body = {
        "user":{
            "name":input("Enter your name: "),
            "email":input("Enter your email: "),
        },
    }

    response  = requests.post(url=userreg_Endpoint,json=body,headers=header)
    print(response.text)

def send_email(flights):
    flight_deals = ''
    for i in flights:
        flight_deals += f"{i['DEST']}:R{round(i['bestprice'],1)}\n"

    admin_email = "teamcodeclinics@gmail.com"
    password = "npfekqklfoafhexm"

    # starting server and connecting to gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(admin_email,password)

        server.sendmail(from_addr=admin_email,to_addrs='kkndlovu9@gmail.com',msg=f"subject: Flight Deals!\n\n{flight_deals} some great deals right")

    print("email sent :)")

if __name__ == "__main__":
    main()