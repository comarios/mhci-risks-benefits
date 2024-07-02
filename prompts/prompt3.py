# -*- coding: utf-8 -*-
"""Mobile HCI - SDGs Prompt

## Setup
#### Load the API key and relevant Python libaries.
"""


from google.colab import files
import io
from dotenv import dotenv_values, load_dotenv, find_dotenv
import openai
import os
from copy import deepcopy
import json
import time
import ast

import pprint

# env file
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
                                 max_tokens=950): #1100
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut
    )
    return response.choices[0].message["content"]

def get_completion_and_token_count(messages,
                                 model="gpt-4",
                                 temperature=0,
                                 max_tokens=950):

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

"""# Iterate and Save Use Riskiness Results

# Functions
"""

def replace_key(d, old_key, new_key):
  """
  Replace `old_key` with `new_key` in dictionary `d`.
  The associated value is retained.
  """
  if old_key in d:
      d[new_key] = d.pop(old_key)
  return d

"""## Read In Prompt Result"""

def read_prompt_output():
  print("Select the right input you need.")
  selected_prompt_uploaded = files.upload() # change this for other prompts

  # Get the first key from the uploaded dictionary
  file_key = list(selected_prompt_uploaded.keys())[0]

  # Read the uploaded file
  file_content = selected_prompt_uploaded[file_key].decode('utf-8')

  file_content_dict = ast.literal_eval(file_content)

  N = len(file_content_dict[0])

  # rename the uses so that we have 46 ids
  i = 0
  for el in file_content_dict:
    for use_el in el:
      use_el['Use'] = int(use_el['Use']) + i * N
    i += 1

  flattened_list = [item for sublist in file_content_dict for item in sublist]
  return flattened_list

prompt_result = read_prompt_output()

prompt_result

"""# PART 1 PROMPT: SDGs 1-5"""

# Assuming you have the variables domain, purpose, aiCapability, aiUser, and aiSubject defined with appropriate values

