# -*- coding: utf-8 -*-
"""MobileHCI - Generation Prompt

## Setup
#### Load the API key and relevant Python libaries.
"""

from google.colab import files
import io
from dotenv import dotenv_values, load_dotenv, find_dotenv
import openai
import os
import json
import numpy as np

uploaded = files.upload()

# Get the first key from the uploaded dictionary
# Generate OpenAI key and use it here
env_file_key = list(uploaded.keys())[0]

# Read the uploaded file
env_content = uploaded[env_file_key].decode('utf-8')

# Load the content into a variable
env_variables = dotenv_values(stream=io.StringIO(env_content))

api_key = env_variables['OPENAI_API_KEY']
openai.api_key = api_key

"""# Models"""

def get_completion_from_messages(messages,
                                 model="gpt-4",
                                 temperature=0,
                                 max_tokens=7000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can output
    )
    return response.choices[0].message["content"]

def get_completion_and_token_count(messages,
                                 model="gpt-4",
                                 temperature=0,
                                 max_tokens=7000):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message["content"]

    token_dict = {
    'prompt_tokens':response['usage']['prompt_tokens'],
    'completion_tokens':response['usage']['completion_tokens'],
    'total_tokens':response['usage']['total_tokens'],
    }

    return content, token_dict

"""# Var: 3 System Role, Instruction, Risk Concepts, Domains, Examles

### Domain 1-8
"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Biometric identification and categorization of natural persons
        2. Family
        3. Romantic relationships and friendships
        4. Health and Healthcare
        5. Well-being
        6. Human-Computer Interaction
        7. Finance and Investment
        8. Education and vocational training

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

# response, token_count = get_completion_and_token_count(messages)
# print(token_count)

# res = token_count
# cost = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
# cost * 6

print(response)

RESPONSES=[]
RESPONSES.append(response)

"""### Domain 9-16"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Employment, workers management and access to self-employment
        2. Essential private services and public services and benefits
        3. Recommender Systems and Personalization
        4. Social Media
        5. Sports and Recreation
        6. Arts and Entertainment
        7. Security and Cybersecurity
        8. Marketing and Advertising

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

RESPONSES.append(response)

"""### Domain 17-24"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Agriculture and Farming
        2. Entrepreneurship
        3. Autonomous Robots and Robotics
        4. Innovation and Research
        5. Management and Operation of critical infrastructure
        6. Law enforcement
        7. Migration, Asylum and Border control management
        8. Democracy

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

RESPONSES.append(response)

"""### Domain 25-32"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Media and Communication
        2. Accessibility and Inclusion
        3. Energy
        4. Military and Defense
        5. Administration of justice and democratic processes
        6. Government Services and Administration
        7. Diplomacy and Foreign Policy
        8. Food Safety and Regulation

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

RESPONSES.append(response)

"""### Domain 33-40"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Crisis Management and Emergency Response
        2. Humanitarian Aid
        3. Transport and Logistics
        4. Urban Planning
        5. Counterterrorism
        6. Environment and Sustainability
        7. International Law Enforcement and Cooperation
        8. Climate Change Mitigation and Adaptation

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

RESPONSES.append(response)

"""### Domain 41-46 (from Miro)"""

