
import streamlit as st
import re

st.set_page_config(
    page_title="Secure Registration",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 User Registration Application")

email = st.text_input("Email Address")

password = st.text_input(
    "Password", type="password"
)

confirm = st.text_input(
    "Confirm Password", type="password"
)

common_passwords = [
    "password123",
    "admin123",
    "password@123",
    "qwerty123",
    "welcome123",
    "12345678"
]

# Password validation rules
rules = {
    "Minimum 8 characters": len(password) >= 8,
    "Maximum 128 characters": len(password) <= 128,
    "Uppercase letter": bool(re.search(r"[A-Z]", password)),
    "Lowercase letter": bool(re.search(r"[a-z]", password)),
    "Numeric digit": bool(re.search(r"[0-9]", password)),
    "Special character": bool(re.search(r"[^A-Za-z0-9\s]", password)),
    "No whitespace": not bool(re.search(r"\s", password)),
    "Not a common password": password.lower() not in common_passwords,
    "No repeated characters (3 or more)": not bool(
        re.search(r"(.)\1{2,}", password)
    )
}

username = email.split("@")[0].lower()

rules["Does not contain email username"] = (
    not username or username not in password.lower()
)

# Display password policy compliance
st.subheader("Password Requirements")

score = sum(rules.values())

if password:
    st.progress(score / len(rules))

    st.write(f"Requirements satisfied: {score}/{len(rules)}")

    for rule, passed in rules.items():
        if passed:
            st.write(f"✅ {rule}")
        else:
            st.write(f"❌ {rule}")

# Validate credentials
if st.button("Validate Credentials", type="primary"):

    errors = []

    if not re.fullmatch(
        r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", email
    ):
        errors.append("Invalid email address.")

    for rule, passed in rules.items():
        if not passed:
            errors.append(rule)

    if password != confirm:
        errors.append("Passwords do not match.")

    if errors:
        st.error("Validation Failed!")

        for error in errors:
            st.write(f"❌ {error}")

    else:
        st.success("Validation Successful!")
        st.balloons()