MESSAGES = [
    {
        'role': 'system',
        'content': """You are a renowned specialist in the field of mobile and wearable technology with a dedicated focus on understanding, promoting, and implementing the Sustainable Development Goals (SDGs). With your vast experience, decisiveness, and conscientious approach, you have a deep understanding of how mobile and wearable technologies can be leveraged to support the SDGs.
        You possess comprehensive knowledge of the List of Sustainable Development Goal targets and indicators, which encapsulates all targets and indicators for the 17 SDGs. This global framework was meticulously crafted by the Inter-Agency and Expert Group on SDG Indicators (IAEG-SDGs) and was ratified during the 48th session of the United Nations Statistical Commission in March 2017.
        The framework you reference encompasses all subsequent refinements to the official indicator list."""
    },
    {
        'role': 'user',
        'content': """

        Assess the AI system's alignment with the Sustainable Development Goals (SDGs).

        Follow the streamlined steps below:
        1. Describe the AI System: Craft a concise description of the AI system, ensuring it parallels the phrasing used in the Sustainable Development Goal targets and indicators. Your description should begin with "The AI system is designed to..." and should be encapsulated within two sentences.
        2. Evaluate Each SDG:
            For each of the 3 given SDGs, assess if the AI system aligns with or supports the respective SDG. Reference the exact text from the SDG targets and indicators and provide a thorough rationale.
            Rigorously validate your reasoning. The true intent and capabilities of the AI system are crucial for this evaluation. Ensure there is a direct correlation between the system's functionalities and the referenced indicators.
        3. Reference Targets & Indicators: While evaluating, explicitly cite the SDG targets and indicators that resonate most with the AI system's purpose and capabilities.
        4. Classify Non-relevant SDGs: If the AI system does not align with a particular SDG, label it as "Not Relevant" for that SDG.

        Remember, precision is paramount. It's vital to make informed and accurate determinations regarding the AI system's alignment with each SDG. Ensure all SDG targets and indicators are meticulously considered during your assessment.

        Goal 1: End poverty in all its forms everywhere
        Targets:
        1.1 By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day
        1.2 By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions
        1.3 Implement nationally appropriate social protection systems and measures for all, including floors, and by 2030 achieve substantial coverage of the poor and the vulnerable
        1.4 By 2030, ensure that all men and women, in particular the poor and the vulnerable, have equal rights to economic resources, as well as access to basic services, ownership and control over land and other forms of property, inheritance, natural resources, appropriate new technology and financial services, including microfinance
        1.5 By 2030, build the resilience of the poor and those in vulnerable situations and reduce their exposure and vulnerability to climate-related extreme events and other economic, social and environmental shocks and disasters
        1.a Ensure significant mobilization of resources from a variety of sources, including through enhanced development cooperation, in order to provide adequate and predictable means for developing countries, in particular least developed countries, to implement programmes and policies to end poverty in all its dimensions
        1.b Create sound policy frameworks at the national, regional and international levels, based on pro-poor and gender-sensitive development strategies, to support accelerated investment in poverty eradication actions

        Indicators:
        1.1.1 Proportion of the population living below the international poverty line by sex, age, employment status and geographic location (urban/rural)
        1.2.1 Proportion of population living below the national poverty line, by sex and age
        1.2.2 Proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions
        1.3.1 Proportion of population covered by social protection floors/systems, by sex, distinguishing children, unemployed persons, older persons, persons with disabilities, pregnant women, newborns, work-injury victims and the poor and the vulnerable
        1.4.1 Proportion of population living in households with access to basic services
        1.4.2 Proportion of total adult population with secure tenure rights to land, (a) with legally recognized documentation, and (b) who perceive their rights to land as secure, by sex and type of tenure
        1.5.1 Number of deaths, missing persons and directly affected persons attributed to disasters per 100,000 population
        1.5.2 Direct economic loss attributed to disasters in relation to global gross domestic product (GDP)
        1.5.3 Number of countries that adopt and implement national disaster risk reduction strategies in line with the Sendai Framework for Disaster Risk Reduction 2015–2030
        1.5.4 Proportion of local governments that adopt and implement local disaster risk reduction strategies in line with national disaster risk reduction strategies
        1.a.1 Total official development assistance grants from all donors that focus on poverty reduction as a share of the recipient country's gross national income
        1.a.2 Proportion of total government spending on essential services (education, health and social protection)
        1.b.1 Pro-poor public social spending


        Goal 2: End hunger, achieve food security and improved nutrition and promote sustainable agriculture
        Targets:
        2.1 By 2030, end hunger and ensure access by all people, in particular the poor and people in vulnerable situations, including infants, to safe, nutritious and sufficient food all year round.
        2.2 By 2030, end all forms of malnutrition, including achieving, by 2025, the internationally agreed targets on stunting and wasting in children under 5 years of age, and address the nutritional needs of adolescent girls, pregnant and lactating women and older persons.
        2.3 By 2030, double the agricultural productivity and incomes of small-scale food producers, in particular women, indigenous peoples, family farmers, pastoralists and fishers, including through secure and equal access to land, other productive resources and inputs, knowledge, financial services, markets and opportunities for value addition and non-farm employment.
        2.4 By 2030, ensure sustainable food production systems and implement resilient agricultural practices that increase productivity and production, that help maintain ecosystems, that strengthen capacity for adaptation to climate change, extreme weather, drought, flooding and other disasters and that progressively improve land and soil quality.
        2.5 By 2020, maintain the genetic diversity of seeds, cultivated plants and farmed and domesticated animals and their related wild species, including through soundly managed and diversified seed and plant banks at the national, regional and international levels, and promote access to and fair and equitable sharing of benefits arising from the utilization of genetic resources and associated traditional knowledge, as internationally agreed.
        2.a Increase investment, including through enhanced international cooperation, in rural infrastructure, agricultural research and extension services, technology development and plant and livestock gene banks in order to enhance agricultural productive capacity in developing countries, in particular least developed countries.
        2.b Correct and prevent trade restrictions and distortions in world agricultural markets, including through the parallel elimination of all forms of agricultural export subsidies and all export measures with equivalent effect, in accordance with the mandate of the Doha Development Round.
        2.c Adopt measures to ensure the proper functioning of food commodity markets and their derivatives and facilitate timely access to market information, including on food reserves, in order to help limit extreme food price volatility.

        Indicators:
        2.1.1 Prevalence of undernourishment.
        2.1.2 Prevalence of moderate or severe food insecurity in the population, based on the Food Insecurity Experience Scale (FIES).
        2.2.1 Prevalence of stunting (height for age <-2 standard deviation from the median of the World Health Organization (WHO) Child Growth Standards) among children under 5 years of age.
        2.2.2 Prevalence of malnutrition (weight for height >+2 or <-2 standard deviation from the median of the WHO Child Growth Standards) among children under 5 years of age, by type (wasting and overweight).
        2.2.3 Prevalence of anaemia in women aged 15 to 49 years, by pregnancy status (percentage).
        2.3.1 Volume of production per labour unit by classes of farming/pastoral/forestry enterprise size.
        2.3.2 Average income of small-scale food producers, by sex and indigenous status.
        2.4.1 Proportion of agricultural area under productive and sustainable agriculture.
        2.5.1 Number of plant and animal genetic resources for food and agriculture secured in either medium- or long-term conservation facilities.
        2.5.2 Proportion of local breeds classified as being at risk of extinction.
        2.a.1 The agriculture orientation index for government expenditures.
        2.a.2 Total official flows (official development assistance plus other official flows) to the agriculture sector.
        2.b.1 Agricultural export subsidies.
        2.c.1 Indicator of food price anomalies.

        Goal 3: Ensure healthy lives and promote well-being for all at all ages
        Targets:
        3.1 By 2030, reduce the global maternal mortality ratio to less than 70 per 100,000 live births
        3.2 By 2030, end preventable deaths of newborns and children under 5 years of age, with all countries aiming to reduce neonatal mortality to at least as low as 12 per 1,000 live births and under‑5 mortality to at least as low as 25 per 1,000 live births
        3.3 By 2030, end the epidemics of AIDS, tuberculosis, malaria and neglected tropical diseases and combat hepatitis, water-borne diseases and other communicable diseases
        3.4 By 2030, reduce by one third premature mortality from non-communicable diseases through prevention and treatment and promote mental health and well-being
        3.5 Strengthen the prevention and treatment of substance abuse, including narcotic drug abuse and harmful use of alcohol
        3.6 By 2020, halve the number of global deaths and injuries from road traffic accidents
        3.7 By 2030, ensure universal access to sexual and reproductive health-care services, including for family planning, information and education, and the integration of reproductive health into national strategies and programmes
        3.8 Achieve universal health coverage, including financial risk protection, access to quality essential health-care services and access to safe, effective, quality and affordable essential medicines and vaccines for all
        3.9 By 2030, substantially reduce the number of deaths and illnesses from hazardous chemicals and air, water and soil pollution and contamination
        3.a Strengthen the implementation of the World Health Organization Framework Convention on Tobacco Control in all countries, as appropriate
        3.b Support the research and development of vaccines and medicines for the communicable and non‑communicable diseases that primarily affect developing countries, provide access to affordable essential medicines and vaccines
        3.c Substantially increase health financing and the recruitment, development, training and retention of the health workforce in developing countries, especially in least developed countries and small island developing States
        3.d Strengthen the capacity of all countries, in particular developing countries, for early warning, risk reduction and management of national and global health risks

        Indicators:
        3.1.1 Maternal mortality ratio
        3.1.2 Proportion of births attended by skilled health personnel
        3.2.1 Under‑5 mortality rate
        3.2.2 Neonatal mortality rate
        3.3.1 Number of new HIV infections per 1,000 uninfected population, by sex, age and key populations
        3.3.2 Tuberculosis incidence per 100,000 population
        3.3.3 Malaria incidence per 1,000 population
        3.3.4 Hepatitis B incidence per 100,000 population
        3.3.5 Number of people requiring interventions against neglected tropical diseases
        3.4.1 Mortality rate attributed to cardiovascular disease, cancer, diabetes or chronic respiratory disease
        3.4.2 Suicide mortality rate
        3.5.1 Coverage of treatment interventions (pharmacological, psychosocial and rehabilitation and aftercare services) for substance use disorders
        3.5.2 Alcohol per capita consumption (aged 15 years and older) within a calendar year in litres of pure alcohol
        3.6.1 Death rate due to road traffic injuries
        3.7.1 Proportion of women of reproductive age (aged 15–49 years) who have their need for family planning satisfied with modern methods
        3.7.2 Adolescent birth rate (aged 10–14 years; aged 15–19 years) per 1,000 women in that age group
        3.8.1 Coverage of essential health services
        3.8.2 Proportion of population with large household expenditures on health as a share of total household expenditure or income
        3.9.1 Mortality rate attributed to household and ambient air pollution
        3.9.2 Mortality rate attributed to unsafe water, unsafe sanitation and lack of hygiene (exposure to unsafe Water, Sanitation and Hygiene for All (WASH) services)
        3.9.3 Mortality rate attributed to unintentional poisoning
        3.a.1 Age-standardized prevalence of current tobacco use among persons aged 15 years and older
        3.b.1 Proportion of the target population covered by all vaccines included in their national programme
        3.b.2 Total net official development assistance to medical research and basic health sectors
        3.b.3 Proportion of health facilities that have a core set of relevant essential medicines available and affordable on a sustainable basis
        3.c.1 Health worker density and distribution
        3.d.1 International Health Regulations (IHR) capacity and health emergency preparedness
        3.d.2 Percentage of bloodstream infections due to selected antimicrobial-resistant organisms


        Goal 4: Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all
        Targets:
        4.1 By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes
        4.2 By 2030, ensure that all girls and boys have access to quality early childhood development, care and pre‑primary education so that they are ready for primary education
        4.3 By 2030, ensure equal access for all women and men to affordable and quality technical, vocational and tertiary education, including university
        4.4 By 2030, substantially increase the number of youth and adults who have relevant skills, including technical and vocational skills, for employment, decent jobs and entrepreneurship
        4.5 By 2030, eliminate gender disparities in education and ensure equal access to all levels of education and vocational training for the vulnerable, including persons with disabilities, indigenous peoples and children in vulnerable situations
        4.6 By 2030, ensure that all youth and a substantial proportion of adults, both men and women, achieve literacy and numeracy
        4.7 By 2030, ensure that all learners acquire the knowledge and skills needed to promote sustainable development, including, among others, through education for sustainable development and sustainable lifestyles, human rights, gender equality, promotion of a culture of peace and non-violence, global citizenship and appreciation of cultural diversity and of culture's contribution to sustainable development
        4.a Build and upgrade education facilities that are child, disability and gender sensitive and provide safe, non-violent, inclusive and effective learning environments for all
        4.b By 2020, substantially expand globally the number of scholarships available to developing countries, in particular least developed countries, small island developing States and African countries, for enrolment in higher education, including vocational training and information and communications technology, technical, engineering and scientific programmes, in developed countries and other developing countries
        4.c By 2030, substantially increase the supply of qualified teachers, including through international cooperation for teacher training in developing countries, especially least developed countries and small island developing States

        Indicators:
        4.1.1 Proportion of children and young people (a) in grades 2/3; (b) at the end of primary; and (c) at the end of lower secondary achieving at least a minimum proficiency level in (i) reading and (ii) mathematics, by sex
        4.1.2 Completion rate (primary education, lower secondary education, upper secondary education)
        4.2.1 Proportion of children aged 24–59 months who are developmentally on track in health, learning and psychosocial well-being, by sex
        4.2.2 Participation rate in organized learning (one year before the official primary entry age), by sex
        4.3.1 Participation rate of youth and adults in formal and non-formal education and training in the previous 12 months, by sex
        4.4.1 Proportion of youth and adults with information and communications technology (ICT) skills, by type of skill
        4.5.1 Parity indices (female/male, rural/urban, bottom/top wealth quintile and others such as disability status, indigenous peoples and conflict-affected, as data become available) for all education indicators on this list that can be disaggregated
        4.6.1 Proportion of population in a given age group achieving at least a fixed level of proficiency in functional (a) literacy and (b) numeracy skills, by sex
        4.7.1 Extent to which (i) global citizenship education and (ii) education for sustainable development are mainstreamed in (a) national education policies; (b) curricula; (c) teacher education; and (d) student assessment
        4.a.1 Proportion of schools offering basic services, by type of service
        4.b.1 Volume of official development assistance flows for scholarships by sector and type of study
        4.c.1 Proportion of teachers with the minimum required qualifications, by education level

        Goal 5: Achieve gender equality and empower all women and girls
        Targets:
        5.1 End all forms of discrimination against all women and girls everywhere
        5.2 Eliminate all forms of violence against all women and girls in the public and private spheres, including trafficking and sexual and other types of exploitation
        5.3 Eliminate all harmful practices, such as child, early and forced marriage and female genital mutilation
        5.4 Recognize and value unpaid care and domestic work through the provision of public services, infrastructure and social protection policies and the promotion of shared responsibility within the household and the family as nationally appropriate
        5.5 Ensure women's full and effective participation and equal opportunities for leadership at all levels of decision-making in political, economic and public life
        5.6 Ensure universal access to sexual and reproductive health and reproductive rights as agreed in accordance with the Programme of Action of the International Conference on Population and Development and the Beijing Platform for Action and the outcome documents of their review conferences
        5.a Undertake reforms to give women equal rights to economic resources, as well as access to ownership and control over land and other forms of property, financial services, inheritance and natural resources, in accordance with national laws
        5.b Enhance the use of enabling technology, in particular information and communications technology, to promote the empowerment of women
        5.c Adopt and strengthen sound policies and enforceable legislation for the promotion of gender equality and the empowerment of all women and girls at all levels

        Indicators:
        5.1.1 Whether or not legal frameworks are in place to promote, enforce and monitor equality and non‑discrimination on the basis of sex
        5.2.1 Proportion of ever-partnered women and girls aged 15 years and older subjected to physical, sexual or psychological violence by a current or former intimate partner in the previous 12 months, by form of violence and by age
        5.2.2 Proportion of women and girls aged 15 years and older subjected to sexual violence by persons other than an intimate partner in the previous 12 months, by age and place of occurrence
        5.3.1 Proportion of women aged 20–24 years who were married or in a union before age 15 and before age 18
        5.3.2 Proportion of girls and women aged 15–49 years who have undergone female genital mutilation/cutting, by age
        5.4.1 Proportion of time spent on unpaid domestic and care work, by sex, age and location
        5.5.1 Proportion of seats held by women in (a) national parliaments and (b) local governments
        5.5.2 Proportion of women in managerial positions
        5.6.1 Proportion of women aged 15–49 years who make their own informed decisions regarding sexual relations, contraceptive use and reproductive health care
        5.6.2 Number of countries with laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education
        5.a.1 (a) Proportion of total agricultural population with ownership or secure rights over agricultural land, by sex; and (b) share of women among owners or rights-bearers of agricultural land, by type of tenure
        5.a.2 Proportion of countries where the legal framework (including customary law) guarantees women's equal rights to land ownership and/or control
        5.b.1 Proportion of individuals who own a mobile telephone, by sex
        5.c.1 Proportion of countries with systems to track and make public allocations for gender equality and women's empowerment

        Here are the details of the AI system:

        Domain: "{}",
        Purpose: "{}",
        Capability: "{}",
        Sensing instrument and location: "{}",
        AI User: "{}",
        AI Subject: "{}"

         Please return the assessment in the following format:
         {{
           "Description": "The AI system intended to be used ...",
           "Targets Supported for SDG [SDG Number1]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number1]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number1]": "[Explanation]",
           "Targets Supported for SDG [SDG Number2]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number2]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number2]": "[Explanation]",
           "Targets Supported for SDG [SDG Number3]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number3]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number3]": "[Explanation]",
           "Targets Supported for SDG [SDG Number4]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number4]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number4]": "[Explanation]",
           "Targets Supported for SDG [SDG Number5]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number5]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number5]": "[Explanation]"
         }}
            """
    }
]