messages = [
    {
        'role': 'system',
        'content': """
        As a senior Mobile and Wearable Systems Specialist, you specialize in the latest developments of mobile and wearable technology.
        Mobile and wearable computing involves collecting and analyzing sensor-gathered data to offer insights into individuals' daily activities, whereabouts, and health status.
        These observations can be made from mobile phones, smartwatches, earables, wearables, and sensors. The range of sensing instruments includes, accelerometer, gyroscope, photoplethysmography, electroencephalography, electromyography, among others.
        In this pivotal role, you are entrusted with reviewing, and cataloguing the diverse applications and use cases of mobile and wearable technology across multiple domains.
        """
    },
    {
        'role': 'user',
        'content': """
        Create a comprehensive and self-explanatory list, in JSON format, detailing the various uses of mobile and wearable technology. Each dictionary in the created list describes a particular use case or application of mobile and wearable technology.
        Provide three uses for each of the 8 domains listed below. The uses must contain specific details about how the technology is used, by using action verbs that clearly describe the actions, activities, or processes of the uses.
        The level of specificity should be consistent across all uses.
        For each of these uses, you must output the following 7 elements each in less than 7 words:
        (1) Use: An element of a series of numbered uses, starting with 1. Each use should be listed consecutively.
        (2) Domain: The domain that represents the area or sector the AI system is intended to be used in.
        (3) Purpose: The purpose or objective that is intended to be accomplished by using an AI system.
        (4) Capability: The capability of the AI system that enables the realization of its purpose and reflects the technological capability.
        (5) Sensing instrument and location: The sensing technologies that enable observation require unique input from mobile and wearable sensors such as accelerometers, gyroscopes, photoplethysmography, cameras, and global positioning systems. These sensors are placed in various objects or parts of the body, such as the torso, wrist, and pocket, to monitor human behavior, physical, mental, emotional, and social status, among others.
        (6) AI user: The entity or individual in charge of deploying and managing the AI system, including individuals, organizations, corporations, public authorities, and agencies responsible for its operation and management.
        (7) AI subject: The individual directly affected by the use of the AI system, experiencing its effects and consequences. They interact with or are impacted by the AI system's processes, decisions, or outcomes.
        Ensure that each concept is specific and easy to understand for non-experts. Avoid duplicate purposes or objectives and use clear and precise language to describe the uses' concepts.

        Domains to be included are the following:
        1. Gaming and interactive experiences
        2. Hobbies
        3. Smart home
        4. Social and Community Services
        5. Public and private transportation
        6. Interpersonal Communication

        Follow this example structure for reporting the identified uses:
        [
            {
                "Use": 1,
                "Domain": "Gaming and interactive experiences",
                "Purpose": "Improve player engagement and control in virtual environments",
                "Capability": "Tracking real-time motion and environmental interaction",
                "Observation instrument": "Wearable sensors",
                "AI User": "Game Studios and Developers",
                "AI Subject": "Gamers"
            },
            {
                "Use": 2,
                "Domain": "Sports and Recreation",
                "Purpose": "Enhance athletic performance and safety",
                "Capability": "Monitoring vital signs and movement data",
                "Observation instrument": "Smartwatches",
                "AI User": "Sports teams and coaching staff",
                "AI Subject": "Athletes"
            },
            {
                "Use": 3,
                "Domain": "Well-being",
                "Purpose": "Promote mental and emotional health",
                "Capability": "Tracking physiological signals of stress",
                "Observation instrument": "Smartwatches",
                "AI User": "Health app developers",
                "AI Subject": "Health app users"
            },
            {
                "Use": 4,
                "Domain": "Employment",
                "Purpose": "Prevent workplace accidents",
                "Capability": "Tracking physical movements",
                "Observation instrument": "Smartwatches",
                "AI User": "Supervisor safety officers",
                "AI Subject": "Employees"
            },
            {
                "Use": 5,
                "Domain": "Military and Defense",
                "Purpose": "Augment situational awareness in field operations",
                "Capability": "Biometric monitoring and environmental sensing",
                "Observation instrument": "Smartwatches and air quality sensors",
                "AI User": "Military institutions",
                "AI Subject": "Soldiers"
            }
        ]
        """
    }
]

response = get_completion_from_messages(messages)
print(response)

# response, token_count = get_completion_and_token_count(messages)
# print(token_count)

res = {'prompt_tokens': 810, 'completion_tokens': 1156, 'total_tokens': 1966}
cost = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
print(cost)

RESPONSES.append(response)

"""#### JSON"""

# Assuming RESPONSES is a list of JSON-formatted responses
response1 = json.loads(RESPONSES[0])
response2 = json.loads(RESPONSES[1])
response3 = json.loads(RESPONSES[2])
response4 = json.loads(RESPONSES[3])
response5 = json.loads(RESPONSES[4])
response6 = json.loads(RESPONSES[5])

# Concatenate the responses into a single list
output = [response1, response2, response3, response4, response5, response6]


# Use json.dump to write the list to a file in JSON format
with open('MobileHCI_uses.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)  # 4 spaces of indentation

# Download the file to your local machine
files.download('MobileHCI_uses.json')

