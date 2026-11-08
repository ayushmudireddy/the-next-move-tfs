import streamlit as st
import math as math
st.title("Welcome to the Toyota Advisor!")
st.write("Find the smartest next move for your Toyota!")

car = st.selectbox(
    "Select your Toyota",
    ["Camry", "Corolla", "RAV4", "Prius"]
)

style = st.selectbox(
    "How would you describe your driving style?",
    ["Conservative", "Aggressive", "Performance/Track Driving"],
    help = "Note: Conservative means you gently accelerate and brake, Agressive driving means you heavily accelerate and brake, and Performance/Track Driving means you regularly take your vehicle to the track."
)


mileage = st.number_input(
    "Current Mileage",
    min_value=0
)

prev_maintenance = st.selectbox(
    "How long ago was your last maintenance?",
    ["Less than 6 months or below 5,000 miles", "Less than a year or below 10,000 miles", "Over  a year or over 10,000 miles"]
)

tire_tread = st.selectbox(
    "How is your tire tread looking?",
    ["Good", "Moderate", "Heavy"],
    help = "(Tip: Use the Penny method! Grab a penny, point Abraham Lincoln's face down. If you can't see the top of his forehead, your tread is good! If you can see it, the tread is moderate. If you can see his entire face, your tire tread is heavy.)"
)   

vehicle_condition = st.selectbox(
    "How would you rate your vehicle's overall condition?",
    ["Excellent", "Good", "Fair", "Poor"]
)

mechanical_issues = st.multiselect(
    "Are you currently experiencing any vehicle issues?",
    [
        "Engine problems",
        "Transmission problems",
        "Brake problems",
        "Suspension problems",
        "Battery problems",
        "Electrical problems",
        "Other"
    ]
)

warning_lights = st.multiselect(
    "Do you have any dashboard warning lights on?",
    [
        "Check Engine",
        "Oil Pressure",
        "Battery",
        "ABS (Anti-Lock Braking System)",
        "Tire Pressure",
        "Other"
    ]
)
repair_estimate = st.selectbox(
    "Have you received a repair estimate from a mechanic?",
    ["Yes", "No"]
)
if repair_estimate == "Yes":
    repair_cost = st.number_input(
    "What are the estimated cost of needed repairs?",
    min_value=0,
    value=0,
    step=100
    )   


accident_history = st.selectbox(
    "Has your vehicle been in an accident?",
    [
        "No",
        "Yes - Minor Damage",
        "Yes - Major Damage",
        "Unsure"
    ]
)

annual_mileage = st.number_input(
    "Approximately how many miles do you drive per year?",
    min_value=0,
    value=12000,
    step=1000
)

ownership = st.selectbox(
    "What is your vehicle's ownership status?",
    [
        "Paid Off in Full",
        "Currently Financing",
        "Currently Leasing"
    ]
)

if ownership == "Paid Off in Full":
    ownership_status = "currently own your vehicle."
elif ownership == "Currently Financing":
    ownership_status = "are currently financing your vehicle."
elif ownership == "Currently Leasing":
    ownership_status = "are currently leasing your vehicle."

if accident_history == "No":
    accident = "never been in an accident."
elif accident_history == "Yes - Minor Damage":
    accident = "has been in an accident that has caused minor damage to your vehicle."
elif accident_history == "Yes - Major Damage":
    accident = "has been in an accident that has caused major damage to your vehicle."
elif accident_history == "Unsure":
    accident = "has been in no known accidents."

if car == "Camry":
    min_yr = 1983
elif car == "Corolla":
    min_yr = 1968
elif car == "RAV4":
    min_yr = 1996
elif car == "Prius":
    min_yr = 2001



manufacture_yr = st.number_input(
    "Year of manufacture",
    min_value = min_yr,
    max_value = 2028,
    value = 2026
)
has_estimate = False;
if repair_estimate == "Yes":
    has_estimate = True;
#add api or ai thing and then analyze data to include a brief car overview, reasoning, and then numbers/stats
if st.button("Analyze My Car"):
    st.success(f"Analyzing your Toyota {car}!")
    st.subheader("Vehicle Overview:")
    st.write(f"Vehicle Model and Year: {manufacture_yr} Toyota {car}")
    st.write(f"Current mileage: {mileage:,}")
    st.write(f"Driving Style: {style}")
    st.write(f"Most Recent Maintenance: {prev_maintenance}")
    st.write(f"Tire Tread: {tire_tread}")
    st.write(f"Mechanical Issues: {', '.join(mechanical_issues) if mechanical_issues else 'None'}")
    st.write(f"Warning Lights: {', '.join(warning_lights) if warning_lights else 'None'}")
    if has_estimate:
        st.write(f"Repair Costs: ${repair_cost}")
    st.write(f"Your vehicle has {accident}")
    st.write(f"You {ownership_status}")


st.subheader("Try this monthly vehicle finance calculator!")
approx_price = st.selectbox(
    "Roughly how expensive is your car?",
    [   
        "Low(Under $40,000)",
        "Medium($40,000-$80,000)",
        "High($80,000-$150,000)",
        "Luxury/Performance(Over $150,000)"
    ]
)
loan_length = st.selectbox(
    "What is your loan term(in months)?",
    [24, 36, 48, 60, 72, 84],
    index = 3
)
if approx_price == "Low(Under $40,000)":
    purchase_price = st.slider("Vehicle purchase price", min_value=100.0, max_value=39999.0, step = 100.0)
elif approx_price == "Medium($40,000-$80,000)":
    purchase_price = st.slider("Vehicle purchase price", min_value=40000.0, max_value=79999.0, step = 100.0)
elif approx_price == "High($80,000-$150,000)":
    purchase_price = st.slider("Vehicle purchase price", min_value=80000.0, max_value=149999.0, step = 100.0)
elif approx_price == "Luxury/Performance(Over $150,000)":
    purchase_price = st.slider("Vehicle purchase price", min_value=150000.0, max_value=2000000.0, step = 100.0)
down_payment = st.slider("Down payment", min_value=0.0, max_value=purchase_price, value = purchase_price*0.12, step = 10.0)
interest = st.slider("APR (Annual interest rate)", min_value=0.0, max_value=20.0, value = 8.0, step = 0.1)

loan_amount = purchase_price - down_payment

monthly_interest = interest/1200 #/100 for percentage and /12 for monthly payment

if monthly_interest == 0:
    monthly_payment = loan_amount/loan_length
else:
    monthly_payment = (
        loan_amount * monthly_interest/(1-(1+monthly_interest)**(-loan_length))
    )

total_loan_payments = monthly_payment*loan_length
total_interest = total_loan_payments-loan_amount
total_cost = total_loan_payments+down_payment

monthly_payment = math.ceil(monthly_payment*100)/100
total_interest = math.ceil(total_interest*100)/100
total_cost = math.ceil(total_cost*100)/100

st.subheader("Here are your results!")
st.write(f"Your monthly payment is ${monthly_payment:,.2f}")
st.write(f"Your total loan payments are ${total_loan_payments:,.2f}")
st.write(f"Your total interest is ${total_interest:,.2f}")
st.write(f"Your total purchase cost is ${total_cost:,.2f}")