def format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject):
    S = "test {}"
    messages = deepcopy(MESSAGES)
    messages[1]['content'] = messages[1]['content'].format(domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)
    return messages

FULL_RES = []
cost = 0

start_time = time.time()
i = 0
for useElements in prompt_result:
  useI = str(useElements['Use'])
  # if int(useI) > 4:
  #   continue
  print (f" Parsing use {useI}")

  # Variables for message placeholders
  domain = useElements['Domain']
  purpose = useElements['Purpose']
  aiCapability = useElements['Capability']
  sensingInstrument = useElements['Sensing instrument and location']
  aiUser = useElements['AI User']
  aiSubject = useElements['AI Subject']

  # Extracting "Use i" details
  use_i_details = [domain, purpose, aiCapability, sensingInstrument, aiUser, aiSubject]

  # adapt the prompt for useI
  messages = format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)

  # run the prompt
  response = get_completion_from_messages(messages, temperature=0)
  print(response)

  # response, token_count = get_completion_and_token_count(messages, temperature=0)
  # res = token_count
  # cost_chunk = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
  # cost += cost_chunk

  response = ast.literal_eval(response)

  # print(response)

  # combine the useI and the risk report
  combined_response = {}
  combined_response["id"]= useI
  combined_response["Details"] = use_i_details
  for k, v in response.items():
    combined_response[k] = v
  print (combined_response)

  # save result
  # with open(f"{useI}_risk_report_full.json", "w") as json_file:
  #     json.dump(combined_response, json_file, indent=4)  # 4 spaces of indentation
  # # Download the file to your local machine
  # files.download(f"{useI}_risk_report_full.json")

  FULL_RES.append(combined_response)

  time.sleep(44)

  i+=1
  # print(i)
  # UNCOMMENT FOR RUNNING FOR 3 uses only
  # if i==25:
  #   break

FULL_RES_part1 = FULL_RES.copy()

###############################
# save result
with open(f"FULL_SDG_REPORT_MohileHCI_part1.json", "w") as json_file:
    json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# Download the file to your local machine
files.download(f"FULL_SDG_REPORT_MohileHCI_part1.json")





"""# PART 2 PROMPT : SDGs 6-11"""

# Assuming you have the variables domain, purpose, aiCapability, aiUser, and aiSubject defined with appropriate values

