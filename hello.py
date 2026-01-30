import streamlit as st
import pandas as pd
import os
import numpy as np
from functools import reduce
from datetime import datetime
from io import BytesIO
from xlsxwriter import Workbook


st.set_page_config(page_title="SGI Reporting Dashboard", layout="centered")


# COMPANY METADATA
COMPANY_CONFIG = {
    "MorningStar": {
        "website": "https://idm.morningstar.com/#/status/statusList",
        "login": "bryce@summitglobalinvestments.com",
        "password": "options1"
    },
    "Evestment": {
        "website": "https://app.evestment.com/next/login.aspx",
        "login": "charden@sgilv.com",
        "password": "Silvx$3B"
    },
    "PSN": {
        "website": "https://psn.fi.informais.com/login.asp",
        "login": "charden@sgilv.com",
        "password": "Silvx$3B"
    },
    "Callan": {
        "website": "https://app.callan.com/managers/13700/products",
        "login": "charden@sgilv.com",
        "password": "Silvx$3B"
    },
    "Mercer": {
        "website": "https://www.mercergimd.com/secure/login.asp?RFR=",
        "login": "suttonb",
        "password": "Allison@1995"
    },
    "Wilshire": {
        "website": "https://compassportal.wilshire.com/Account/Login.aspx?ReturnUrl=%2fDefault.aspx",
        "login": "SummitGlobalInv",
        "password": "Silvx$3B"
    },
    "Leia": {
        "website": "https://www.leia-manager-portal.com/portal",
        "login": "SGI",
        "password": "Silvx$3B"
    },
    "DeMarche": {
        "website": "https://client.demarche.com/12_dataRetrieval/login.asp",
        "login": "ccampbell@summitglobalinvestments.com",
        "password": "masdf235@#$"
    }
}

# SESSION STATE INIT
if "page" not in st.session_state:
    st.session_state.page = "home"

if "company" not in st.session_state:
    st.session_state.company = None

def navigate(page):
    st.session_state.page = page
    st.rerun()

# HOME PAGE
if st.session_state.page == "home":
    st.title("SGI Reporting Dashboard")

    company = st.selectbox(
        "Select a Company",
        list(COMPANY_CONFIG.keys()),
        key="company_select"
    )

    if st.button("Submit", key="home_submit"):
        st.session_state.company = company
        navigate("company")

# COMPANY LANDING PAGE
elif st.session_state.page == "company":
    company = st.session_state.company
    meta = COMPANY_CONFIG[company]

    st.title(company)
    st.markdown(f"🔗 **Website:** [{meta['website']}]({meta['website']})")
    st.markdown(f"👤 **Login:** `{meta['login']}`")
    st.markdown(f"🔐 **Password:** `{meta['password']}`")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Performance"):
            navigate("performance")
    with col2:
        if st.button("Holdings"):
            navigate("holdings")
    with col3:
        if st.button("AUM"):
            navigate("aum")

    if st.button("⬅ Back"):
        navigate("home")

