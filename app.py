"""Intelligent Personal Finance Search and Ranking Engine
Main Streamlit application.
Run with:  streamlit run app.py
"""
import streamlit as st
import pandas as pd

from data_manager import DataManager, FIELDS
from search_engine import SearchEngine
from ranking_engine import rank_results
from text_processing import slice_records
import dashboard as db

# ---------------- Page setup ----------------
st.set_page_config(page_title="Finance Search Engine",
                   page_icon="💰", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f4f7fb; }
    .metric-card { background: white; padding: 18px; border-radius: 12px;
                   box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .algo-badge { background: #1a73e8; color: white; padding: 4px 12px;
                  border-radius: 20px; font-size: 14px; }
    div[data-testid="stMetric"] { background: white; padding: 15px;
                  border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# ---------------- Session state ----------------
if "dm" not in st.session_state:
    st.session_state.dm = DataManager()       # our data manager (Python list)
if "search_history" not in st.session_state:
    st.session_state.search_history = []      # search history list
if "last_results" not in st.session_state:
    st.session_state.last_results = None      # results ready for CSV export

dm = st.session_state.dm
engine = SearchEngine()

# ---------------- Sidebar ----------------
st.sidebar.title("💰 Finance Engine")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "➕ Add Record",
                                  "🔍 Search Records", "📜 Search History"])
st.sidebar.markdown("---")
st.sidebar.caption("Built with pure Python algorithms")

# =========================================================
# PAGE 1: DASHBOARD
# =========================================================
if page == "🏠 Dashboard":
    st.title("📊 Financial Records Dashboard")

    df = dm.to_dataframe()
    total, spent, avg = db.summary_metrics(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Transactions", total)
    c2.metric("Total Spent", f"₹{spent:,.2f}")
    c3.metric("Average Amount", f"₹{avg:,.2f}")

    if df.empty:
        st.info("No records yet. Go to 'Add Record' to add your first one!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spending by Category")
            st.bar_chart(db.category_chart(df))
        with col2:
            st.subheader("Payment Methods")
            st.pie_chart(db.payment_chart(df))

        st.subheader("All Records")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # CSV export of all records
        csv_all = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export All Records (CSV)", csv_all,
                           "all_records.csv", "text/csv")

# =========================================================
# PAGE 2: ADD RECORD
# =========================================================
elif page == "➕ Add Record":
    st.title("➕ Add a New Financial Record")
    st.caption("All fields are validated before saving.")

    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            desc = st.text_input("Description *", placeholder="Grocery Shopping")
            category = st.selectbox("Category *",
                ["Food", "Travel", "Bills", "Shopping", "Health",
                 "Entertainment", "Education", "Other"])
            merchant = st.text_input("Merchant", placeholder="Local Store")
        with c2:
            amount = st.text_input("Amount (₹) *", placeholder="2500")
            payment = st.selectbox("Payment Method",
                                   ["UPI", "Cash", "Card", "Net Banking"])
            date = st.date_input("Date")
        tid = st.text_input("Transaction ID (leave empty for auto ID)",
                            placeholder="TX101")
        submitted = st.form_submit_button("💾 Save Record")

    if submitted:
        tid_val = tid.strip() if tid.strip() else None
        record, error = dm.add_record(desc, category, merchant, amount,
                                      payment, str(date), tid_val)
        if error:
            st.error(f"⚠️ {error}")
        else:
            st.success(f"✅ Transaction successfully added: "
                       f"{record['transaction_id']} — {record['description']}")

    # Edit / Delete section
    st.markdown("---")
    st.subheader("✏️ Edit or 🗑️ Delete a Record")
    if not dm.records:
        st.info("No records to edit or delete yet.")
    else:
        ids = [r["transaction_id"] for r in dm.records]
        chosen = st.selectbox("Choose Transaction ID", ids)
        rec = dm.find_by_id(chosen)
        if rec:
            with st.form("edit_form"):
                new_desc = st.text_input("Description", value=rec["description"])
                new_amt = st.text_input("Amount (₹)", value=str(rec["amount"]))
                if st.form_submit_button("💾 Save Changes"):
                    _, err = dm.update_record(chosen, description=new_desc,
                                              amount=new_amt)
                    st.error(f"⚠️ {err}") if err else st.success("✅ Record updated!")
            if st.button("🗑️ Delete this record"):
                dm.delete_record(chosen)
                st.warning(f"Deleted {chosen}.")
                st.rerun()

# =========================================================
# PAGE 3: SEARCH
# =========================================================
elif page == "🔍 Search Records":
    st.title("🔍 Smart Search & Ranking")

    if not dm.records:
        st.info("Add some records first!")
    else:
        query = st.text_input("Search query", placeholder="e.g. Grocery or TX101")
        search_type = st.radio("Search algorithm",
            ["🔤 Text Search (Linear Search — partial match)",
             "🆔 Exact ID (Binary Search — needs sorted data)",
             "💵 Exact Amount (Binary Search — needs sorted data)"])
        rank_by = st.selectbox("Rank results by",
            ["No sorting", "Highest amount first", "Lowest amount first",
             "Alphabetical (Merchant A-Z)", "Category (A-Z)",
             "Recent transaction first"])
        show_n = st.slider("Show top N results", 1, 50, 10)

        if st.button("🔍 Search"):
            if not query.strip():
                st.warning("Please enter a search query.")
            else:
                # ----- run the chosen search -----
                if search_type.startswith("🔤"):
                    results, info = engine.smart_text_search(dm.records, query)
                elif search_type.startswith("🆔"):
                    results, info = engine.exact_id_search(dm.records, query)
                else:
                    try:
                        results, info = engine.amount_search(dm.records, float(query))
                    except ValueError:
                        results, info = [], None
                        st.error("⚠️ Amount search needs a number, e.g. 2500")

                if info:
                    # save to search history
                    st.session_state.search_history.append(info)

                    # show performance info
                    st.markdown(f"**Algorithm used:** <span class='algo-badge'>"
                                f"{info['algorithm']}</span>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Query", info["query"])
                    c2.metric("Matching Records", info["matches"])
                    c3.metric("Time", f"{info['time_ms']} ms")
                    st.caption(f"💡 {info['note']}")

                    if results:
                        # ----- ranking -----
                        if rank_by != "No sorting":
                            results, algo = rank_results(results, rank_by)
                            st.info(f"📶 Ranking: {algo}")
                            st.session_state.search_history[-1]["ranking"] = algo

                        # ----- slicing: show only top N -----
                        shown = slice_records(results, 0, show_n)
                        df = dm.to_dataframe(shown)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        st.session_state.last_results = df

                        csv_res = df.to_csv(index=False).encode("utf-8")
                        st.download_button("⬇️ Export Results (CSV)", csv_res,
                                           "search_results.csv", "text/csv")
                    else:
                        st.warning("No matching records found.")
                        st.session_state.last_results = None

# =========================================================
# PAGE 4: SEARCH HISTORY
# =========================================================
else:
    st.title("📜 Search History")
    history = st.session_state.search_history
    if not history:
        st.info("No searches yet.")
    else:
        history = history[::-1]              # newest first (slicing trick!)
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total searches: {len(history)}")