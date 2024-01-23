import re
import json


def parse_input_format(input_text):
    # Split the input text into lines
    lines = input_text.strip().split('\n')

    # Initialize variables to store parsed data
    subject_name = None
    sections = {}
    current_section = None
    chapters = []

    # Define regular expressions for matching section and chapter lines
    section_pattern = re.compile(r'^section \((\w)\) \| (.+)$', re.IGNORECASE)
    chapter_pattern = re.compile(r'^(\d+(\.\d+)?) (.+)$')

    # Iterate through each line in the input
    for line in lines:
        # Check if the line matches the section pattern
        section_match = section_pattern.match(line)
        if section_match:
            # Update current section
            current_section = section_match.group(2)
            sections[current_section] = []
        else:
            # Check if the line matches the chapter pattern
            chapter_match = chapter_pattern.match(line)
            if chapter_match:
                # Add chapter to the current section
                chapter_number = chapter_match.group(1)
                chapter_name = chapter_match.group(3)
                chapters.append({"name": f"{chapter_number} {chapter_name}", "questions": []})

    # Create the final data structure
    subject_data = {"sections": {current_section: {"chapters": chapters}}}
    return {subject_name: subject_data} if subject_name else subject_data

# Example Usage:
input_text = """
subject : Contemporary Issues
section (A) | Social Issues
1.1 Social disputes and conflict
1.2 Social justice and equality
1.3 Social and cultural transformationa
1.4 Distributive justice of resources: disparities and marginalization
1.5 Social protection, social securitu and social responsibility
1.6 Cultural diversity and social mobilization
1.7 Populaiton
1.8 Organized Crime
1.9 Food sovereignty and security

section (B) | Economic Issues
2.1 Economic growth and Economic development
2.2 Major aspects of economic development
2.3 Role of public sector, private sector and cooperative in economic development
2.4 Foreign assistance and international co-operation
2.5 Foreign Investment: portfolio and directory
2.6 Technology transfer including intellectual property rights
2.7 Trade, market and labour liberalization
2.8 Economic diplomacy
2.9 Poverty and unemployment

section (C) | Developmental Issues
3.1 Human development
3.2 Infrastructure development
3.3 Sustainable development
3.4 Role of state and non-state actors in development process
3.5 Peace and conflict sensitive development
3.6 Decentralization and local self-governance
3.7 Citizen engagement in development
3.8 Partnership development and community based development
3.9 Role of information and Communication Technology (ICT) in development
3.10 Globalization and development

section (D) | Environmental Issues
4.1 Ecosystem
4.2 Bio-diversity and conservation
4.3 Climate change and carbon Trade
4.4 Environment degradation
4.5 Deforestation
4.6 Crisis/Disaster management
4.7 Environment and development
4.8 Energy crisis and energy conservation
4.9 Pollution and waste management

section (E) | Annex
5.1 The Constitution of Nepal
5.2 Fifteenth Plan
"""
parsed_data = parse_input_format(input_text)
print(parsed_data)

def update_existing_json(existing_json, parsed_data):
    # Extract subject name from parsed data
    subject_name = list(parsed_data.keys())[0] if parsed_data else None

    # Check if the subject already exists in the JSON
    if subject_name in existing_json['subjects']:
        # Update the existing subject with new sections and chapters
        existing_json['subjects'][subject_name]['sections'].update(parsed_data[subject_name]['sections'])
    else:
        # Add a new subject to the JSON
        existing_json['subjects'].update(parsed_data)

    return existing_json

