
import math
import re

import streamlit as st
from google import genai
from google.genai import types


@st.cache_data(ttl=86400, show_spinner=False)
def find_first_year(car):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""
        Search Google for the first production model year
        of the vehicle: {car}.

        Use the earliest production model year worldwide.
        Do not confuse it with a different model or generation.
        If the brand is omitted, assume Toyota.

        Return ONLY the four-digit year.
        If uncertain, return UNKNOWN.
        """,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        ),
    )

    answer = (response.text or "").strip()
    match = re.search(r"\b(?:18|19|20)\d{2}\b", answer)

    source = None

    if response.candidates:
        metadata = response.candidates[0].grounding_metadata

        if metadata and metadata.grounding_chunks:
            for chunk in metadata.grounding_chunks:
                if chunk.web and chunk.web.uri:
                    source = chunk.web.uri
                    break

    if match:
        return int(match.group()), source

    return None, None


st.title("Welcome to the Toyota Advisor!")
st.write("Find the smartest next move for your Toyota!")

car = st.text_input(
    "What Toyota, Lexus, Century, or GR vehicle do you have?",
    placeholder="Toyota Camry, Lexus RX 350, GR Supra...",
)

min_yr = 1900

if car.strip():
    try:
        first_year, source = find_first_year(car.strip().lower())

        if first_year and 1900 <= first_year <= 2028:
            min_yr = first_year
            st.success(f"First model year found: {min_yr}")

            if source:
                st.link_button("View source", source)
            else:
                st.caption("Source not available. Please verify the year.")
        else:
            st.warning("First production year could not be verified.")

    except Exception as e:
        st.warning(f"Year lookup unavailable: {e}")

manufacture_yr = st.number_input(
    "Vehicle Model Year",
    min_value=min_yr,
    max_value=2028,
    value=max(2026, min_yr),
    step=1,
    key=f"vehicle_year_{car.strip().lower()}_{min_yr}",
)

style = st.selectbox(
    "How would you describe your driving style?",
    ["Conservative", "Aggressive", "Performance/Track Driving"],
    help=(
        "Conservative means gently accelerating and braking. "
        "Aggressive means heavily accelerating and braking. "
        "Performance/Track Driving means regularly driving on a track."
    ),
)

mileage = st.number_input(
    "Current Mileage",
    min_value=0,
)

prev_maintenance = st.selectbox(
    "How long ago was your last maintenance?",
    [
        "Less than 6 months or below 5,000 miles",
        "Less than a year or below 10,000 miles",
        "Over a year or over 10,000 miles",
    ],
)

tire_tread = st.selectbox(
    "How is your tire tread looking?",
    ["Good", "Moderate", "Heavy"],
    help=(
        "Penny test: place a penny in the tread with Lincoln's head down. "
        "If you can see the top of his head, the tread may be too worn."
    ),
)

vehicle_condition = st.selectbox(
    "How would you rate your vehicle's overall condition?",
    ["Excellent", "Good", "Fair", "Poor"],
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
        "Other",
    ],
)

warning_lights = st.multiselect(
    "Do you have any dashboard warning lights on?",
    [
        "Check Engine",
        "Oil Pressure",
        "Battery",
        "ABS (Anti-Lock Braking System)",
        "Tire Pressure",
        "Other",
    ],
)

repair_estimate = st.selectbox(
    "Have you received a repair estimate from a mechanic?",
    ["Yes", "No"],
)

repair_cost = None

if repair_estimate == "Yes":
    repair_cost = st.number_input(
        "What is the estimated cost of needed repairs?",
        min_value=0,
        value=0,
        step=100,
    )

accident_history = st.selectbox(
    "Has your vehicle been in an accident?",
    ["No", "Yes - Minor Damage", "Yes - Major Damage", "Unsure"],
)

annual_mileage = st.number_input(
    "Approximately how many miles do you drive per year?",
    min_value=0,
    value=12000,
    step=1000,
)

ownership = st.selectbox(
    "What is your vehicle's ownership status?",
    ["Paid Off in Full", "Currently Financing", "Currently Leasing"],
)

replacement_budget = st.number_input(
    "What is your maximum budget for a replacement vehicle? ($)",
    min_value=0,
    value=0,
    step=1000,
    help="Optional. Enter 0 if you aren't sure or aren't considering a replacement.",
)

if ownership == "Paid Off in Full":
    ownership_status = "currently own your vehicle."
elif ownership == "Currently Financing":
    ownership_status = "are currently financing your vehicle."
else:
    ownership_status = "are currently leasing your vehicle."


# Vehicle overview
if st.button("Show Vehicle Overview", disabled=not car.strip()):
    st.success(f"Analyzing your {car}!")
    st.subheader("Vehicle Overview:")

    st.write(f"Vehicle Model and Year: {manufacture_yr} {car}")
    st.write(f"Current mileage: {mileage:,}")
    st.write(f"Driving Style: {style}")
    st.write(f"Most Recent Maintenance: {prev_maintenance}")
    st.write(f"Tire Tread: {tire_tread}")

    st.write(
        f"Mechanical Issues: {', '.join(mechanical_issues) if mechanical_issues else 'None'}"
    )

    st.write(
        f"Warning Lights: {', '.join(warning_lights) if warning_lights else 'None'}"
    )

    if repair_estimate == "Yes":
        st.write(f"Repair Costs: ${repair_cost:,}")

    st.write(f"Accident History: {accident_history}")
    st.write(f"You {ownership_status}")


# Vehicle financing calculator
st.subheader("Try this monthly vehicle finance calculator!")

approx_price = st.selectbox(
    "What price range is the vehicle you're considering financing?",
    [
        "Low(Under $40,000)",
        "Medium($40,000-$80,000)",
        "High($80,000-$150,000)",
        "Luxury/Performance(Over $150,000)",
    ],
)

loan_length = st.selectbox(
    "What is your loan term (in months)?",
    [24, 36, 48, 60, 72, 84],
    index=3,
)

if approx_price == "Low(Under $40,000)":
    purchase_price = st.slider(
        "Vehicle purchase price",
        min_value=100.0,
        max_value=39999.0,
        step=100.0,
    )

elif approx_price == "Medium($40,000-$80,000)":
    purchase_price = st.slider(
        "Vehicle purchase price",
        min_value=40000.0,
        max_value=79999.0,
        step=100.0,
    )

elif approx_price == "High($80,000-$150,000)":
    purchase_price = st.slider(
        "Vehicle purchase price",
        min_value=80000.0,
        max_value=149999.0,
        step=100.0,
    )

else:
    purchase_price = st.slider(
        "Vehicle purchase price",
        min_value=150000.0,
        max_value=2000000.0,
        step=100.0,
    )

# Check whether the purchase price exceeds the budget
if replacement_budget > 0 and purchase_price > replacement_budget:
    st.warning("This vehicle exceeds your stated replacement budget.")

down_payment = st.slider(
    "Down payment",
    min_value=0.0,
    max_value=purchase_price,
    value=purchase_price * 0.12,
    step=10.0,
)

interest = st.slider(
    "APR (Annual interest rate)",
    min_value=0.0,
    max_value=20.0,
    value=8.0,
    step=0.1,
)

# Calculate monthly payments
loan_amount = purchase_price - down_payment
monthly_interest = interest / 1200

if monthly_interest == 0:
    monthly_payment = loan_amount / loan_length
else:
    monthly_payment = loan_amount * monthly_interest / (
        1 - (1 + monthly_interest) ** (-loan_length)
    )

total_loan_payments = monthly_payment * loan_length
total_interest = total_loan_payments - loan_amount
total_cost = total_loan_payments + down_payment

monthly_payment = math.ceil(monthly_payment * 100) / 100
total_interest = math.ceil(total_interest * 100) / 100
total_cost = math.ceil(total_cost * 100) / 100

st.subheader("Here are your results!")

st.write(f"Your monthly payment is ${monthly_payment:,.2f}")
st.write(f"Your total loan payments are ${total_loan_payments:,.2f}")
st.write(f"Your total interest is ${total_interest:,.2f}")
st.write(f"Your total purchase cost is ${total_cost:,.2f}")


# AI Toyota Advisor
st.subheader("AI Toyota Advisor")

if st.button("Analyze My Toyota with AI", disabled=not car.strip()):
    prompt = f"""
    You are an AI Toyota vehicle and financial advisor for TFS
    (Toyota Financial Services).

    Analyze this customer's situation:

    VEHICLE DETAILS:
    Model: {manufacture_yr} {car}
    Mileage: {mileage}
    Driving style: {style}
    Maintenance: {prev_maintenance}
    Tire tread: {tire_tread}
    Overall condition: {vehicle_condition}
    Mechanical issues: {mechanical_issues}
    Warning lights: {warning_lights}
    Accident history: {accident_history}
    Annual mileage: {annual_mileage}
    Ownership: {ownership}
    Repair estimate: {repair_cost if repair_estimate == "Yes" else "Unknown"}

    REPLACEMENT FINANCING:
    Replacement budget: {f"${replacement_budget:,}" if replacement_budget > 0 else "Not provided"}
    Purchase price: ${purchase_price:,.2f}
    Down payment: ${down_payment:,.2f}
    APR: {interest}%
    Loan term: {loan_length} months
    Monthly payment: ${monthly_payment:,.2f}
    Total interest: ${total_interest:,.2f}

    TASK:
    Recommend whether the customer should KEEP, REPAIR,
    or CONSIDER REPLACING their vehicle.

    Explain:
    1. How driving style, mileage, and maintenance affect mechanical longevity.
    2. Any mechanical and safety concerns.
    3. Possible financial advantages and disadvantages.
    4. Brief overview of why you chose your recommendation.
    5. Practical next steps based on the supplied information.

    Use the supplied information. Do not invent exact repair costs or resale values.
    Identify missing data. Keep the answer under 250 words.

    Rules to follow before making assumptions:
    1. If current used-vehicle prices are unavailable, state that clearly
       instead of claiming to have checked comparable vehicles.
    2. Do not automatically recommend replacement due to mileage, driving habits,
       or warning lights. Explain urgent safety concerns separately.
    3. Consider confirmed mechanical severity, repair costs, maintenance,
       driving habits, and financial trade-offs.
    4. First recommend KEEP, REPAIR, or CONSIDER REPLACING. If appropriate,
       discuss trade-ins or selling, new versus used, and financing, leasing,
       or paying cash when enough information is available.
    """

    with st.spinner("Gemini is analyzing your Toyota..."):
        try:
            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )

            st.success("Your Toyota analysis is ready!")
            st.markdown(response.text or "No response returned.")

        except Exception as e:
            st.error(f"Gemini error: {e}")