# PERFORMANCE PAGE
elif st.session_state.page == "performance":
    st.title("Performance")
    st.subheader("Please select the last day of the month for performance of that month!")

    selected_date = st.date_input("Select a date:")
    show_performance = st.button("Submit")

    if show_performance:
        #extracting data from excel and merging into single performance dataframe
        #LC (Gross)
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "GIPS Performance - Master.xlsx")
        LC_g = pd.read_excel(file_path, sheet_name='LC (Gross)')
        LC_g = LC_g.iloc[:, [0,3]]
        LC_g = LC_g.dropna().round(2)

        LC_g.iloc[1:, 0] = pd.to_datetime(LC_g.iloc[1:, 0])
        LC_g.columns = LC_g.iloc[0]  # Set the first row as the header
        LC_g = LC_g.iloc[1:].reset_index(drop=True)
        LC_g = LC_g.rename(columns={'Gross Return': 'Large Cap Gross'})


        #LC (Net)
        LC_n = pd.read_excel(file_path, sheet_name='LC (Net)')
        LC_n = LC_n.iloc[:, [0,3]]
        LC_n = LC_n.dropna().round(2)

        LC_n.iloc[1:, 0] = pd.to_datetime(LC_n.iloc[1:, 0])
        LC_n.columns = LC_n.iloc[0]  # Set the first row as the header
        LC_n = LC_n.iloc[1:].reset_index(drop=True)
        LC_n = LC_n.rename(columns={'Net Return': 'Large Cap Net'})

        #Global (Gross)
        global_g = pd.read_excel(file_path, sheet_name='Global (Gross)')
        global_g = global_g.iloc[:, [0,3]]
        global_g = global_g.dropna().round(2)

        global_g.iloc[1:, 0] = pd.to_datetime(global_g.iloc[1:, 0])
        global_g.columns = global_g.iloc[0]  # Set the first row as the header
        global_g = global_g.iloc[1:].reset_index(drop=True)
        global_g = global_g.rename(columns={'Gross Return': 'Global Gross'})

        #Global (Net)
        global_n = pd.read_excel(file_path, sheet_name='Global (Net)')
        global_n = global_n.iloc[:, [0,3]]
        global_n = global_n.dropna().round(2)

        global_n.iloc[1:, 0] = pd.to_datetime(global_n.iloc[1:, 0])
        global_n.columns = global_n.iloc[0]  # Set the first row as the header
        global_n = global_n.iloc[1:].reset_index(drop=True)
        global_n = global_n.rename(columns={'Net Return': 'Global Net'})


        #BOGIX (Gross)
        bogix_g = pd.read_excel(file_path, sheet_name='BOGIX (Gross)')
        bogix_g = bogix_g.iloc[:, [0,3]]
        bogix_g = bogix_g.dropna().round(2)

        bogix_g.iloc[1:, 0] = pd.to_datetime(bogix_g.iloc[1:, 0])
        bogix_g.columns = bogix_g.iloc[0]  # Set the first row as the header
        bogix_g = bogix_g.iloc[1:].reset_index(drop=True)
        bogix_g = bogix_g.rename(columns={'Gross Return': 'Small Cap Core Gross'})

        #BOGIX (Net)
        bogix_n = pd.read_excel(file_path, sheet_name='BOGIX (Net)')

        bogix_n = bogix_n.iloc[:, [0,3]]
        bogix_n = bogix_n.dropna().round(2)

        bogix_n.iloc[1:, 0] = pd.to_datetime(bogix_n.iloc[1:, 0])
        bogix_n.columns = bogix_n.iloc[0]  # Set the first row as the header
        bogix_n = bogix_n.iloc[1:].reset_index(drop=True)
        bogix_n = bogix_n.rename(columns={'Gross Return': 'Small Cap Core Net'})
        
        #merging into single dataframe
        data_frames = [LC_g, LC_n, global_g, global_n, bogix_g, bogix_n]
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                                    how='outer'), data_frames).fillna(0)

        df_merged['Date'] = pd.to_datetime(df_merged['Date'], errors='coerce')
        df_merged['Date'] = df_merged['Date'].dt.date
        df_merged = df_merged.round(2)
        #extracting row for of values for specified date
        value = pd.to_datetime(selected_date)
        value = value.date()
        filtered_row = df_merged[df_merged['Date'] == value]
        filtered_row = filtered_row.reset_index(drop=True)
        filtered_row = filtered_row.to_csv()
        data_list = [row.split(",") for row in filtered_row.splitlines()]

        #printing dataframe in streamlit
        st.success(f"Performance data for {selected_date} would be displayed here:")
        st.dataframe(data_list)

    if st.button("⬅ Back"):
        navigate("company")