# Example Usage:
existing_json = {
  "subjects": {
    "Governance Systems": {
      "sections": {
        "Section (A) | State and Governance": {
          "chapters": [
            {"name": "1.1 Fundamentals of governance: concept, context and characteristics", "questions": []},
            {"name": "1.2 Political and administrative structures of governance", "questions": []},
            {"name": "1.3 Right to information and transparency", "questions": []},
            {"name": "1.4 Nation building and state building", "questions": []},
            {"name": "1.5 Governance systems in Nepal", "questions": []},
            {"name": "1.6 National security management", "questions": []},
            {"name": "1.7 Multi-level governance and Nepal", "questions": []}
          ]
        },
        "Section (B) | Constitution and Law": {
          "chapters": [
            {"name": "2.1 Constitutionalism", "questions": []},
            {"name": "2.2 Constitutional development in Nepal", "questions": []},
            {"name": "2.3 Present constitution of Nepal", "questions": []},
            {"name": "2.4 Human rights", "questions": []},
            {"name": "2.5 Civic sense, duties and responsibilities of people", "questions": []},
            {"name": "2.6 Sources of law- and law-making process in Nepal", "questions": []},
            {"name": "2.7 Rule of law, democratic values and norms, inclusion, proportional representation and affirmative action", "questions": []}
          ]
        },
        "Section (C) | Public Service and Public Management": {
          "chapters": [
            {"name": "3.1 Concept, functions, characteristics and role of public service", "questions": []},
            {"name": "3.2 Public Service delivery", "questions": []},
            {"name": "3.3 Political neutrality, commitment, transparency and accountability", "questions": []},
            {"name": "3.4 Utilization of public funds, ethics and morality", "questions": []},
            {"name": "3.5 Public management, civil service and bureaucracy", "questions": []},
            {"name": "3.6 Public policy: formulation process and analysis", "questions": []},
            {"name": "3.7 Public Service Charter", "questions": []},
            {"name": "3.8 E-governance", "questions": []}
          ]
        },
        "Section (D) | Resource Management and Planning": {
          "chapters": [
            {"name": "4.1 Human Resource Management: procurement, development, utilization and maintenance", "questions": []},
            {"name": "4.2 Public financial management: planning and budgeting system in Nepal", "questions": []},
            {"name": "4.3 Government accounting and auditing system in Nepal", "questions": []},
            {"name": "4.4 Financial management and social accountability", "questions": []},
            {"name": "4.5 Development planning and current periodic plan", "questions": []},
            {"name": "4.6 Participatory planning and development", "questions": []}
          ]
        }
      }
    },
    "Contemporary Issues": {
      "sections": {
        "section (A) | Social Issues": {
          "chapters": [
            {"name": "1.1 Social disputes and conflict", "questions": []},
            {"name": "1.2 Social justice and equality", "questions": []},
            {"name": "1.3 Social and cultural transformationa", "questions": []},
            {"name": "1.4 Distributive justice of resources: disparities and marginalization", "questions": []},
            {"name": "1.5 Social protection, social securitu and social responsibility", "questions": []},
            {"name": "1.6 Cultural diversity and social mobilization", "questions": []},
            {"name": "1.7 Populaiton", "questions": []},
            {"name": "1.8 Organized Crime", "questions": []},
            {"name": "1.9 Food sovereignty and security", "questions": []}
          ]
        },
        "section (B) | Economic Issues": {
          "chapters": [
            {"name": "2.1 Economic growth and Economic development", "questions": []},
            {"name": "2.2 Major aspects of economic development", "questions": []},
            {"name": "2.3 Role of public sector, private sector and cooperative in economic development", "questions": []},
            {"name": "2.4 Foreign assistance and international co-operation", "questions": []},
            {"name": "2.5 Foreign Investment: portfolio and directory", "questions": []},
            {"name": "2.6 Technology transfer including intellectual property rights", "questions": []},
            {"name": "2.7 Trade, market and labour liberalization", "questions": []},
            {"name": "2.8 Economic diplomacy", "questions": []},
            {"name": "2.9 Poverty and unemployment", "questions": []}
          ]
        },
        "section (C) | Developmental Issues": {
          "chapters": [
            {"name": "3.1 Human development", "questions": []},
            {"name": "3.2 Infrastructure development", "questions": []},
            {"name": "3.3 Sustainable development", "questions": []},
            {"name": "3.4 Role of state and non-state actors in development process", "questions": []},
            {"name": "3.5 Peace and conflict sensitive development", "questions": []},
            {"name": "3.6 Decentralization and local self-governance", "questions": []},
            {"name": "3.7 Citizen engagement in development", "questions": []},
            {"name": "3.8 Partnership development and community based development", "questions": []},
            {"name": "3.9 Role of information and Communication Technology (ICT) in development", "questions": []},
            {"name": "3.10 Globalization and development", "questions": []}
          ]
        },
        "section (D) | Environmental Issues": {
          "chapters": [
            {"name": "4.1 Ecosystem", "questions": []},
            {"name": "4.2 Bio-diversity and conservation", "questions": []},
            {"name": "4.3 Climate change and carbon Trade", "questions": []},
            {"name": "4.4 Environment degradation", "questions": []},
            {"name": "4.5 Deforestation", "questions": []},
            {"name": "4.6 Crisis/Disaster management", "questions": []},
            {"name": "4.7 Environment and development", "questions": []},
            {"name": "4.8 Energy crisis and energy conservation", "questions": []},
            {"name": "4.9 Pollution and waste management", "questions": []}
          ]
        },
        "section (E) | Annex": {
          "chapters": [
            {"name": "5.1 The Constitution of Nepal", "questions": []},
            {"name": "5.2 Fifteenth Plan", "questions": []}
          ]
        }
      }
    }
  }
}


updated_json = update_existing_json(existing_json, parsed_data)


def save_to_json(updated_json, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(updated_json, json_file, indent=1)

# Example Usage:
output_file_path = 'output_file.json'  # Replace with the desired path and filename
save_to_json(updated_json, output_file_path)