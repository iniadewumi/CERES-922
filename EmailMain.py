import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText		
import re


class Email:
    def __init__(self):
        self.sender_email = ''	
        self.password = ''	
        self.recipients = []
        self.subject = ''
        
        
        self.regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        self.emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    def sender_email_validator(self, email):
        '''
        NOTE
        ----------
        Cleans recipient list for symbols, emojis, etc. Then verifies syntax via Regex

        Parameters
        ----------
        email : TYPE
            DESCRIPTION.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        email : TYPE
            DESCRIPTION.

        '''
        #clean emojis and symbols from email
        email = self.emoji_pattern.sub(r'', str(email))
        print(email)
        #checks for valid email pattern
        if(re.search(self.regex, email)):
            return email
            
        raise ValueError(f"Email: {email} {type(email)}\nEmail syntax validation failed!")
    
    
    def recipients_validator(self, recipients):
        '''
        NOTE
        ----------
        Cleans recipient list for symbols, emojis, etc. Then verifies syntax via Regex

        Parameters
        ----------
        recipients : TYPE
            DESCRIPTION.

        Returns
        -------
        recipients : TYPE
            DESCRIPTION.

        '''
        
        if type(recipients)==list:
            #clean emojis and symbols from emails
            recipients = [self.emoji_pattern.sub(r'', str(email)) for email in recipients]
            
            #checks for valid email pattern
            recipients = [email for email in recipients if re.search(self.regex, email)!=None]
            self.wrong_emails = [email for email in recipients if re.search(self.regex, email)==None]
            
            print(f'{len(self.wrong_emails)} emails had incorrect syntax')
            UserWarning(f'{len(self.wrong_emails)} emails had incorrect syntax', self.wrong_emails)
            
            return recipients
        print(recipients)
        raise ValueError(f"{type(recipients)} detected.\nPlease enter emails as list!")        
        
    def sendmail(self, sender_email:str, password:str, recipients:list, subject:str, html:str, bcc:str=""):
        
        '''

        Parameters
        ----------
        sender_email : str
            DESCRIPTION: This should be your origin email address.
        password : str
            DESCRIPTION: This is the password for the email account (NOTE: Store in variable for security purposes)
        recipients : list
            DESCRIPTION: List of recipients ['a@b.com', 'b@c.com']
        subject : str
            DESCRIPTION: Email Subject "CERES DAILY EMAIL"
        html : str
            DESCRIPTION: HTML String for email body.
        bcc : str, optional
            DESCRIPTION. The default is "".
            
            
            
        Returns
        -------
        str
            DESCRIPTION: Returns a message informing you of recipients email was sent to.
        recipients : TYPE
            DESCRIPTION.

        '''
        
        self.sender_email = self.sender_email_validator(sender_email)[0].replace("\n", "").strip()
        self.password = password.strip()
        self.recipients = ", ".join(self.recipients_validator(recipients))
        self.subject = subject

            
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipients         
        msg['Bcc'] = bcc
        
        
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        mail = smtplib.SMTP('smtp.gmail.com', 587)
          
        
        
        try:
            mail.ehlo()
            mail.starttls()
            mail.login(user=[EMAIL ADDRESS], password=str(self.password))
            mail.sendmail(from_addr=self.sender_email, to_addrs=self.recipients, msg=msg.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print("Error:", e)
            print("Email and/or password you entered is incorrect")
            return
        except Exception as e:
            print("Error:", e)
            return

        mail.quit()
        return ("Completed, and emails have been sent to", self.recipients)
        

