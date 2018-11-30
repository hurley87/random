import pandas as pd
import numpy as np
from pipedrive import Pipedrive
from datetime import datetime

# collect all funnel data in one dict
metrics = {}

# load survey gizmo data into dataframe
sg_df = pd.read_csv('sg.csv')

# load pipedrive data into dataframe`
# store all deals from Pipedrive into dataframe (deal_df)
pipedrive = Pipedrive('48357285ee02f8a9dabfbde9adacc3bd7a9ec67f')

more_deals = True
deal_lists = []
new_start = 0

while more_deals:
    print(new_start)
    pipedrive_deals = pipedrive.deals({'status':'all_not_deleted', 'limit': 500, 'start': new_start}, method='GET')
    new_deals = pipedrive_deals['data']
    deal_dataframe = pd.DataFrame(new_deals)
    deal_lists.append(deal_dataframe)
    print(len(deal_lists))
    more_deals = pipedrive_deals['additional_data']['pagination']['more_items_in_collection']
    new_start += 500

deal_df = pd.concat(deal_lists)

print(len(deal_df.index))


# TODO: Get cost data from Facebook ads. Use API to grab cost per campaign - we will be doing that going forward
def cost_by_source(code):
    return {
        'E': 500,
        'REF': 250,
        'EVENT': 500,
        'CA': 800,
        'FB': cost_by_FB(DAY),
        'P': 500
    }.get(code, 100)

# manually  
def cost_by_FB(day):
    return {
    'june8': 771.11,
    'june9': 805.89,
    'june11': 1554.22,
    'june12': 1340.78,
    'june14': 279.43,
    'april20': 289.58,
    'april21': 248.15,
    'april24': 197.43,
    'april25': 395.11,
    'april26': 255.51,
    'april27': 595.35
}.get(day, 100)

# I've identified key questions that we ask all users during the discovery process. 
# Question are asked to the user in this order
key_questions = [
 'retirementAge',
 'currentAge',
 'firstName',
 'email',
 'phone',
 'hasSpouse',
 'annualIncome',
 'renting',
 'hasChildren',
 'debt',
 'sex',
 'smoke',
 'province']

 # we record how long it takes a user to answer each question.
key_questions_time = [
 'retirementAgeTime',
 'currentAgeTime',
 'firstNameTime',
 'emailTime',
 'phoneTime',
 'spouseTime',
 'annualIncomeTime',
 'rentTime',
 'kidsTime',
 'debtTime',
 'sexTime',
 'smokingTime',
 'provinceTime']

# conversion rate of the entire form
# What percentage of people who started the form finished it?
def form_conversion(leads_datatable):
    first_question_count = leads_datatable[key_questions[0]].count()
    last_question_count = leads_datatable[key_questions[len(key_questions) - 1]].count()
    form_conversion = last_question_count / first_question_count
    return str(round(form_conversion * 100,2)) + '%'

metrics['form_conversion'] = form_conversion(sg_df)

# look at key question stats
# how many people answered the question
# the question conversion rate
# average time spent on that question
metrics['onboarding'] = {}
metrics['questions'] = {}
index = 1
questions_length = len(key_questions)
for question in key_questions:
    current_question_count = sg_df[question].count()
    previous_index = index - 1
    previous_question = key_questions[previous_index]
    previous_question_count = sg_df[previous_question].count()
    conversion = (previous_question_count - current_question_count) / previous_question_count
    average_time_spent = sg_df[key_questions_time[index]].mean()
    metrics['questions'][question] = {
    	'count': current_question_count,
    	'conversion': round((1 - conversion) * 100, 2),
    	'avg_time': round(average_time_spent, 2)
    }
    if index < questions_length - 2:
        index += 1

def clicks_by(ref_code):
    return sg_df[sg_df.ref == ref_code].ref.count()

# How many emails did we get from each REF code?
def email_count(ref_code):
    return sg_df[sg_df.ref == ref_code].email.count()

# How many numbers did we get from each REF code?
def phone_count(ref_code):
    return sg_df[sg_df.ref == ref_code].phone.count()

# How many plans did we get from each REF code?
def plan_count(ref_code):
    return sg_df[sg_df.ref == ref_code].province.count()

def email_conversion(ref_code):
    clicks = clicks_by(ref_code)
    count = email_count(ref_code)
    return round(count/clicks*100, 2)

def phone_conversion(ref_code):
    clicks = clicks_by(ref_code)
    count = phone_count(ref_code)
    return round(count/clicks*100, 2)

def plan_conversion(ref_code):
    clicks = clicks_by(ref_code)
    count = plan_count(ref_code)
    return round(count/clicks*100, 2)

# Cost of a marketing qualified lead (MQL)
def email_cost(ref_code):
    count = email_count(ref_code)
    code = ref_code.split('-')[0]
    cost = cost_by_source(code)
    return round(cost / (count + 1), 2)

# Cost of a sales qualified lead (SQL)
def phone_cost(ref_code):  
    count = phone_count(ref_code)
    code = ref_code.split('-')[0]
    cost = cost_by_source(code)
    return round(cost / (count + 1), 2)

# Cost of a plan qualified lead (PQL)
# TODO: get plan count from production data or pipedrive
def plan_cost(ref_code):
    count = plan_count(ref_code)
    code = ref_code.split('-')[0]
    cost = cost_by_source(code)
    return round(cost / (count + 1), 2)

# What is the conversion rate of discovery flow for each ref code?
ref_codes = list(set(sg_df[sg_df.ref.notnull()]['ref'].tolist()))

for ref in ref_codes:
    datatable = sg_df[sg_df.ref == ref]
    if ref not in metrics.keys()
    	metrics[ref] = {}
    	metrics[ref]['f']`


print(metrics)

















