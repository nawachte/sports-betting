from helper import *
from itertools import combinations
import schedule
import time
import smtplib
from email.mime.text import MIMEText

# [[[[[[[[[[[[[[[calculations]]]]]]]]]]]]]]]
def compute_arbitrage(book1, book2, team1, team2, odds_b1_t1_us, odds_b1_t2_us, odds_b2_t1_us, odds_b2_t2_us, bet_amount):
    # function to convert US odds to decimal
    def convert_us_to_dec(odds_us):
        return (odds_us / 100 + 1) if odds_us > 0 else (100 / abs(odds_us) + 1)
    
    # convert all odds to decimal
    b1t1_dec = convert_us_to_dec(odds_b1_t1_us)
    b1t2_dec = convert_us_to_dec(odds_b1_t2_us)
    b2t1_dec = convert_us_to_dec(odds_b2_t1_us)
    b2t2_dec = convert_us_to_dec(odds_b2_t2_us)

    def calculate_profit(odds_teamA, odds_teamB, bet_amount):
        # implied probabilities
        ipA = 1 / odds_teamA
        ipB = 1 / odds_teamB
        margin = ipA + ipB

        if margin < 1:
            betA = (bet_amount * ipA) / margin
            betB = (bet_amount * ipB) / margin
            profit = (bet_amount / margin) - bet_amount
            return betA, betB, profit
        return None

    # Scenario A: Team1 at Book1, Team2 at Book2
    scenario_A = calculate_profit(b1t1_dec, b2t2_dec, bet_amount)

    # Scenario B: Team2 at Book1, Team1 at Book2
    scenario_B = calculate_profit(b1t2_dec, b2t1_dec, bet_amount)

    # Print results for scenarios that yield true arbitrage
    out_string = ""

    if scenario_A:
        betA, betB, profit = scenario_A
        out_string += f"{team1} VS {team2}\n"
        out_string += f"Scenario A: Bet ${round(betA, 2)} on {team1}({odds_b1_t1_us}) at {book1} and ${round(betB, 2)} on {team2}({odds_b2_t2_us}) at {book2}\n"
        out_string += f"Profit: ${profit}\n\n"

    if scenario_B:
        betA, betB, profit = scenario_B
        out_string += f"{team1} VS {team2}\n"
        out_string += f"Scenario B: Bet ${round(betA, 2)} on {team2}({odds_b1_t2_us}) at {book1} and ${round(betB, 2)} on {team1}({odds_b2_t1_us}) at {book2}\n"
        out_string += f"Profit: ${round(profit,2)}\n\n"
    
    return out_string

# [[[[[[[[[[[[[[[run book data]]]]]]]]]]]]]]]
def run_moneylines(moneylines,bet=10):
    out_string = ""
    for match in list(moneylines.keys()):
        book_list = moneylines[match]
        book_matches = list(combinations(book_list, 2)) #book_matches = [([b1,t1odds,t2odds],[b2,t1odds,t2odds]), ...]
        for bmatch in book_matches:
            b1 = bmatch[0][0]
            b2 = bmatch[1][0]
            t1 = match[0]
            t2 = match[1]
            b1t1_odds = bmatch[0][1]
            b1t2_odds = bmatch[0][2]
            b2t1_odds = bmatch[1][1]
            b2t2_odds = bmatch[1][2]
            out_string += compute_arbitrage(b1,b2,t1,t2,b1t1_odds,b1t2_odds,b2t1_odds,b2t2_odds,bet)
    # out_string += compute_arbitrage("book1","book2","team1","team2",110,-123,-127,123,bet) # testing
    return out_string

# [[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]
def run_calculations():
    # moneylines = get_NFL_moneylines()
    moneylines = get_NBA_moneylines()
    return run_moneylines(moneylines)

def send_email(to_address, subject, body):
    from_address = "############@gmail.com"
    app_password = "###############"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Using Gmail’s SMTP server on port 465 (SSL)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_address, app_password)
        server.send_message(msg)

def job():
    try:
        result = run_calculations()
        if result.strip():  # Check if the string is not empty
            send_email("###########@gmail.com", "sports betting", result)
    except Exception as e:
        send_email(
            "###########@gmail.com",
            "sports betting error",
            f"An error occurred: {e}"
        )

# job() # testing

schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
