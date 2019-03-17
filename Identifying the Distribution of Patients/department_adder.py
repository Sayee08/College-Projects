import random
import csv
departments=['Anaesthesiology','Dental Surgery','Dermatology','Ent,Head and Neck Services','General Medicine','General Surgery',
             'Obsterics & Gynaecology','Ophthalmology','Orthopaedics & Trauma','Psychiatry','Paediatrics','Radiology & Imaging','TB & Chest',
             'Cardiothoracis Surgery','Cardiology','Emergency Medicine','Gastroenterology','Nephrology','Neurosurgery','Neurology',
             'Medical Oncology','Paediatric Surgery','Physiotherapy','Plastic Surgery','Pulmonology','Urology','Yoga & Neturopathy',
             'Rheumatology','Hepato-Pancreatic-Biliary Surgery & Liver Transplant Surgery']
with open('sample2.csv','wb') as csvfile:
    data=csv.writer(csvfile)
    count=0
    j=1
    while(count<16230):
        r=random.choice(departments)
        data.writerow([str(r)])
        count=count+1
                    
		
