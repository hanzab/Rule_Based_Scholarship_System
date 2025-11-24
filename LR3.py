import streamlit as st
import operator

st.title("🎓 Scholarship Advisory Rule-Based System")
st.write("This system evaluates applicants based on predefined scholarship rules.")

# -----------------------------------------------------------
# RULE BASE — EXACT JSON (as required)
# -----------------------------------------------------------
rules = [
    {
        "name": "Top merit candidate", "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship", "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review", "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible", "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record", "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

# -----------------------------------------------------------
# OPERATORS
# -----------------------------------------------------------
ops = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq
}

# -----------------------------------------------------------
# RULE EVALUATION FUNCTION
# -----------------------------------------------------------
def evaluate_applicant(applicant):
    sorted_rules = sorted(rules, key=lambda r: r["priority"], reverse=True)

    for rule in sorted_rules:
        conditions_met = True

        for field, op, value in rule["conditions"]:
            if not ops[op](applicant[field], value):
                conditions_met = False
                break

        if conditions_met:
            return rule["name"], rule["action"]["decision"], rule["action"]["reason"]

    return None, "NO_DECISION", "No rule was triggered."


# -----------------------------------------------------------
# STREAMLIT INPUT FORM (only fields actually used in rules)
# -----------------------------------------------------------
st.subheader("Enter Applicant Information")

cgpa = st.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, step=0.01)
income = st.number_input("Monthly Family Income (RM)", min_value=0, step=50)
co = st.number_input("Co-curricular Score (0–100)", min_value=0, max_value=100)
discipline = st.number_input("Number of Disciplinary Actions", min_value=0, max_value=10)

submit = st.button("Evaluate Applicant")

# -----------------------------------------------------------
# DECISION OUTPUT + POPUP MESSAGE
# -----------------------------------------------------------
if submit:
    applicant = {
        "cgpa": cgpa,
        "family_income": income,
        "co_curricular_score": co,
        "disciplinary_actions": discipline
    }
    
    rule_name, decision, reason = evaluate_applicant(applicant)

    st.subheader("🎯 Evaluation Result")

    if decision == "AWARD_FULL":
        st.success(f"🏅 FULL SCHOLARSHIP AWARDED\n\n*Rule:* {rule_name}\n\n*Reason:* {reason}")
    elif decision == "AWARD_PARTIAL":
        st.info(f"🎓 PARTIAL SCHOLARSHIP AWARDED\n\n*Rule:* {rule_name}\n\n*Reason:* {reason}")
    elif decision == "REVIEW":
        st.warning(f"🧐 REVIEW REQUIRED\n\n*Rule:* {rule_name}\n\n*Reason:* {reason}")
    elif decision == "REJECT":
        st.error(f"❌ APPLICATION REJECTED\n\n*Rule:* {rule_name}\n\n*Reason:* {reason}")
    else:
        st.write("No rule matched the applicant's profile.")