MESSAGES = [
    {
        'role': 'system',
        'content': """You are a renowned specialist in the field of mobile and wearable technology with a dedicated focus on understanding, promoting, and implementing the Sustainable Development Goals (SDGs). With your vast experience, decisiveness, and conscientious approach, you have a deep understanding of how mobile and wearable technologies can be leveraged to support the SDGs.
        You possess comprehensive knowledge of the List of Sustainable Development Goal targets and indicators, which encapsulates all targets and indicators for the 17 SDGs. This global framework was meticulously crafted by the Inter-Agency and Expert Group on SDG Indicators (IAEG-SDGs) and was ratified during the 48th session of the United Nations Statistical Commission in March 2017.
        The framework you reference encompasses all subsequent refinements to the official indicator list."""
    },
    {
        'role': 'user',
        'content': """

        Assess the AI system's alignment with the Sustainable Development Goals (SDGs).

        Follow the streamlined steps below:
        1. Describe the AI System: Craft a concise description of the AI system, ensuring it parallels the phrasing used in the Sustainable Development Goal targets and indicators. Your description should begin with "The AI system is designed to..." and should be encapsulated within two sentences.
        2. Evaluate Each SDG:
            For each of the 3 given SDGs, assess if the AI system aligns with or supports the respective SDG. Reference the exact text from the SDG targets and indicators and provide a thorough rationale.
            Rigorously validate your reasoning. The true intent and capabilities of the AI system are crucial for this evaluation. Ensure there is a direct correlation between the system's functionalities and the referenced indicators.
        3. Reference Targets & Indicators: While evaluating, explicitly cite the SDG targets and indicators that resonate most with the AI system's purpose and capabilities.
        4. Classify Non-relevant SDGs: If the AI system does not align with a particular SDG, label it as "Not Relevant" for that SDG.

        Remember, precision is paramount. It's vital to make informed and accurate determinations regarding the AI system's alignment with each SDG. Ensure all SDG targets and indicators are meticulously considered during your assessment.

        Goal 6: Ensure availability and sustainable management of water and sanitation for all
        Targets:
        6.1 By 2030, achieve universal and equitable access to safe and affordable drinking water for all
        6.2 By 2030, achieve access to adequate and equitable sanitation and hygiene for all and end open defecation, paying special attention to the needs of women and girls and those in vulnerable situations
        6.3 By 2030, improve water quality by reducing pollution, eliminating dumping and minimizing release of hazardous chemicals and materials, halving the proportion of untreated wastewater and substantially increasing recycling and safe reuse globally
        6.4 By 2030, substantially increase water-use efficiency across all sectors and ensure sustainable withdrawals and supply of freshwater to address water scarcity and substantially reduce the number of people suffering from water scarcity
        6.5 By 2030, implement integrated water resources management at all levels, including through transboundary cooperation as appropriate
        6.6 By 2020, protect and restore water-related ecosystems, including mountains, forests, wetlands, rivers, aquifers, and lakes
        6.a By 2030, expand international cooperation and capacity-building support to developing countries in water- and sanitation-related activities and programmes, including water harvesting, desalination, water efficiency, wastewater treatment, recycling, and reuse technologies
        6.b Support and strengthen the participation of local communities in improving water and sanitation management

        Indicators:
        6.1.1 Proportion of population using safely managed drinking water services
        6.2.1 Proportion of population using (a) safely managed sanitation services and (b) a handwashing facility with soap and water
        6.3.1 Proportion of domestic and industrial wastewater flows safely treated
        6.3.2 Proportion of bodies of water with good ambient water quality
        6.4.1 Change in water-use efficiency over time
        6.4.2 Level of water stress: freshwater withdrawal as a proportion of available freshwater resources
        6.5.1 Degree of integrated water resources management
        6.5.2 Proportion of transboundary basin area with an operational arrangement for water cooperation
        6.6.1 Change in the extent of water-related ecosystems over time
        6.a.1 Amount of water- and sanitation-related official development assistance that is part of a government-coordinated spending plan
        6.b.1 Proportion of local administrative units with established and operational policies and procedures for participation of local communities in water and sanitation management


        Goal 7: Ensure access to affordable, reliable, sustainable and modern energy for all
        Targets:
        7.1 By 2030, ensure universal access to affordable, reliable, and modern energy services
        7.2 By 2030, increase substantially the share of renewable energy in the global energy mix
        7.3 By 2030, double the global rate of improvement in energy efficiency
        7.a By 2030, enhance international cooperation to facilitate access to clean energy research and technology, including renewable energy, energy efficiency, and advanced and cleaner fossil-fuel technology, and promote investment in energy infrastructure and clean energy technology
        7.b By 2030, expand infrastructure and upgrade technology for supplying modern and sustainable energy services for all in developing countries, in particular least developed countries, small island developing States, and landlocked developing countries, in accordance with their respective programs of support

        Indicators:
        7.1.1 Proportion of population with access to electricity
        7.1.2 Proportion of population with primary reliance on clean fuels and technology
        7.2.1 Renewable energy share in the total final energy consumption
        7.3.1 Energy intensity measured in terms of primary energy and GDP
        7.a.1 International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems
        7.b.1 Installed renewable energy-generating capacity in developing countries (in watts per capita)

        Goal 8: Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all
        Targets:
        8.1 Sustain per capita economic growth in accordance with national circumstances and, in particular, at least 7 per cent gross domestic product growth per annum in the least developed countries.
        8.2 Achieve higher levels of economic productivity through diversification, technological upgrading, and innovation, including through a focus on high-value added and labor-intensive sectors.
        8.3 Promote development-oriented policies that support productive activities, decent job creation, entrepreneurship, creativity and innovation, and encourage the formalization and growth of micro-, small- and medium-sized enterprises, including through access to financial services.
        8.4 Improve progressively, through 2030, global resource efficiency in consumption and production and endeavor to decouple economic growth from environmental degradation, in accordance with the 10‑Year Framework of Programmes on Sustainable Consumption and Production, with developed countries taking the lead.
        8.5 By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value.
        8.6 By 2020, substantially reduce the proportion of youth not in employment, education, or training.
        8.7 Take immediate and effective measures to eradicate forced labor, end modern slavery and human trafficking and secure the prohibition and elimination of the worst forms of child labor, including recruitment and use of child soldiers, and by 2025 end child labor in all its forms.
        8.8 Protect labor rights and promote safe and secure working environments for all workers, including migrant workers, in particular, women migrants, and those in precarious employment.
        8.9 By 2030, devise and implement policies to promote sustainable tourism that creates jobs and promotes local culture and products.
        8.10 Strengthen the capacity of domestic financial institutions to encourage and expand access to banking, insurance, and financial services for all.
        8.a Increase Aid for Trade support for developing countries, in particular, least-developed countries, including through the Enhanced Integrated Framework for Trade-related Technical Assistance to Least Developed Countries.
        8.b By 2020, develop and operationalize a global strategy for youth employment and implement the Global Jobs Pact of the International Labour Organization.

        Indicators:
        8.1.1 Annual growth rate of real GDP per capita
        8.2.1 Annual growth rate of real GDP per employed person
        8.3.1 Proportion of informal employment in total employment, by sector and sex
        8.4.1 Material footprint, material footprint per capita, and material footprint per GDP
        8.4.2 Domestic material consumption, domestic material consumption per capita, and domestic material consumption per GDP
        8.5.1 Average hourly earnings of employees, by sex, age, occupation, and persons with disabilities
        8.5.2 Unemployment rate, by sex, age, and persons with disabilities
        8.6.1 Proportion of youth (aged 15–24 years) not in education, employment, or training
        8.7.1 Proportion and number of children aged 5–17 years engaged in child labor, by sex and age
        8.8.1 Fatal and non-fatal occupational injuries per 100,000 workers, by sex and migrant status
        8.8.2 Level of national compliance with labor rights (freedom of association and collective bargaining) based on International Labour Organization (ILO) textual sources and national legislation, by sex and migrant status
        8.9.1 Tourism direct GDP as a proportion of total GDP and in growth rate
        8.10.1 (a) Number of commercial bank branches per 100,000 adults and (b) number of automated teller machines (ATMs) per 100,000 adults
        8.10.2 Proportion of adults (15 years and older) with an account at a bank or other financial institution or with a mobile-money-service provider
        8.a.1 Aid for Trade commitments and disbursements
        8.b.1 Existence of a developed and operationalized national strategy for youth employment, as a distinct strategy or as part of a national employment strategy.


        Goal 9: Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation
        Targets:
        9.1 Develop quality, reliable, sustainable, and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being, with a focus on affordable and equitable access for all.
        9.2 Promote inclusive and sustainable industrialization and, by 2030, significantly raise the industry's share of employment and gross domestic product, in line with national circumstances, and double its share in least-developed countries.
        9.3 Increase the access of small-scale industrial and other enterprises, especially in developing countries, to financial services, including affordable credit, and their integration into value chains and markets.
        9.4 By 2030, upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency and greater adoption of clean and environmentally sound technologies and industrial processes, with all countries taking action in accordance with their respective capabilities.
        9.5 Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, especially developing countries, including, by 2030, encouraging innovation and substantially increasing the number of research and development workers per 1 million people and public and private research and development spending.
        9.a Facilitate sustainable and resilient infrastructure development in developing countries through enhanced financial, technological, and technical support to African countries, least-developed countries, landlocked developing countries, and small island developing States.
        9.b Support domestic technology development, research, and innovation in developing countries, including by ensuring a conducive policy environment for, among other things, industrial diversification and value addition to commodities.
        9.c Significantly increase access to information and communications technology and aim to provide universal and affordable access to the Internet in least-developed countries by 2020.

        Indicators:
        9.1.1 Proportion of the rural population who live within 2 km of an all-season road
        9.1.2 Passenger and freight volumes, by mode of transport
        9.2.1 Manufacturing value added as a proportion of GDP and per capita
        9.2.2 Manufacturing employment as a proportion of total employment
        9.3.1 Proportion of small-scale industries in total industry value added
        9.3.2 Proportion of small-scale industries with a loan or line of credit
        9.4.1 CO2 emission per unit of value added
        9.5.1 Research and development expenditure as a proportion of GDP
        9.5.2 Researchers (in full-time equivalent) per million inhabitants
        9.a.1 Total official international support (official development assistance plus other official flows) to infrastructure
        9.b.1 Proportion of medium and high-tech industry value added in total value added
        9.c.1 Proportion of the population covered by a mobile network, by technology.

        Goal 10: Reduce inequality within and among countries
        Targets:
        10.1 By 2030, progressively achieve and sustain income growth of the bottom 40 per cent of the population at a rate higher than the national average.
        10.2 By 2030, empower and promote the social, economic, and political inclusion of all, irrespective of age, sex, disability, race, ethnicity, origin, religion, or economic or other status.
        10.3 Ensure equal opportunity and reduce inequalities of outcome, including by eliminating discriminatory laws, policies, and practices and promoting appropriate legislation, policies, and action.
        10.4 Adopt policies, especially fiscal, wage, and social protection policies, and progressively achieve greater equality.
        10.5 Improve the regulation and monitoring of global financial markets and institutions and strengthen their implementation.
        10.6 Ensure enhanced representation and voice for developing countries in decision-making in global international economic and financial institutions.
        10.7 Facilitate orderly, safe, regular, and responsible migration and mobility of people, including through well-managed migration policies.
        10.a Implement special and differential treatment for developing countries, particularly least developed countries, according to World Trade Organization agreements.
        10.b Encourage official development assistance and financial flows to States where the need is greatest.
        10.c By 2030, reduce the transaction costs of migrant remittances to less than 3 per cent and eliminate remittance corridors with costs higher than 5 per cent.

        Indicators:
        10.1.1 Growth rates of household expenditure or income per capita among the bottom 40 per cent and the total population
        10.2.1 Proportion of people living below 50 per cent of median income
        10.3.1 Proportion of the population reporting discrimination or harassment based on grounds prohibited under international human rights law
        10.4.1 Labour share of GDP
        10.4.2 Redistributive impact of fiscal policy
        10.5.1 Financial Soundness Indicators
        10.6.1 Proportion of members and voting rights of developing countries in international organizations
        10.7.1 Recruitment cost borne by employee relative to monthly income earned in the country of destination
        10.7.2 Number of countries with policies that facilitate orderly, safe, regular, and responsible migration
        10.7.3 Number of people who died or disappeared during migration towards an international destination
        10.7.4 Proportion of the population who are refugees, by country of origin
        10.a.1 Proportion of tariff lines applied to imports from least developed countries and developing countries with zero-tariff
        10.b.1 Total resource flows for development, by recipient and donor countries and type of flow
        10.c.1 Remittance costs as a proportion of the amount remitted.


        Goal 11: Make cities and human settlements inclusive, safe, resilient and sustainable
        Targets:
        11.1 By 2030, ensure access for all to adequate, safe, and affordable housing and basic services, and upgrade slums.
        11.2 By 2030, provide access to safe, affordable, accessible, and sustainable transport systems for all, with attention to vulnerable populations.
        11.3 By 2030, promote sustainable urbanization and the ability for inclusive urban planning in all countries.
        11.4 Strengthen efforts to protect the world's cultural and natural heritage.
        11.5 By 2030, substantially reduce the impacts and losses caused by disasters, especially for the vulnerable.
        11.6 By 2030, decrease the negative environmental impacts of cities, focusing on air quality and waste management.
        11.7 By 2030, ensure access for all to safe and inclusive public spaces.
        11.a Strengthen connections between urban and rural areas through development planning.
        11.b By 2020, increase the number of settlements with holistic policies for climate change, resilience, and disaster risk management.
        11.c Support least developed countries in sustainable building practices.

        Indicators:
        11.1.1 Proportion of urban population living in slums or inadequate housing
        11.2.1 Proportion of population with access to public transport, considering demographics
        11.3.1 Rate of land consumption relative to population growth
        11.3.2 Proportion of cities with democratic civil society participation in urban planning
        11.4.1 Per capita spending on the preservation of cultural and natural heritage
        11.5.1 Disaster-related deaths, missing persons, and affected persons per 100,000 population
        11.5.2 Economic losses from disasters in relation to global GDP and disruptions to services
        11.6.1 Proportion of municipal waste managed in controlled facilities by cities
        11.6.2 Annual mean levels of fine particulate matter in cities (e.g., PM2.5, PM10)
        11.7.1 Share of city areas that are open spaces accessible to the public, considering demographics
        11.7.2 Proportion of people who experienced harassment in the last 12 months, considering demographics
        11.a.1 Number of countries with urban or regional plans addressing population dynamics, territorial development, and local fiscal considerations
        11.b.1 Number of countries with national disaster risk reduction strategies in line with the Sendai Framework
        11.b.2 Proportion of local governments with disaster risk reduction strategies in alignment with national strategies
        For 11.c, no suitable replacement indicator was proposed by 2020, and further development is encouraged for a comprehensive review in 2025.


        Here are the details of the AI system:

        Domain: "{}",
        Purpose: "{}",
        Capability: "{}",
        Sensing instrument and location: "{}",
        AI User: "{}",
        AI Subject: "{}"

         Please return the assessment in the following format:
         {{
           "Description": "The AI system intended to be used ...",
           "Targets Supported for SDG [SDG Number6]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number6]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number6]": "[Explanation]",
           "Targets Supported for SDG [SDG Number7]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number7]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number7]": "[Explanation]",
           "Targets Supported for SDG [SDG Number8]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number8]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number8]": "[Explanation]",
           "Targets Supported for SDG [SDG Number9]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number9]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number9]": "[Explanation]",
           "Targets Supported for SDG [SDG Number10]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number10]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number10]": "[Explanation]",
           "Targets Supported for SDG [SDG Number11]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number11]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number11]": "[Explanation]",
         }}
            """
    }
]



