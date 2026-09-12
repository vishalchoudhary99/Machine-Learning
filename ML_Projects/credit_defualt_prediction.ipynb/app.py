import streamlit as st
import numpy as np
import pickle 

# import the model 
model = pickle.load(open('D:\scikit-learn.py\ml_projects.ipynb\credit_defualt_prediction.ipynb\model.pkl','rb'))
with open('D:\scikit-learn.py\ml_projects.ipynb\credit_defualt_prediction.ipynb\optimal_threshold', 'rb') as f:
    optimal_threshold = pickle.load(f)

st.title('Credit Default Prediction')

# Credit Limit
Limit_Bal = st.number_input('Credit Card Balance (₹)', min_value = 10000, max_value = 3000000, step = 5000)

# Gender 
Gender = st.selectbox('Gender', ['Male','Female'])
if Gender == 'Male':
    Gender = 1
else:
    Gender = 0

# Education
Education = st.selectbox('Education', ['Graduate School','University','High School','Others'])
if Education == 'Others':
    Education = 0
elif Education == 'Graduate School':
    Education = 1
elif Education == 'University':
    Education = 2
else:
    Education = 3

# Marital Status
Marital_Status = st.selectbox('Marital Status',['Married','Single','Others'])
if Marital_Status == 'Married':
    Marital_Status = 1
elif Marital_Status == 'Single':
    Marital_Status = 2
else:
    Marital_Status = 0

# Age
Age = st.number_input('Age',min_value = 18, max_value = 100, step = 1)

