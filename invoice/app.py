from flask import Flask,redirect, render_template, url_for, request, Response, make_response, send_file

import pdfkit, datetime,os



app = Flask(__name__)


templater = ''
context = {}


@app.route('/')
def index():
    return render_template('inv.html')

@app.route('/in',methods=['POST','GET'])
def collect_value():
    if request.method == 'POST':
        Ftoken = request.form['token']
        FStartD = request.form['sdate']
        FEDate = request.form['edate']
        company = "fairmoney"
        invoice_no = 1
        today = datetime.datetime.now().date()
        unit = 75
        freq = 1000
        subtotal = unit * freq
        vat = 0.075 * subtotal
        total =  vat + subtotal
        global templater
        templater = render_template('index.html',InvoiceNo=invoice_no,Company=company,today=today,unit=unit,freq=freq,subtotal=subtotal,month=FStartD,monthend=FEDate,Vat=vat,total= total)
        global context
        context={
                        
                        
                        "Company" : company,
                        "InvoiceNo" : invoice_no,
                        "today" : today,
                        "unit" : unit,
                        "freq" : freq,
                        "subtotal" : subtotal,
                        "vat" : vat,
                        "total" :  total,
                        "month":FStartD,
                        "monthend":FEDate
                        }
        
        
        return templater
        # return redirect(url_for("download",))
    else:
        return render_template("index.html")
        # tem = pdfkit.from_file(templater, False)
        # return send_file(tem,as_attachment=True,attachment_filename='invoice.pdf' ,mimetype='application/pdf')



@app.route('/return')
def download():
    
    # pdfkit.from_string(templater, 'output.pdf')
    # pdf = open("output.pdf")
    # resp = Response(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
    # resp['Content-Disposition'] = 'attachment; filename=output.pdf'
    # pdf.close()
    # os.remove("output.pdf")  # remove the locally created pdf file.
    # return redirect('inv.html')  # returns the response.

    pdf1 = pdfkit.from_string(templater, False)
    pdf = open(pdf1)
    resp = Response(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
    resp['Content-Disposition'] = 'attachment; filename=output.pdf'
    pdf.close()
    os.remove("output.pdf")  # remove the locally created pdf file.
    return send_file(pdf,as_attachment=True,attachment_filename='invoice.pdf' ,mimetype='application/pdf')
    



if __name__ == "__main__":
    app.run(debug=True)   
