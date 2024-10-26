# report/views.py
import pandas as pd
from django.core.mail import send_mail
from django.shortcuts import render

def custom_dataframe_summary(df):
    # Create a summary string
    summary = f"Data Shape : {df.shape[0]} rows and {df.shape[1]} columns.\n\n"
    
    # Loop through columns to get data types and missing value counts
    summary += "Columns Information:\n"
    for col in df.columns:
        dtype = df[col].dtype
        missing_count = df[col].isnull().sum()
        summary += f"- {col}: Type: {dtype} || Missing Values: {missing_count}\n"
    
    return summary


def upload_file(request):
    info_summary = ""
    data_table = ""
    if request.method == 'POST':
        # Check if 'file' key exists in request.FILES
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            # Determine the file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                return render(request, 'index.html', {'summary': 'Invalid file format.'})

            # Generate summary and convert DataFrame to HTML
            info_summary = custom_dataframe_summary(df)
            
            data_table = df.to_html(classes='data', header="true", index=False)  # Convert DataFrame to HTML

            # Create the email body
            email_body = f'''
            <h1>File Summary and Data table</h1>
            <h2>Summary</h2>
            <pre>{info_summary}</pre>
            <h2>Data Table:</h2>
            {data_table}
             
            <h2>Best regards,<br>
            Vinay Kumar Rai</h2>
            '''

           #send email 
            send_mail(
                'Python Assignment - Vinay Kumar Rai',
                'Please see the attached data table.',
                'demo911check@gmail.com',  
                ['vinay19rai@gmail.com'],  
                html_message=email_body, 
                fail_silently=False,
            )
        else:
            info_summary = "No file was uploaded."

   # Returent the summary and data table to HTML
    return render(request, 'index.html', {'summary': info_summary, 'data_table': data_table})
