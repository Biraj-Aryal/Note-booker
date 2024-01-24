import json

def process_text_to_json(existing_json, text):
    subjects = existing_json.get('subjects', {})
    
    lines = text.strip().split('\n')
    subject_name = lines[0].split(': ')[1].strip()
    
    sections = {}
    current_section = None
    current_chapters = []
    
    for line in lines[1:]:
        if line.startswith('section ('):
            if current_section:
                sections[current_section] = {"chapters": current_chapters}
                current_chapters = []
                
            current_section = line.split('|')[1].strip()
        else:
            current_chapters.append({"name": line.strip(), "questions": []})
    
    if current_section:
        sections[current_section] = {"chapters": current_chapters}
    
    subjects[subject_name] = {"sections": sections}
    
    return {"subjects": subjects}

def append_text_to_existing_json(existing_json, text):
    new_json = process_text_to_json(existing_json, text)
    existing_json["subjects"].update(new_json["subjects"])
    return existing_json

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=None)

def load_json_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"subjects": {}}

if __name__ == "__main__":

    # Example usage:
    json_filename = 'subjects_data.json'
    existing_json = load_json_from_file(json_filename)

    text_from_book = """subject : Laws Issues

section (A) | Law Issues
1.1 legal disputes and conflict
1.2 Social justice and equality
1.3 Social and cultural transformationa
1.4 Distributive justice of resources: disparities and marginalization
1.5 Social protection, social securitu and social responsibility
1.6 Cultural diversity and social mobilization
1.7 Populaiton
1.8 Organized Crime
1.9 Food sovereignty and security

section (B) | Financial Issues
1.1 legal disputes and conflict
1.2 Social justice and equality
1.3 Social and cultural transformationa
1.4 Distributive justice of resources: disparities and marginalization
1.5 Social protection, social securitu and social responsibility
1.6 Cultural diversity and social mobilization
1.7 Populaiton
1.8 Organized Crime
1.9 Food sovereignty and security
"""

    updated_json = append_text_to_existing_json(existing_json, text_from_book)
    save_json_to_file(updated_json, json_filename)






'''


subject : Contemporary Law and Practices

section (A) | Law and Justice Related Contemporary Issues
1.1 Constitution and Constitutionalism
1.2 Fundamental aspects of Civil and Criminal Code
1.3 Human RIghts & International Law
1.4 Corruption, Organized Crime and Money Laundering
1.5 Judicial Activism and Public Interest Litigation
1.6 Alternative Dispute Resolution (ADR)
1.7 Concept of Environmental Justice
1.8 Consumer's Right Protection
1.9 Gender Justice and Domestic Violence
1.10 Concept of Victimology

section (B) | Law Drafting and Other legal aspects
2.1 Concept of drafting and philosophical consent of act, rule notified order and ordinance
2.2 Construction of treaty agreement
2.3 Editing of notice published in Nepal Gazette
2.4 Legislative Procedures
2.5 Delegated Legislation
2.6 Intellectual Property Rights
2.7 Contract
2.8 Writ 
2.9 Judicial rights of Administrative bodies
2.10 Civil Service Act

section (C) | Theoretical and Practical Issues of Law Related to Government Attorney
3.1 Attorney General
3.2 Investigation and Prosecution of State Criminal Cases
3.3 Bail and Witness Examination
3.4 Legal Opinion
3.5 Appeal and Defense State Party Criminal Case
3.6 Art of Pleading (Legal Advocacy) and Pleading Management
3.7 Professional Skill (competency) and Code of Conduct of Government Attorney
3.8 Comparative study on the role of Government Attorney
3.9 Civil Crimes Code, 2074
3.10 Civil Criminal Procedure Code, 2074
3.11 Criminal Offenses (Sentencing and Enforcement) Act, 2074
3.12 Government Attorney Regulation

section (D) | Court Related Functions and Procedures
4.1 Locus Standi, Limitation
4.2 Jurisdiction of Court of Nepal
4.3 Registration and Endorsement of Document
4.4 Court Fee, Bail and Surety
4.5 Statement or Deposition, Attorney and Sakarnama
4.6 Interlocutory order and Interim order
4.7 Examination of Evidence
4.8 Theoretical & Practical Knowledge Regarding Judgement 
4.9 Appeal and Execution of Judgement
4.10 Administration of Justice & Judicial Service Commission
4.11 Supreme court regulation, High Court regulation and District court regulation
4.12 Nepal Judicial Service (Formation, Group, Category, Division, Appointment) Rules, 2051



'''