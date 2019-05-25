#!/usr/bin/env python

import os
import re
import glob
from flask import Flask, render_template, redirect, url_for, request
import shutil
import zipfile
from uuid import uuid4


# create the application object
app = Flask(__name__)
html_content_st = """
{% extends 'layout_output.html' %}
{% block title %}output_result{% endblock title %}
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">

{% block main %}
<fieldset>
"""

html_content_ed = """
</fieldset>
{% endblock main %}
"""
# use decorators to link the function to a url

@app.route('/')
def upload_info():
    return render_template('index.html')


@app.route('/respond/<uuid>')
def respond(uuid):
#    outpage = "mysite/templates/{}".format(uuid)
    output_result="output_result_%s.html" % uuid
    return render_template(output_result, uuid=uuid)


@app.route('/submit', methods=['POST'])
def submit():
        #   """Handle the upload of a file."""
    form = request.form

        # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())
    target_folder = "/home/litina2011/mysite/data/" + str(uuid4())+"/"
        # Target folder for these uploads.
    target = "{}".format(target_folder)
    try:
            os.mkdir(target)
    except:
                return "Couldn't create upload directory: {}".format(target)
    pos_check=["rs662799","rs1121980","rs9939609","rs2229616","rs429358","rs7412","rs75932628"]
    for upload in request.files.getlist("input_file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        upload.save(destination)
    folder = target_folder +"*"
    myqtype = request.form['query_type']
    for file in glob.glob(folder):
        if not file.split('.')[-1]=='zip' and not file.split('.')[-1]=='txt':
            outfile_name = "/home/litina2011/mysite/templates/output_result_%s.html" % upload_key
            outfile = open(outfile_name, 'w')
            outfile.write(html_content_st)
            outfile.write("<legend>Your Obesity risk profile</legend>")
            outfile.write("<h3>This file may not be the file downloaded from 23andme or not the version supported.</h3>")
            outfile.write(html_content_ed)
        else:
            if file.split('.')[-1]=='zip':
                zip_ref = zipfile.ZipFile(destination, 'r')
                zip_ref.extractall(target)
                upload_file = file.split('.')[:-1].pop()+".txt"

                zip_ref.close()
                os.remove(file)
            else:
                upload_file = file
            upfile = open(upload_file,'r')
            lines = upfile.readlines()
            pos_count=0
            for line in lines:
                line = line.rstrip()
                rec = line.split('\t')
                if rec[0][0]!="#" and len(rec)!=4:
                    outfile_name = "/home/litina2011/mysite/templates/output_result_%s.html" % upload_key
                    outfile = open(outfile_name, 'w')
                    outfile.write(html_content_st)
                    outfile.write("<legend>Your Obesity risk profile</legend>")
                    outfile.write("<h3>This file may not be the file downloaded from 23andme or not the version supported.</h3>")
                    outfile.write(html_content_ed)
                    break
                elif rec[0][0]!="#":

                    for elem in pos_check:
                        if re.match(elem,rec[0]):
                            pos_count+=1
            if pos_count<7:
                outfile_name = "/home/litina2011/mysite/templates/output_result_%s.html" % upload_key
                outfile = open(outfile_name, 'w')
                outfile.write(html_content_st)
                outfile.write("<legend>Your Obesity risk profile</legend>")
                outfile.write("<h3>This file may not be the file downloaded from 23andme or not the version supported.</h3>")
                outfile.write(html_content_ed)
            else:
                if myqtype == "Obesity":
                    check_Obesity(upload_file,upload_key)
                    output_result="output_result_%s.html" % upload_key
                if myqtype == "Alzheimers":
                    check_Alz(upload_file,upload_key)
                    output_result="output_result_alz_%s.html" % upload_key
           # return redirect("http://localhost:5000/test")
                return render_template(output_result)


        return redirect(url_for("respond", uuid=upload_key))


def check_Obesity(in_file, key):

    html_content_st = """
{% extends 'layout_output.html' %}
{% block title %}output_result{% endblock title %}
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">

{% block main %}
<fieldset>
"""

    html_content_ed = """
</fieldset>
{% endblock main %}
"""
    outfile_name = "/home/litina2011/mysite/templates/output_result_%s.html" % key
    outfile = open(outfile_name, 'w')
    outfile.write(html_content_st)
    outfile.write("<legend>Your Obesity risk profile</legend>")
    infile = open(in_file,'r')
    line = infile.readline()
    Obesity_site_count = 0
    unseq = 0
    while line != "":
        line = line.rstrip()
        rec = line.split('\t')
        if rec[0] == "rs662799" and rec[1] == "11" and rec[2] == "116792991":
                if rec[3] == "AG":
                    outfile.write("<p>rs662799 indicates that you are likely to have elevated triglyceride level, higher risk to develop heart disease, but are not likely to gain weight on a high fat diet</p>")
                    Obesity_site_count = Obesity_site_count + 1
                elif rec[3] == "GG":
                    outfile.write("<p>rs662799 indicates that you are likely to have elevated triglyceride level, higher risk to develop heart disease, but are not likely to gain weight on a high fat diet</p>")
                    Obesity_site_count = Obesity_site_count + 1

                elif rec[3] == "--":
                #    outfile.write("rs429358 was not genotyped\n")
                    unseq = unseq + 1
                else:
                    Obesity_site_count = Obesity_site_count
        if rec[0] == "rs1121980" and rec[1] == "16" and rec[2] == "53775335":
                if rec[3] == "CT" or rec[3] == "TC":
                    outfile.write("<p>rs429358 Allele indicates that your risk of early onset obesity is ~1.67 times elevated</p>")
                    Obesity_site_count = Obesity_site_count + 1
                elif rec[3] == "TT":
                    outfile.write("<p>rs429358 Allele indicates that your risk of early onset obesity is ~2.76 times elevated</p>")
                    Obesity_site_count = Obesity_site_count + 1
                elif rec[3] == "--":
                # outfile.write("rs75932628 was not genotyped\n")
                    unseq = unseq + 1
                else:
                    Obesity_site_count = Obesity_site_count
        if rec[0] == "rs9939609" and rec[1] == "16" and rec[2] == "53786615":
                if rec[3] == "AA":
                    outfile.write("<p>rs9939609 indicates that you have elevated risk of obesity and your risk of Type 2 Diabetes is 1.6 times elevated</p>")
                    Obesity_site_count = Obesity_site_count + 1
                elif rec[3] == "AT":
                    outfile.write("<p>rs9939609 indicates that you have elevated risk of obesity and your risk of Type 2 Diabetes is 1.3 times elevated</p>")
                    Obesity_site_count = Obesity_site_count + 1
                elif rec[3] == "TT":
                    outfile.write("<p>Congratulations! rs9939609 indicates that your risk of obesity and Type 2 Diabetes is lower than most people.</p>")
                    Obesity_site_count = Obesity_site_count
                elif rec[3] == "--":
                # outfile.write("rs7412 was not genotyped\n")
                    unseq = unseq + 1
                else:
                    Obesity_site_count = Obesity_site_count
        if rec[0] == "rs2229616" and rec[1] == "18" and rec[2] == "60372043":
                if rec[3] == "AA" or rec[3] == "GA" or rec[3] == "AG":
                    outfile.write("<p>Congratulations! rs2229616 indicates that you have lower risk of metabolic syndrome, such as appetite control and BMI")
                elif rec[3] == "--":
                # outfile.write("rs75932628 was not genotyped\n")
                    unseq = unseq + 1
        line = infile.readline()
    if Obesity_site_count == 0:
        outfile.write("<h3>You don't have elevated risk of obesity</h3>")
    if Obesity_site_count > 0:
        outfile.write("<h3>Number of risk factors is %s\n" % Obesity_site_count)
    if unseq > 0:
        outfile.write("<h3>Number of risk factors that were not sequenced is %s</h3>" % unseq)
    outfile.write(html_content_ed)


def check_Alz(in_file,key):
    html_content_st = """
        {% extends 'layout_output.html' %}
        {% block title %}output_result{% endblock title %}
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">

        {% block main %}
        <fieldset>
        """

    html_content_ed = """
        </fieldset>
        {% endblock main %}
 """
    outfile_name = "/home/litina2011/mysite/templates/output_result_%s.html" % key
    outfile = open(outfile_name, 'w')
    outfile.write(html_content_st)
    outfile.write("<legend>Your Obesity risk profile</legend>")
    Obesity_site_count = 0
    unseq = 0


    outfile_name = "/home/litina2011/mysite/templates/output_result_alz_%s.html" % key
    outfile = open(outfile_name, 'w')
    outfile.write(html_content_st)
    outfile.write("<legend>Your Alzhermer's risk profile</legend>")
    infile = open(in_file,'r')
    for line in infile:
        line = line.rstrip()
        rec = line.split('\t')
        Alz_site_count = 0
        unseq = 0
        if rec[0]== "rs429358":
                if rec[1] == "CT":
                    outfile.write("rs429358 Allele indicates that your risk of Alzhermer's is ~3 times elevated\n")
                    Alz_site_count = Alz_site_count + 1
                elif rec[1] == "CC":
                    hold="hold"

                elif rec[1] == "--":
                #    outfile.write("rs429358 was not genotyped\n")
                    unseq = unseq + 1
                else:
                     Alz_site_count = Alz_site_count
        if rec[0]== "rs7412":
                if rec[1] == "CC" and hold=="hold":
                    outfile.write("ApoE indicates that your risk of Alzhermer's is ~11 times elevated\n")
                    Alz_site_count = 2
                elif rec[1] == "CT":
                    outfile.write("rs7412 indicates that you are more likely to gain weight if taking olanzapine\n")
                    Alz_site_count = Alz_site_count + 1
                elif rec[1] == "--":
                    #outfile.write("rs7412 was not genotyped\n")
                    unseq = unseq + 1
                else:
                    Alz_site_count = Alz_site_count
        if rec[0]== "rs75932628":
                if rec[1] == "TT":
                    outfile.write("rs429358 Allele indicates that your risk of Alzhermer's is ~3.5 times elevated\n")
                    Alz_site_count = Alz_site_count + 1
                elif rec[1] == "--":
                   unseq = unseq + 1
                else:
                    Alz_site_count = Alz_site_count
    if Alz_site_count == 0:
            outfile.write("You don't have elevated risk of Alzhermer's disease.\n")
    if Alz_site_count > 0:
            outfile.write("Number of risk factors is %s.\n" % Alz_site_count)
    if unseq > 0:
            outfile.write("Number of risk factors that were not sequenced is %s.\n" % unseq)
    outfile.write(html_content_ed)

if __name__ == '__main__':
    print ("A local client for the Personal Genome API is now initialized.")
    app.run(debug=False)