def format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject):
    S = "test {}"
    messages = deepcopy(MESSAGES)
    messages[1]['content'] = messages[1]['content'].format(domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)
    return messages



FULL_RES = []
cost = 0

start_time = time.time()
i = 0
for useElements in prompt_result:
  useI = str(useElements['Use'])
  # if int(useI) < 114:
  #   continue
  print (f" Parsing use {useI}")

  # Variables for message placeholders
  domain = useElements['Domain']
  purpose = useElements['Purpose']
  aiCapability = useElements['Capability']
  sensingInstrument = useElements['Sensing instrument and location']
  aiUser = useElements['AI User']
  aiSubject = useElements['AI Subject']

  # Extracting "Use i" details
  use_i_details = [domain, purpose, aiCapability, sensingInstrument, aiUser, aiSubject]

  # adapt the prompt for useI
  messages = format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)

  # run the prompt
  response = get_completion_from_messages(messages, temperature=0)
  # print(response)

  # response, token_count = get_completion_and_token_count(messages, temperature=0)
  # res = token_count
  # cost_chunk = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
  # cost += cost_chunk

  response = ast.literal_eval(response)

  # print(response)

  # combine the useI and the risk report
  combined_response = {}
  combined_response["id"]= useI
  combined_response["Details"] = use_i_details
  for k, v in response.items():
    combined_response[k] = v
  pprint.pprint (combined_response)

  # save result
  # with open(f"{useI}_risk_report_full.json", "w") as json_file:
  #     json.dump(combined_response, json_file, indent=4)  # 4 spaces of indentation
  # # Download the file to your local machine
  # files.download(f"{useI}_risk_report_full.json")

  FULL_RES.append(combined_response)

  time.sleep(33)

  i+=1
  # print(i)
  # UNCOMMENT FOR RUNNING FOR 3 uses only
  # if i==25:
  #   break

