import pandas as pd
import numpy as np

class Rocs:
  
  def __init__(self):
    return
  
  def cheq_recon_transform(self, balance, file):
    df = pd.read_csv(file, skiprows = 3)
    final = pd.DataFrame() 	 #Read
    #Transform the date into desired format
    final['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    #final['Date'] = pd.to_datetime(df['Date Posted'], format ='%Y%m%d')
    final['Transaction Description'] = df.Description

    final['Withdrawals (Debit)'] = np.where(df['Transaction Type'] == 'DEBIT', abs(df[' Transaction Amount']), '')
    final['Deposits (Credit)'] = np.where( df['Transaction Type'] == 'CREDIT', abs(df[' Transaction Amount']), '')
    final['Description'] = ''

    #Calculate the balance
    transacs = list(df[' Transaction Amount'])
    out = []
    for amount in transacs:
      balance = round(balance + amount, 2)
      out.append(round(balance, 2))
    final['Balance'] = out

    print('chequeing account statement finishes')
    return final
  
  def sav_recon_transform(self, balance, file):
    df = pd.read_csv(file, skiprows = 3)
    final = pd.DataFrame() 	
    final['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    final['Transaction Description'] = df.Description

    final['Withdrawals (Debit)'] = np.where(df['Transaction Type'] == 'DEBIT', abs(df[' Transaction Amount']), '')
    final['Deposits (Credit)'] = np.where( df['Transaction Type'] == 'CREDIT', abs(df[' Transaction Amount']), '')
    final['Description'] = ''

    transacs = list(df[' Transaction Amount'])
    out = []
    for amount in transacs:
      balance = round(balance + amount, 2)
      out.append(round(balance, 2))
    final['Balance'] = out
    
    print('saving account statement finishes')
    return final
  
  def Income_chequeing_helper(self, cheque_file):
    
    cheq = pd.DataFrame()
    df = pd.read_csv(cheque_file, skiprows = 3)
    cheq['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    cheq['No.'] = ''
    cheq['Currency'] = 'CAD'
    #Avoid Internal Transaction and E-Transfer Fee
    avoid = ((-df.Description.str.contains('0389#8815')) & (-df.Description.str.contains('INTERAC E-TRANSFER FEE')))
    
    cheq['Receipt Amount'] = np.where(
            #Condition:
              (df['Transaction Type'] == 'CREDIT') & avoid,
              df[' Transaction Amount'],
              np.nan
          )
    cheq['Exchange-CAD'] = ''
    #Deals with typical e-transfer received

    def Income_replace_paid_from(des):
      if des.find('[CW]INTERAC ETRNSFR AD RECVD') != -1:
          return des.replace('[CW]INTERAC ETRNSFR AD RECVD', '').strip()
      elif des.find('[IN]') != -1:
          return 'BMO'
      else:
          return np.nan
  
    cheq['Paid From'] = df['Description'].apply(lambda des: Income_replace_paid_from(des))
    cheq['Description'] = ''
    cheq['Payment Type'] = ['Direct Deposit' if pay == 'BMO' else 'E-Transfer' for pay in cheq['Paid From']]
    return cheq

  def Income_saving_helper(self, saving_file):

    save= pd.DataFrame()
    df = pd.read_csv(saving_file, skiprows = 3)
    save['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    save['No.'] = ''
    save['Currency'] = 'CAD'
    avoid = ((-df.Description.str.contains('0389#8815')) & (-df.Description.str.contains('INTERAC E-TRANSFER FEE')))
    save['Receipt Amount'] = np.where(
          #Condition:
          (df['Transaction Type'] == 'CREDIT') & avoid,
          df[' Transaction Amount'],
          np.nan
        )
    save['Exchange-CAD'] = ''
    #Deals with typical e-transfer received

    def Income_replace_paid_from(des):
      if des.find('[CW]INTERAC ETRNSFR AD RECVD') != -1:
          return des.replace('[CW]INTERAC ETRNSFR AD RECVD', '').strip()
      elif des.find('[IN]') != -1:
          return 'BMO'
      else:
          return np.nan
       
    save['Paid From'] = df['Description'].apply(lambda des: Income_replace_paid_from(des))
    save['Description'] = ''
    save['Payment Type'] = ['Direct Deposit' if pay == 'BMO' else 'E-Transfer' for pay in save['Paid From']]
    return save
  
  def income_transform(self, cheque_file, saving_file):
    '''
    This method should return a CSV file that is correctly transformed, containing
    desired form, precise number etc. 
    Remember, 
      1. Internal transaction should not be included
      2. E-transfer fee should not be included
      3. Interest earned and maintanence fee should be included
    '''
    #Write your code here...
    #Chequeing first
    cheq_income = self.Income_chequeing_helper(cheque_file=cheque_file)
    #Saving account
    save_income = self.Income_saving_helper(saving_file=saving_file)
    #Combine both
    final = pd.concat([cheq_income, save_income], axis=0)
    final.reset_index(drop=True, inplace = True)
    final.drop(
       index=final[final.isna().any(axis=1)].index,
       axis = 0,
       inplace = True
    )
    final.reset_index(drop = True, inplace = True)
    print('Income sheet generated')
    return final
  
  def Expenditure_chequeing_helper(self, cheque_file):
    
    cheq = pd.DataFrame()
    df = pd.read_csv(cheque_file, skiprows = 3)
    cheq['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    cheq['No.'] = ''
    cheq['Currency'] = 'CAD'
    #Avoid Internal Transaction and E-Transfer Fee
    avoid = ((-df.Description.str.contains('0389#8815')) & (-df.Description.str.contains('INTERAC E-TRANSFER FEE')))
    
    cheq['Receipt Amount'] = np.where(
            #Condition:
              (df['Transaction Type'] == 'DEBIT') & avoid,
              abs(df[' Transaction Amount']),
              np.nan
          )
    cheq['Total Amount'] = ''
    #Deals with typical e-transfer received

    def Income_replace_paid_to(des):
      if des.find('[CW]INTERAC ETRNSFR SENT') != -1:
          des = des.replace('[CW]INTERAC ETRNSFR SENT', '')
          return des.replace(des.split().pop(), '').strip()
      elif des.find('[SC]MAINTENANCE FEE') != -1:
          return 'BMO'
      else:
          return np.nan
  
    cheq['Paid To'] = df['Description'].apply(lambda des: Income_replace_paid_to(des))
    cheq['Description'] = ''
    cheq['Payment Type'] = ['BMO Service Fee' if pay == 'BMO' else 'E-Transfer' for pay in cheq['Paid To']]
    return cheq
  
  def Expenditure_saving_helper(self, saving_file):
    
    save = pd.DataFrame()
    df = pd.read_csv(saving_file, skiprows = 3)
    save['Date'] = df['Date Posted'].apply(lambda date: pd.to_datetime(date, format='%Y%m%d').strftime('%Y%m%d'))
    save['No.'] = ''
    save['Currency'] = 'CAD'
    #Avoid Internal Transaction and E-Transfer Fee
    avoid = ((-df.Description.str.contains('0389#8815')) & (-df.Description.str.contains('INTERAC E-TRANSFER FEE')))
    
    save['Receipt Amount'] = np.where(
            #Condition:
              (df['Transaction Type'] == 'DEBIT') & avoid,
              abs(df[' Transaction Amount']),
              np.nan
          )
    save['Total Amount'] = ''
    #Deals with typical e-transfer received

    def Income_replace_paid_to(des):
      if des.find('[CW]INTERAC ETRNSFR SENT') != -1:
          des = des.replace('[CW]INTERAC ETRNSFR SENT', '')
          return des.replace(des.split().pop(), '').strip()
      elif des.find('[SC]MAINTENANCE FEE') != -1:
          return 'BMO'
      else:
          return np.nan
  
    save['Paid To'] = df['Description'].apply(lambda des: Income_replace_paid_to(des))
    save['Description'] = ''
    save['Payment Type'] = ['BMO Service Fee' if pay == 'BMO' else 'E-Transfer' for pay in save['Paid To']]
    return save
  
  def expenditure_transform(self, cheque_file, saving_file):
    '''
    This method should return a CSV file that is correctly transformed, containing
    desired form, precise number etc. 
    Remember, 
      1. Internal transaction should not be included
      2. E-transfer fee should not be included
      3. Interest earned and maintanence fee should be included
    '''
    
    #Write your code here...
    #Chequeing first
    cheq_income = self.Expenditure_chequeing_helper(cheque_file=cheque_file)
    #Saving account
    save_income = self.Expenditure_saving_helper(saving_file=saving_file)
    #Combine both
    final = pd.concat([cheq_income, save_income], axis=0)
    final.reset_index(drop=True, inplace = True)
    final.drop(
       index=final[final.isna().any(axis=1)].index,
       axis = 0,
       inplace = True
    )
    final.reset_index(drop = True, inplace = True)
    print('Expenditure sheet generated')
    return final