# HOLDINGS PAGE 
elif st.session_state.page == "holdings":
    company = st.session_state.company
    st.title(f"{company} – Holdings")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if st.button("Submit"):
        if uploaded_file is None:
            st.warning("Please upload an Excel file.")
        else:
            if company == "MorningStar":
                st.success("Running MorningStar Holdings logic")
                df2 = pd.read_excel(uploaded_file, header=3)
                global_holdings = df2[df2['Account ID']=='19-8338'].reset_index(drop=True)
                largecap_holdings = df2[df2['Account ID']=='19-8337'].reset_index(drop=True)


                columns = [
                    "Identifier",
                    "Identifier Type",
                    "Ticker",
                    "Security Name",
                    "Security Type",
                    "# of Shares",
                    "Security Price",
                    "Weight (%)",
                    "Country",
                    "Market Value"
                ]

                # Create the empty DataFrame
                evestment_temp = pd.DataFrame(columns=columns)

                # Display the DataFrame

                column_mapping = {
                    'CUSIP Id': 'Identifier',
                    'Ticker Symbol': 'Ticker',
                    'Asset Long Name 1': 'Security Name',
                    'Shares/Par': '# of Shares',
                    'Current Price': 'Security Price',
                    'Market Value': 'Market Value'
                }

                df_renamed = global_holdings.rename(columns=column_mapping)
                df_renamed = df_renamed.drop(columns=['Account ID', 'As Of Date','Unnamed: 8'])
                df_renamed["Identifier Type"] = "CUSIP"
                df_renamed["Security Type"] = "common stock"
                df_renamed["Country"] = "United States"

                total_market_value1 = df_renamed["Market Value"].sum()
                df_renamed["Weight (%)"] = df_renamed["Market Value"]/total_market_value1*100
                df_renamed["Weight (%)"] = df_renamed["Weight (%)"].apply(lambda x: f"{x:.2f}%")
                df_renamed_1 = df_renamed[columns]

                df_renamed = largecap_holdings.rename(columns=column_mapping)
                df_renamed = df_renamed.drop(columns=['Account ID', 'As Of Date','Unnamed: 8'])
                df_renamed["Identifier Type"] = "CUSIP"
                df_renamed["Security Type"] = "common stock"
                df_renamed["Country"] = "United States"

                total_market_value2 = df_renamed["Market Value"].sum()
                df_renamed["Weight (%)"] = df_renamed["Market Value"]/total_market_value2*100
                df_renamed["Weight (%)"] = df_renamed["Weight (%)"].apply(lambda x: f"{x:.2f}%")
                df_renamed_2 = df_renamed[columns]

            elif company == "Evestment":
                st.success("Running Evestment Holdings logic")
                df2 = pd.read_excel(uploaded_file, header=3)
                global_holdings = df2[df2['Account ID']=='19-8338'].reset_index(drop=True)
                largecap_holdings = df2[df2['Account ID']=='19-8337'].reset_index(drop=True)


                columns = [
                    "Identifier",
                    "Identifier Type",
                    "Ticker",
                    "Security Name",
                    "Security Type",
                    "# of Shares",
                    "Security Price",
                    "Weight (%)",
                    "Country",
                    "Market Value"
                ]

                # Create the empty DataFrame
                evestment_temp = pd.DataFrame(columns=columns)

                # Display the DataFrame

                column_mapping = {
                    'CUSIP Id': 'Identifier',
                    'Ticker Symbol': 'Ticker',
                    'Asset Long Name 1': 'Security Name',
                    'Shares/Par': '# of Shares',
                    'Current Price': 'Security Price',
                    'Market Value': 'Market Value'
                }

                df_renamed = global_holdings.rename(columns=column_mapping)
                df_renamed = df_renamed.drop(columns=['Account ID', 'As Of Date','Unnamed: 8'])
                df_renamed["Identifier Type"] = "CUSIP"
                df_renamed["Security Type"] = "common stock"
                df_renamed["Country"] = "United States"

                total_market_value1 = df_renamed["Market Value"].sum()
                df_renamed["Weight (%)"] = df_renamed["Market Value"]/total_market_value1*100
                df_renamed["Weight (%)"] = df_renamed["Weight (%)"].apply(lambda x: f"{x:.2f}%")
                df_renamed_1 = df_renamed[columns]

                df_renamed = largecap_holdings.rename(columns=column_mapping)
                df_renamed = df_renamed.drop(columns=['Account ID', 'As Of Date','Unnamed: 8'])
                df_renamed["Identifier Type"] = "CUSIP"
                df_renamed["Security Type"] = "common stock"
                df_renamed["Country"] = "United States"

                total_market_value2 = df_renamed["Market Value"].sum()
                df_renamed["Weight (%)"] = df_renamed["Market Value"]/total_market_value2*100
                df_renamed["Weight (%)"] = df_renamed["Weight (%)"].apply(lambda x: f"{x:.2f}%")
                df_renamed_2 = df_renamed[columns]

            elif company == "PSN":
                st.success("Running PSN Holdings logic")

            elif company == "Callan":
                st.success("Running Callan Holdings logic")

            elif company == "Mercer":
                st.success("Running Mercer Holdings logic")

            elif company == "Wilshire":
                st.success("Running Wilshire Holdings logic")

            elif company == "Leia":
                st.success("Running Leia Holdings logic")

            elif company == "DeMarche":
                st.success("Running DeMarche Holdings logic")

            else:
                st.error("Unsupported company")
            
            def to_excel_download(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            global_xlsx = to_excel_download(df_renamed_1)
            largecap_xlsx = to_excel_download(df_renamed_2)
            #df_renamed.to_excel("output.xlsx", index=False)
            # Download buttons
            st.download_button(
                label="Download Global Holdings",
                data=global_xlsx,
                file_name="global_holdings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown(f"**Total Market Value (Global Holdings):** ${total_market_value1:,.2f}")

            st.download_button(
                label="Download Large Cap Holdings",
                data=largecap_xlsx,
                file_name="large_cap_holdings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown(f"**Total Market Value (Large Cap Holdings):** ${total_market_value2:,.2f}")

    if st.button("⬅ Back"):
        navigate("company")

# AUM PAGE 
elif st.session_state.page == "aum":
    company = st.session_state.company
    st.title(f"{company} – AUM")

    selected_date = st.date_input("Select a date")

    if st.button("Submit"):
        if company == "MorningStar":
            st.success("Running MorningStar AUM logic")

        elif company == "Evestment":
                st.success("Running Evestment AUM logic")
                current_dir = os.path.dirname(__file__)
                file_path = os.path.join(current_dir, "AUM.xlsx")
                df3 = pd.read_excel(file_path, sheet_name='Strategy&Account')
                file_path = os.path.join(current_dir, "Fund info.xlsx")
                df4 = pd.read_excel(file_path)
                df3['Date'] = pd.to_datetime(df3['Date'], errors='coerce')
                df3['Date'] = df3['Date'].dt.date

                value = selected_date
                value = pd.to_datetime(value)
                value = value.date()
                x = df3[df3['Date'] == value]

                funds = df4[df4['Product'].isin(['Large Cap','Global','Small Cap Core'])]
                fund_names =funds.iloc[:,0]
                x.loc[:,fund_names] = x.loc[:,fund_names].apply(lambda x: x / 1000000)

                #extracting account numbers from columns
                target_columns = fund_names

                columns = x.columns.tolist()
                selected_columns = []

                for col in target_columns:
                    try:
                        idx = columns.index(col)
                        selected_columns.append(col)
                        if idx + 1 < len(columns):
                            selected_columns.append(columns[idx + 1])
                    except ValueError:
                        print(f"Column '{col}' not found!")

                # Drop duplicates in case some columns are repeated
                selected_columns = list(dict.fromkeys(selected_columns))

                result_df = x[selected_columns]


                #formatting table to better structure
                fund_columns = fund_names
                account_columns = [col for col in result_df.columns if "Accts." in col]

                funds1 = []
                accounts = []

                for f_col, a_col in zip(fund_columns, account_columns):
                    funds1 += result_df[f_col].tolist()
                    accounts += result_df[a_col].tolist()

                df_long = pd.DataFrame({
                    'Name': fund_columns,
                    'Accounts': accounts,
                    'Assets in Millions':funds1
                })


                #merging tables
                merged_inner = funds.merge(df_long, on='Name')

                #formatting table
                merged_inner.insert(0, "Date", value)
                merged_inner["Client Domicile"] = 'United States'
                merged_inner["Defined Contribution"] = 'Yes'
                merged_inner = merged_inner.drop(['In Composite?','Strategy','Name'], axis=1)
                merged_inner = merged_inner.rename(columns={'Product': 'Product Name'})
                merged_inner['Date'] = pd.to_datetime(merged_inner['Date']).dt.strftime('%m/%d/%y')
                merged_inner['Tax Status'] = np.where(merged_inner['Tax Status'] == 'Y', 'Taxable', 'Tax-Exempt')
                merged_inner['Institutional'] = np.where(merged_inner['Institutional'] == 'Y', 'Yes', 'No')

                #sorting columns
                new_order = [
                    'Date',
                    'Product Name',
                    'Assets in Millions',
                    'Client Type',
                    'Vehicle Type',
                    'Institutional',
                    'Client Domicile',
                    'Tax Status',
                    'Defined Contribution',
                    'Accounts'
                ]
                merged_inner = merged_inner[new_order]

                def to_excel_download(df):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df.to_excel(writer, index=False)
                    return output.getvalue()

                new_AUM = to_excel_download(merged_inner)
                # Download buttons
                st.download_button(
                label="Download Global Holdings",
                data=new_AUM,
                file_name="new_AUM.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif company == "PSN":
            st.success("Running PSN AUM logic")

        elif company == "Callan":
            st.success("Running Callan AUM logic")

        elif company == "Mercer":
            st.success("Running Mercer AUM logic")

        elif company == "Wilshire":
            st.success("Running Wilshire AUM logic")

        elif company == "Leia":
            st.success("Running Leia AUM logic")

        elif company == "DeMarche":
            st.success("Running DeMarche AUM logic")

        else:
            st.error("Unsupported company")

    if st.button("⬅ Back"):
        navigate("company")