FULL_RES_part2 = FULL_RES.copy()

###############################
# save result
# with open(f"FULL_SDG_REPORT_EO.json", "w") as json_file:
#     json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# # Download the file to your local machine
# files.download(f"FULL_SDG_REPORT_EO.json")
# end_time = time.time()

# print(f"Execution time: {end_time - start_time:.5f} seconds")
# print (f"TOTAL COST {cost}")



###############################
# save result
with open(f"FULL_SDG_REPORT_MobileHCI_part2.json", "w") as json_file:
    json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# Download the file to your local machine
files.download(f"FULL_SDG_REPORT_MobileHCI_part2.json")





"""# PART 3 PROMPT : SDGs 12-17"""

# Assuming you have the variables domain, purpose, aiCapability, aiUser, and aiSubject defined with appropriate values

MESSAGES = [
    {
        'role': 'system',
        'content': """You are a renowned specialist in the field of mobile and wearable technology with a dedicated focus on understanding, promoting, and implementing the Sustainable Development Goals (SDGs). With your vast experience, decisiveness, and conscientious approach, you have a deep understanding of how mobile and wearable technologies can be leveraged to support the SDGs.
        You possess comprehensive knowledge of the List of Sustainable Development Goal targets and indicators, which encapsulates all targets and indicators for the 17 SDGs. This global framework was meticulously crafted by the Inter-Agency and Expert Group on SDG Indicators (IAEG-SDGs) and was ratified during the 48th session of the United Nations Statistical Commission in March 2017.
        The framework you reference encompasses all subsequent refinements to the official indicator list."""
    },
    {
        'role': 'user',
        'content': """

        Assess the AI system's alignment with the Sustainable Development Goals (SDGs).

        Follow the streamlined steps below:
        1. Describe the AI System: Craft a concise description of the AI system, ensuring it parallels the phrasing used in the Sustainable Development Goal targets and indicators. Your description should begin with "The AI system is designed to..." and should be encapsulated within two sentences.
        2. Evaluate Each SDG:
            For each of the 3 given SDGs, assess if the AI system aligns with or supports the respective SDG. Reference the exact text from the SDG targets and indicators and provide a thorough rationale.
            Rigorously validate your reasoning. The true intent and capabilities of the AI system are crucial for this evaluation. Ensure there is a direct correlation between the system's functionalities and the referenced indicators.
        3. Reference Targets & Indicators: While evaluating, explicitly cite the SDG targets and indicators that resonate most with the AI system's purpose and capabilities.
        4. Classify Non-relevant SDGs: If the AI system does not align with a particular SDG, label it as "Not Relevant" for that SDG.

        Remember, precision is paramount. It's vital to make informed and accurate determinations regarding the AI system's alignment with each SDG. Ensure all SDG targets and indicators are meticulously considered during your assessment.

        Goal 12: Ensure sustainable consumption and production patterns
        Targets:
        12.1 Implementation of sustainable consumption and production patterns.
        12.2 Sustainable management and efficient use of natural resources by 2030.
        12.3 Halve global food waste at the retail and consumer levels and reduce food losses by 2030.
        12.4 Sound management of chemicals and wastes by 2020.
        12.5 Reduce waste generation through prevention, recycling, and reuse by 2030.
        12.6 Encourage companies, especially large ones, to adopt sustainable practices and reporting.
        12.7 Promote sustainable public procurement practices.
        12.8 Enhance public awareness and information for sustainable development by 2030.
        12.a Support developing countries in scientific and tech capacity for sustainable consumption and production.
        12.b Monitor sustainable tourism impacts that promote jobs and local culture.
        12.c Rationalize fossil fuel subsidies to discourage wasteful consumption.

        Indicators:
        12.1.1 Countries adopting sustainable consumption and production policies.
        12.2.1 Material footprint measurements.
        12.2.2 Domestic material consumption metrics.
        12.3.1 Food loss and waste indices.
        12.4.1 Parties adhering to environmental agreements on hazardous waste and chemicals.
        12.4.2 Metrics on hazardous waste generation and treatment.
        12.5.1 National recycling rates.
        12.6.1 Companies publishing sustainability reports.
        12.7.1 Implementation of sustainable public procurement policies.
        12.8.1 Integration of global citizenship and sustainability education into national systems.
        12.a.1 Renewable energy capacity in developing countries.
        12.b.1 Use of standard tools for monitoring tourism sustainability.
        12.c.1 Fossil-fuel subsidies per GDP unit.

        Goal 13: Take urgent action to combat climate change and its impacts
        Targets:
        13.1 Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters in all countries.
        13.2 Integrate climate change measures into national policies, strategies and planning.
        13.3 Improve education, awareness-raising, and capacity on climate change mitigation, adaptation, impact reduction, and early warning.
        13.a Commitment by developed-country parties to mobilize $100 billion annually by 2020 for developing countries and operationalize the Green Climate Fund.
        13.b Raise capacity for climate change-related planning in least developed countries and small island developing States, emphasizing women, youth, and marginalized communities.

        Indicators:
        13.1.1 Number of deaths, missing persons, and affected persons attributed to disasters per 100,000 population.
        13.1.2 Countries adopting national disaster risk reduction strategies in line with the Sendai Framework for Disaster Risk Reduction 2015–2030.
        13.1.3 Local governments adopting disaster risk reduction strategies aligned with national strategies.
        13.2.1 Countries with nationally determined contributions, strategies, and plans related to climate change.
        13.2.2 Total annual greenhouse gas emissions.
        13.3.1 Integration of global citizenship and sustainability education into national education systems.
        13.a.1 USD amounts mobilized annually towards the $100 billion commitment through to 2025.
        13.b.1 Number of least developed countries and small island developing States with climate change contributions, strategies, and plans.

        Goal 14: Conserve and sustainably use the oceans, seas and marine resources for sustainable development
        Targets:
        14.1 By 2025, prevent and significantly reduce marine pollution of all kinds, particularly from land-based activities.
        14.2 By 2020, sustainably manage marine and coastal ecosystems to prevent adverse impacts and enhance resilience.
        14.3 Address the impacts of ocean acidification through enhanced scientific cooperation.
        14.4 By 2020, regulate harvesting, end overfishing and illegal practices, and restore fish stocks.
        14.5 By 2020, conserve at least 10% of coastal and marine areas based on scientific information.
        14.6 By 2020, prohibit harmful fisheries subsidies and combat illegal, unreported, and unregulated fishing.
        14.7 By 2030, enhance economic benefits from sustainable marine resources for small island states and least developed countries.
        14.a Increase scientific knowledge, research capacity, and technology transfer regarding marine biodiversity.
        14.b Provide access for small-scale artisanal fishers to marine resources and markets.
        14.c Implement international law for the conservation and sustainable use of oceans.

        Indicators:
        14.1.1 Coastal eutrophication index and plastic debris density.
        14.2.1 Countries using ecosystem-based approaches for marine management.
        14.3.1 Average marine acidity (pH) at selected sampling stations.
        14.4.1 Proportion of fish stocks within biologically sustainable levels.
        14.5.1 Coverage of protected marine areas.
        14.6.1 Implementation of international instruments to combat illegal fishing.
        14.7.1 Sustainable fisheries' contribution to GDP in selected countries.
        14.a.1 Research budget allocation to marine technology.
        14.b.1 Framework protecting access rights for small-scale fisheries.
        14.c.1 Countries progressing in the implementation of ocean-related international law.

        Goal 15: Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss
        Targets:
        15.1 By 2020, conserve and sustainably use terrestrial and inland freshwater ecosystems.
        15.2 By 2020, promote sustainable forest management, halt deforestation, and increase afforestation and reforestation.
        15.3 By 2030, combat desertification and achieve a land degradation-neutral world.
        15.4 By 2030, conserve mountain ecosystems and their biodiversity.
        15.5 Take action to reduce habitat degradation, halt biodiversity loss, and protect threatened species by 2020.
        15.6 Ensure fair sharing of benefits from genetic resources.
        15.7 Take urgent action against poaching and illegal wildlife trafficking.
        15.8 By 2020, prevent the adverse impact of invasive alien species.
        15.9 By 2020, integrate ecosystem and biodiversity values into planning and development processes.
        15.a Increase financial resources for conserving and using biodiversity and ecosystems sustainably.
        15.b Mobilize resources for sustainable forest management, including conservation and reforestation.
        15.c Enhance global support against poaching and trafficking of protected species.

        Indicators:
        15.1.1 Forest area proportion of total land area.
        15.1.2 Protected areas covering important terrestrial and freshwater biodiversity sites.
        15.2.1 Progress towards sustainable forest management.
        15.3.1 Proportion of degraded land.
        15.4.1 Protected areas covering important mountain biodiversity sites.
        15.4.2 Mountain Green Cover Index.
        15.5.1 Red List Index.
        15.6.1 Countries adopting frameworks for fair benefits sharing from genetic resources.
        15.7.1 Proportion of traded wildlife that was illicitly trafficked.
        15.8.1 Countries adopting legislation against invasive alien species.
        15.9.1 Countries integrating biodiversity into national planning and reporting.
        15.a.1 Financial resources for biodiversity conservation and sustainable use.
        15.b.1 Financial resources for sustainable forest management.
        15.c.1 Proportion of traded wildlife that was illicitly trafficked.

        Goal 16: Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels
        Targets:
        16.1 Reduce violence and related death rates.
        16.2 End violence against children including abuse, exploitation, trafficking, and torture.
        16.3 Promote rule of law and ensure equal access to justice.
        16.4 Reduce illicit financial and arms flows, and combat organized crime by 2030.
        16.5 Substantially reduce corruption and bribery.
        16.6 Develop accountable and transparent institutions.
        16.7 Ensure inclusive and participatory decision-making.
        16.8 Strengthen participation of developing countries in global governance.
        16.9 Provide legal identity for all, including birth registration by 2030.
        16.10 Ensure public access to information and protect fundamental freedoms.
        16.a Strengthen institutions to prevent violence and combat terrorism and crime.
        16.b Enforce non-discriminatory laws and policies for sustainable development.

        Indicators:
        16.1.1 Intentional homicide victims per 100,000 population.
        16.1.2 Conflict-related deaths per 100,000 population.
        16.1.3 Population subjected to physical, psychological, or sexual violence in the past year.
        16.1.4 Population feeling safe in their area.
        16.2.1 Children experiencing punishment or aggression by caregivers.
        16.2.2 Victims of human trafficking per 100,000 population.
        16.2.3 Young adults experiencing sexual violence by age 18.
        16.3.1 Victims reporting their victimization.
        16.3.2 Unsentenced detainees in prison population.
        16.3.3 Population accessing dispute resolution mechanisms.
        16.4.1 Value of illicit financial flows.
        16.4.2 Tracing of seized or found arms.
        16.5.1 Persons paying bribes to public officials.
        16.5.2 Businesses paying bribes to public officials.
        16.6.1 Government expenditures vs. approved budget.
        16.6.2 Population satisfaction with public services.
        16.7.1 Positions in national/local institutions by demographic.
        16.7.2 Population believing in inclusive and responsive decision-making.
        16.8.1 Membership and voting rights of developing countries in international organizations.
        16.9.1 Children under 5 with registered births.
        16.10.1 Cases against journalists, media personnel, trade unionists, and human rights advocates.
        16.10.2 Countries adopting guarantees for public access to information.
        16.a.1 Existence of national human rights institutions.
        16.b.1 Population reporting discrimination or harassment.

        Goal 17: Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development
        Targets:
        17.1 Strengthen domestic resource mobilization, including through international support to developing countries, to improve domestic capacity for tax and other revenue collection
        17.2 Developed countries to implement fully their official development assistance commitments, including the commitment by many developed countries to achieve the target of 0.7 per cent of gross national income for official development assistance (ODA/GNI) to developing countries and 0.15 to 0.20 per cent of ODA/GNI to least developed countries; ODA providers are encouraged to consider setting a target to provide at least 0.20 per cent of ODA/GNI to least developed countries
        17.3 Mobilize additional financial resources for developing countries from multiple sources
        17.4 Assist developing countries in attaining long-term debt sustainability through coordinated policies aimed at fostering debt financing, debt relief and debt restructuring, as appropriate, and address the external debt of highly indebted poor countries to reduce debt distress
        17.5 Adopt and implement investment promotion regimes for least developed countries
        17.6 Enhance North-South, South-South and triangular regional and international cooperation on and access to science, technology and innovation and enhance knowledge-sharing on mutually agreed terms, including through improved coordination among existing mechanisms, in particular at the United Nations level, and through a global technology facilitation mechanism
        17.7 Promote the development, transfer, dissemination and diffusion of environmentally sound technologies to developing countries on favourable terms, including on concessional and preferential terms, as mutually agreed
        17.8 Fully operationalize the technology bank and science, technology and innovation capacity-building mechanism for least developed countries by 2017 and enhance the use of enabling technology, in particular information and communications technology
        17.9 Enhance international support for implementing effective and targeted capacity-building in developing countries to support national plans to implement all the Sustainable Development Goals, including through north–south, South-South and triangular cooperation
        17.10 Promote a universal, rules-based, open, non‑discriminatory and equitable multilateral trading system under the World Trade Organization, including through the conclusion of negotiations under its Doha Development Agenda
        17.11 Significantly increase the exports of developing countries, in particular with a view to doubling the least developed countries’ share of global exports by 2020
        17.12 Realize timely implementation of duty-free and quota-free market access on a lasting basis for all least developed countries, consistent with World Trade Organization decisions, including by ensuring that preferential rules of origin applicable to imports from least developed countries are transparent and simple, and contribute to facilitating market access
        17.13 Enhance global macroeconomic stability, including through policy coordination and policy coherence
        17.14 Enhance policy coherence for sustainable development
        17.15 Respect each country's policy space and leadership to establish and implement policies for poverty eradication and sustainable development
        17.16 Enhance the Global Partnership for Sustainable Development, complemented by multi-stakeholder partnerships that mobilize and share knowledge, expertise, technology and financial resources, to support the achievement of the Sustainable Development Goals in all countries, in particular developing countries
        17.17 Encourage and promote effective public, public-private and civil society partnerships, building on the experience and resourcing strategies of partnerships
        17.18 By 2020, enhance capacity-building support to developing countries, including for least developed countries and small island developing States, to increase significantly the availability of high-quality, timely and reliable data disaggregated by income, gender, age, race, ethnicity, migratory status, disability, geographic location and other characteristics relevant in national contexts
        17.19 By 2030, build on existing initiatives to develop measurements of progress on sustainable development that complement gross domestic product, and support statistical capacity-building in developing countries

        Indicators:
        17.1.1 Total government revenue as a proportion of GDP, by source
        17.1.2 Proportion of domestic budget funded by domestic taxes
        17.2.1 Net official development assistance, total and to least developed countries, as a proportion of the Organization for Economic Cooperation and Development (OECD) Development Assistance Committee donors’ gross national income (GNI)
        17.3.1 Foreign direct investment, official development assistance and South-South cooperation as a proportion of gross national income
        17.3.2 Volume of remittances (in United States dollars) as a proportion of total GDP
        17.4.1 Debt service as a proportion of exports of goods and services
        17.5.1 Number of countries that adopt and implement investment promotion regimes for developing countries, including the least developed countries
        17.6.1 Fixed Internet broadband subscriptions per 100 inhabitants, by speed[n 28]
        17.7.1 Total amount of funding for developing countries to promote the development, transfer, dissemination and diffusion of environmentally sound technologies
        17.8.1 Proportion of individuals using the Internet
        17.9.1 Dollar value of financial and technical assistance (including through north–south, South‑South and triangular cooperation) committed to developing countries
        17.10.1 Worldwide weighted tariff-average
        17.11.1 Developing countries’ and least developed countries’ share of global exports
        17.12.1 Weighted average tariffs faced by developing countries, least developed countries and small island developing States
        17.13.1 Macroeconomic Dashboard
        17.14.1 Number of countries with mechanisms in place to enhance policy coherence of sustainable development
        17.15.1 Extent of use of country-owned results frameworks and planning tools by providers of development cooperation
        17.16.1 Number of countries reporting progress in multi-stakeholder development effectiveness monitoring frameworks that support the achievement of the sustainable development goals
        17.17.1 Amount in United States dollars committed to public-private partnerships for infrastructure
        17.18.1 Statistical capacity indicator for Sustainable Development Goal monitoring
        17.18.2 Number of countries that have national statistical legislation that complies with the Fundamental Principles of Official Statistics
        17.18.3 Number of countries with a national statistical plan that is fully funded and under implementation, by source of funding
        17.19.1 Dollar value of all resources made available to strengthen statistical capacity in developing countries
        17.19.2 Proportion of countries that (a) have conducted at least one population and housing census in the last 10 years; and (b) have achieved 100 per cent birth registration and 80 per cent death registration

        Here are the details of the AI system:

        Domain: "{}",
        Purpose: "{}",
        Capability: "{}",
        Sensing instrument and location: "{}",
        AI User: "{}",
        AI Subject: "{}"

         Please return the assessment in the following format:
         {{
           "Description": "The AI system intended to be used ...",
           "Targets Supported for SDG [SDG Number12]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number12]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number12]": "[Explanation]",
           "Targets Supported for SDG [SDG Number13]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number13]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number13]": "[Explanation]",
           "Targets Supported for SDG [SDG Number14]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number14]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number14]": "[Explanation]",
           "Targets Supported for SDG [SDG Number15]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number15]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number15]": "[Explanation]",
           "Targets Supported for SDG [SDG Number16]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number16]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number16]": "[Explanation]",
           "Targets Supported for SDG [SDG Number17]": "Include Relevant Targets (ONLY their number id) that mostly closely resembles the text.",
           "Indicators Supported for SDG [SDG Number17]": "Include Relevant Indicators (ONLY their number id) that mostly closely resembles the text.",
           "Reasoning for Support for SDG [SDG Number17]": "[Explanation]",
         }}
            """
    }
]