# April_Delay
Apr_Delay = st.selectbox('April Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if Apr_Delay == 'No Bill Generated':
    Apr_Delay = -2
elif Apr_Delay == 'Paid On Time':
    Apr_Delay = -1
elif Apr_Delay == 'Late But Not Overdue':
    Apr_Delay = 0
elif Apr_Delay == 'One Month':
    Apr_Delay = 1
elif Apr_Delay == 'Two Month':
    Apr_Delay = 2
elif Apr_Delay == 'Three Month':
    Apr_Delay = 3
elif Apr_Delay == 'Four Month':
    Apr_Delay = 4
elif Apr_Delay == 'Five Month':
    Apr_Delay = 5
elif Apr_Delay == 'Six Month':
    Apr_Delay = 6
elif Apr_Delay == 'Seven Month':
    Apr_Delay = 7
else:
    Apr_Delay = 8

# May_Delay
May_Delay = st.selectbox('May Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if May_Delay == 'No Bill Generated':
    May_Delay = -2
elif May_Delay == 'Paid On Time':
    May_Delay = -1
elif May_Delay == 'Late But Not Overdue':
    May_Delay = 0
elif May_Delay == 'One Month':
    May_Delay = 1
elif May_Delay == 'Two Month':
    May_Delay = 2
elif May_Delay == 'Three Month':
    May_Delay = 3
elif May_Delay == 'Four Month':
    May_Delay = 4
elif May_Delay == 'Five Month':
    May_Delay = 5
elif May_Delay == 'Six Month':
    May_Delay = 6
elif May_Delay == 'Seven Month':
    May_Delay = 7
else:
    May_Delay = 8

# June_Delay
Jun_Delay = st.selectbox('June Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if Jun_Delay == 'No Bill Generated':
    Jun_Delay = -2
elif Jun_Delay == 'Paid On Time':
    Jun_Delay = -1
elif Jun_Delay == 'Late But Not Overdue':
    Jun_Delay = 0
elif Jun_Delay == 'One Month':
    Jun_Delay = 1
elif Jun_Delay == 'Two Month':
    Jun_Delay = 2
elif Jun_Delay == 'Three Month':
    Jun_Delay = 3
elif Jun_Delay == 'Four Month':
    Jun_Delay = 4
elif Jun_Delay == 'Five Month':
    Jun_Delay = 5
elif Jun_Delay == 'Six Month':
    Jun_Delay = 6
elif Jun_Delay == 'Seven Month':
    Jun_Delay = 7
else:
    Jun_Delay = 8


# July_Delay
Jul_Delay = st.selectbox('July Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if Jul_Delay == 'No Bill Generated':
    Jul_Delay = -2
elif Jul_Delay == 'Paid On Time':
    Jul_Delay = -1
elif Jul_Delay == 'Late But Not Overdue':
    Jul_Delay = 0
elif Jul_Delay == 'One Month':
    Jul_Delay = 1
elif Jul_Delay == 'Two Month':
    Jul_Delay = 2
elif Jul_Delay == 'Three Month':
    Jul_Delay = 3
elif Jul_Delay == 'Four Month':
    Jul_Delay = 4
elif Jul_Delay == 'Five Month':
    Jul_Delay = 5
elif Jul_Delay == 'Six Month':
    Jul_Delay = 6
elif Jul_Delay == 'Seven Month':
    Jul_Delay = 7
else:
    Jul_Delay = 8

# August Delay
Aug_Delay = st.selectbox('August Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if Aug_Delay == 'No Bill Generated':
    Aug_Delay = -2
elif Aug_Delay == 'Paid On Time':
    Aug_Delay = -1
elif Aug_Delay == 'Late But Not Overdue':
    Aug_Delay = 0
elif Aug_Delay == 'One Month':
    Aug_Delay = 1
elif Aug_Delay == 'Two Month':
    Aug_Delay = 2
elif Aug_Delay == 'Three Month':
    Aug_Delay = 3
elif Aug_Delay == 'Four Month':
    Aug_Delay = 4
elif Aug_Delay == 'Five Month':
    Aug_Delay = 5
elif Aug_Delay == 'Six Month':
    Aug_Delay = 6
elif Aug_Delay == 'Seven Month':
    Aug_Delay = 7
else:
    Aug_Delay = 8

# Sep_Delay
Sep_Delay = st.selectbox('Sepetember Delay',['No Bill Generated','Paid On Time','Late But Not Overdue','One Month','Two Month','Three Month','Four Month','Five Month','Six Month','Seven Month','Eight Month'])
if Sep_Delay == 'No Bill Generated':
    Sep_Delay = -2
elif Sep_Delay == 'Paid On Time':
    Sep_Delay = -1
elif Sep_Delay == 'Late But Not Overdue':
    Sep_Delay = 0
elif Sep_Delay == 'One Month':
    Sep_Delay = 1
elif Sep_Delay == 'Two Month':
    Sep_Delay = 2
elif Sep_Delay == 'Three Month':
    Sep_Delay = 3
elif Sep_Delay == 'Four Month':
    Sep_Delay = 4
elif Sep_Delay == 'Five Month':
    Sep_Delay = 5
elif Sep_Delay == 'Six Month':
    Sep_Delay = 6
elif Sep_Delay == 'Seven Month':
    Sep_Delay = 7
else:
    Sep_Delay = 8

# Bill_Gen_Apr
Bill_Gen_Apr = st.number_input('Bill Generated in April',min_value = 0, max_value = 3000000, step = 1000)

# Bill_Gen_May
Bill_Gen_May = st.number_input('Bill Generated in May',min_value = 0, max_value = 3000000, step = 1000)

# Bill_Gen_Jun
Bill_Gen_Jun = st.number_input('Bill Generated in June',min_value = 0, max_value = 3000000, step = 1000)

# Bill_Gen_Jul
Bill_Gen_Jul = st.number_input('Bill Generated in July',min_value = 0, max_value = 3000000, step = 1000)

# Bill_Gen_Aug
Bill_Gen_Aug = st.number_input('Bill Generated in August',min_value = 0, max_value = 3000000, step = 1000)

# Bill_Gen_Sep
Bill_Gen_Sep = st.number_input('Bill Generated in September',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_Apr
Amt_Paid_Apr = st.number_input('Amount Paid in April',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_May
Amt_Paid_May = st.number_input('Amount Paid in May',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_Jun
Amt_Paid_Jun = st.number_input('Amount Paid in June',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_Jul
Amt_Paid_Jul = st.number_input('Amount Paid in July',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_Aug
Amt_Paid_Aug = st.number_input('Amount Paid in August',min_value = 0, max_value = 3000000, step = 1000)

# Amt_Paid_Sep
Amt_Paid_Sep = st.number_input('Amount Paid in September',min_value = 0, max_value = 3000000, step = 1000)

# Negative_Bill_Count
Negative_Bill_Count = int(Bill_Gen_Apr < 0) + int(Bill_Gen_Aug < 0) + int(Bill_Gen_Jun) + int(Bill_Gen_Jul) + int(Bill_Gen_Aug) + int(Bill_Gen_Sep)

# Total_Bill
Total_Bill = Bill_Gen_Sep + Bill_Gen_Aug + Bill_Gen_Jul + Bill_Gen_Jun + Bill_Gen_May + Bill_Gen_Apr

# Total_Pay
Total_Pay = Amt_Paid_Apr + Amt_Paid_May + Amt_Paid_Jun + Amt_Paid_Jul + Amt_Paid_Aug + Amt_Paid_Sep

# Avg_Bill 
Avg_Bill = Total_Bill/6

# Avg_Pay
Avg_Pay = Total_Pay/6

# Payment_Bill_Ratio 
Payment_Bill_Ratio = round(Avg_Pay / Avg_Bill, 2) if Avg_Bill > 0 else 0

# Credit_Utilization
Credit_Utilization = round(Avg_Bill / Limit_Bal, 2)

# Max_Delay
Max_Delay =  max([Apr_Delay, May_Delay, Jun_Delay, Jul_Delay, Aug_Delay, Sep_Delay])

# Avg_Delay 
arr = np.array([Apr_Delay, May_Delay, Jun_Delay, Jul_Delay, Aug_Delay, Sep_Delay])
count = np.where(arr>0, 1,0).sum()
Avg_Delay = round((np.where(arr>0, arr, 0).sum()/count),2) if count > 0 else 0

# Delay_Count
Delay_Count = int(count)

# On_time_count 
On_time_count = 6 - count

# No_Bill_Count
No_Bill_Count = int(np.where(arr == -2, 1,0).sum())

# No_Overdue_Count
No_Overdue_Count = int(np.where(arr == 0, 1,0).sum())

# Maximum_Bill 
Maximum_Bill = max([Bill_Gen_Apr, Bill_Gen_May, Bill_Gen_Jun, Bill_Gen_Jul, Bill_Gen_Aug, Bill_Gen_Sep])

query = np.array([Limit_Bal, Gender, Education, Marital_Status, Age, Sep_Delay, Aug_Delay, Jul_Delay, Jun_Delay, May_Delay, Apr_Delay, Bill_Gen_Sep,
                  Bill_Gen_Aug, Bill_Gen_Jul, Bill_Gen_Jun, Bill_Gen_May, Bill_Gen_Apr, Amt_Paid_Sep, Amt_Paid_Aug, Amt_Paid_Jul, Amt_Paid_Jun, Amt_Paid_May,
                  Amt_Paid_Apr, Negative_Bill_Count, Total_Bill, Total_Pay, Avg_Bill, Avg_Pay, Payment_Bill_Ratio, Credit_Utilization, Max_Delay,
                  Avg_Delay, Delay_Count, On_time_count, No_Bill_Count, No_Overdue_Count, Maximum_Bill]).reshape(1,37)

if st.button('Predict Default'):
    pred_prob = ((model.predict_proba(query))[0,1])
    prediction = int((model.predict_proba(query))[0,1] >= optimal_threshold)

    def risk(pred_prob):
        if pred_prob < 0.2:
            return '🟢 Low Risk'
        elif pred_prob < 0.5 and pred_prob >= 0.2:
            return '🟡 Medium Risk'
        elif pred_prob >= 0.5:
            return '🔴 High Risk'

    if prediction == 0:
        st.header(f'Prediction')
        st.success('🟢 Customer is NOT likely to default.')
        st.subheader(f'Probability of Default')
        st.write(f'{model.predict_proba(query)[0,1] * 100:.2f} %')
        st.subheader('Risk Level')
        st.warning(risk(pred_prob))
        st.subheader('Explanation')
        st.write('''The customer has a relatively low estimated probability
                    of default based on the entered financial and repayment
                    history.''')
    else:
        st.header(f'Prediction')
        st.success('🔴 Customer is likely to default.')
        st.subheader(f'Probability of Default')
        st.write(f'{model.predict_proba(query)[0,1] * 100:.2f} %')
        st.subheader(f'Risk Level')
        st.warning(f'{risk(pred_prob)}')
        st.subheader('Explanation')
        st.write(''' The customer has a high estimated probability of default.
                     Additional financial assessment is recommended before
                     granting new credit.''')

    
    