def format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject):
    S = "test {}"
    messages = deepcopy(MESSAGES)
    messages[1]['content'] = messages[1]['content'].format(domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)
    return messages



FULL_RES = []
cost = 0

start_time = time.time()
i = 0
for useElements in prompt_result:
  useI = str(useElements['Use'])
  if int(useI) not in [92]:
    continue
  # print (f" Parsing use {useI}")

  # Variables for message placeholders
  domain = useElements['Domain']
  purpose = useElements['Purpose']
  aiCapability = useElements['Capability']
  sensingInstrument = useElements['Sensing instrument and location']
  aiUser = useElements['AI User']
  aiSubject = useElements['AI Subject']

  # Extracting "Use i" details
  use_i_details = [domain, purpose, aiCapability, sensingInstrument, aiUser, aiSubject]

  # adapt the prompt for useI
  messages = format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)

  # run the prompt
  response = get_completion_from_messages(messages, temperature=0)
  # print(response)

  # response, token_count = get_completion_and_token_count(messages, temperature=0)
  # res = token_count
  # cost_chunk = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
  # cost += cost_chunk

  try:
    response = ast.literal_eval(response)
  except:
    time.sleep(33)
    continue

  # print(response)

  # combine the useI and the risk report
  combined_response = {}
  combined_response["id"]= useI
  combined_response["Details"] = use_i_details
  for k, v in response.items():
    combined_response[k] = v
  pprint.pprint (combined_response)

  # save result
  # with open(f"{useI}_risk_report_full.json", "w") as json_file:
  #     json.dump(combined_response, json_file, indent=4)  # 4 spaces of indentation
  # # Download the file to your local machine
  # files.download(f"{useI}_risk_report_full.json")

  FULL_RES.append(combined_response)

  time.sleep(33)

  i+=1
  # print(i)
  # UNCOMMENT FOR RUNNING FOR 3 uses only
  # if i==25:
  #   break

FULL_RES_part3 = FULL_RES.copy()


###############################
# save result
# with open(f"FULL_SDG_REPORT_EO.json", "w") as json_file:
#     json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# # Download the file to your local machine
# files.download(f"FULL_SDG_REPORT_EO.json")
# end_time = time.time()

# print(f"Execution time: {end_time - start_time:.5f} seconds")
# print (f"TOTAL COST {cost}")



###############################
# save result
with open(f"FULL_SDG_REPORT_part3.json", "w") as json_file:
    json.dump(FULL_RES_part3, json_file, indent=4)  # 4 spaces of indentation
# Download the file to your local machine
files.download(f"FULL_SDG_REPORT_part3.json")

###############################
# save result
with open(f"FULL_SDG_REPORT_part3.json", "w") as json_file:
    json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# Download the file to your local machine
files.download(f"FULL_SDG_REPORT_part3.json")


