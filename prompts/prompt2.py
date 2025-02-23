# -*- coding: utf-8 -*-
"""Mobile HCI - Risk Assessment Prompt

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
    # i += 1

  flattened_list = [item for sublist in file_content_dict for item in sublist]
  return flattened_list

prompt_result = read_prompt_output()

prompt_result

"""# FINAL PROMPT"""

# Assuming you have the variables domain, purpose, aiCapability, aiUser, and aiSubject defined with appropriate values

MESSAGES = [
    {
        'role': 'system',
        'content': """You are an experienced regulatory compliance specialists who works in the field of AI technology regulation. You are thoughtful, decisive, experienced and conscientious.
        You have access to the entirety of the EU AI Act and its amendments, which outline how various AI technologies are to be regulated and risk-classified within the European Union."""
    },
    {
        'role': 'user',
        'content': """

        Classify the following AI system by utilizing a three-tier classification: 1) Unacceptable Risk, 2) High Risk, and 3) Not Classified as High Risk or Unacceptable Risk.

        Follow these four steps below:
        1. Write a brief description of the AI system, using similar language to the EU AI Act. The description should start with "The AI system intended to be used ...", and be no longer than two sentences.
        2. Determine whether the AI system is of Unacceptable Risk or High Risk, providing the exact text from the EU AI Act and explaining the reasoning. Be very strict and verify the reasoning.
        Assume High Risk unless there is clear evidence for Unacceptable Risk. Pay particular attention to the subject and user of the AI system, as this is critical for classification.
        Ensure that the subject and user align with the text. They are very important. Also, ensure that you understand the purpose and the capability of the AI system as this is highly critical for the risk classification.
        For example, the capability to verify patient identities by using AI technology implies the use of biometric identification of patients. Be aware of these and similar cases.
        3. Go through all the amendments to the EU AI Act and ensure that nothing has changed that would affect the classification.
        If something has changed, update the classification accordingly and explicitly reference the amendment that most closely resembles the AI system.
        The amendments can be found under the text: "Here are some important amendments to the Act:"
        4. If the AI system is neither High Risk nor Unacceptable Risk, classify it as Not Classified as High Risk or Unacceptable Risk.

        It is of utmost importance to exercise precision and make accurate judgments when classifying the risk associated with the AI system.
        Please carefully consider all the regulations listed below during the risk classification of the AI system:

        The relevant portions of the Act for what is unacceptable:
        5.2.2. PROHIBITED ARTIFICIAL INTELLIGENCE PRACTICES (TITLE II)
        Title II establishes a list of prohibited AI. The regulation follows a risk-based approach,
        differentiating between uses of AI that create (i) an unacceptable risk, (ii) a high risk, and (iii)
        low or minimal risk. The list of prohibited practices in Title II comprises all those AI systems
        whose use is considered unacceptable as contravening Union values, for instance by violating
        fundamental rights. The prohibitions covers practices that have a significant potential to
        manipulate persons through subliminal techniques beyond their consciousness or exploit vulnerabilities
        of specific vulnerable groups such as children or persons with disabilities in
        order to materially distort their behaviour in a manner that is likely to cause them or another
        person psychological or physical harm. Other manipulative or exploitative practices affecting
        adults that might be facilitated by AI systems could be covered by the existing data
        protection, consumer protection and digital service legislation that guarantee that natural
        persons are properly informed and have free choice not to be subject to profiling or other
        practices that might affect their behaviour. The proposal also prohibits AI-based social
        scoring for general purposes done by public authorities. Finally, the use of ‘real time’ remote
        biometric identification systems in publicly accessible spaces for the purpose of law
        enforcement is also prohibited unless certain limited exceptions apply.

        PROHIBITED ARTIFICIAL INTELLIGENCE PRACTICES
        Article 5
        1. The following artificial intelligence practices shall be prohibited:
        (a) the placing on the market, putting into service or use of an AI system that
        deploys subliminal techniques beyond a person’s consciousness in order to
        materially distort a person’s behaviour in a manner that causes or is likely to
        cause that person or another person physical or psychological harm;
        (b) the placing on the market, putting into service or use of an AI system that
        exploits any of the vulnerabilities of a specific group of persons due to their
        age, physical or mental disability, in order to materially distort the behaviour of
        a person pertaining to that group in a manner that causes or is likely to cause
        that person or another person physical or psychological harm;
        (c) the placing on the market, putting into service or use of AI systems by public
        authorities or on their behalf for the evaluation or classification of the
        trustworthiness of natural persons over a certain period of time based on their
        social behaviour or known or predicted personal or personality characteristics,
        with the social score leading to either or both of the following:
        (i) detrimental or unfavourable treatment of certain natural persons or whole
        groups thereof in social contexts which are unrelated to the contexts in
        which the data was originally generated or collected;
        (ii) detrimental or unfavourable treatment of certain natural persons or whole
        groups thereof that is unjustified or disproportionate to their social
        behaviour or its gravity;
        (d) the use of ‘real-time’ remote biometric identification systems in publicly
        accessible spaces for the purpose of law enforcement, unless and in as far as
        such use is strictly necessary for one of the following objectives:
        the targeted search for specific potential victims of crime, including
        missing children;
        (ii) the prevention of a specific, substantial and imminent threat to the life or
        physical safety of natural persons or of a terrorist attack;
        (iii) the detection, localisation, identification or prosecution of a perpetrator
        or suspect of a criminal offence referred to in Article 2(2) of Council
        Framework Decision 2002/584/JHA62 and punishable in the Member
        State concerned by a custodial sentence or a detention order for a
        maximum period of at least three years, as determined by the law of that
        Member State.
        2. The use of ‘real-time’ remote biometric identification systems in publicly accessible
        spaces for the purpose of law enforcement for any of the objectives referred to in
        paragraph 1 point d) shall take into account the following elements:
        (a) the nature of the situation giving rise to the possible use, in particular the
        seriousness, probability and scale of the harm caused in the absence of the use
        of the system;
        (b) the consequences of the use of the system for the rights and freedoms of all
        persons concerned, in particular the seriousness, probability and scale of those
        consequences.
        In addition, the use of ‘real-time’ remote biometric identification systems in publicly
        accessible spaces for the purpose of law enforcement for any of the objectives
        referred to in paragraph 1 point d) shall comply with necessary and proportionate
        safeguards and conditions in relation to the use, in particular as regards the temporal,
        geographic and personal limitations.
        3. As regards paragraphs 1, point (d) and 2, each individual use for the purpose of law
        enforcement of a ‘real-time’ remote biometric identification system in publicly
        accessible spaces shall be subject to a prior authorisation granted by a judicial
        authority or by an independent administrative authority of the Member State in
        which the use is to take place, issued upon a reasoned request and in accordance with
        the detailed rules of national law referred to in paragraph 4. However, in a duly
        justified situation of urgency, the use of the system may be commenced without an
        authorisation and the authorisation may be requested only during or after the use.
        The competent judicial or administrative authority shall only grant the authorisation
        where it is satisfied, based on objective evidence or clear indications presented to it,
        that the use of the ‘real-time’ remote biometric identification system at issue is
        necessary for and proportionate to achieving one of the objectives specified in
        paragraph 1, point (d), as identified in the request. In deciding on the request, the
        competent judicial or administrative authority shall take into account the elements
        referred to in paragraph 2.
        4. A Member State may decide to provide for the possibility to fully or partially
        authorise the use of ‘real-time’ remote biometric identification systems in publicly
        accessible spaces for the purpose of law enforcement within the limits and under the
        conditions listed in paragraphs 1, point (d), 2 and 3. That Member State shall lay
        down in its national law the necessary detailed rules for the request, issuance and
        exercise of, as well as supervision relating to, the authorisations referred to in
        paragraph 3. Those rules shall also specify in respect of which of the objectives listed
        in paragraph 1, point (d), including which of the criminal offences referred to in
        point (iii) thereof, the competent authorities may be authorised to use those systems
        for the purpose of law enforcement.

        The relevant portions of the Act for what is High risk:
        CLASSIFICATION OF AI SYSTEMS AS HIGH-RISK
        Article 6
        Classification rules for high-risk AI systems
        1. Irrespective of whether an AI system is placed on the market or put into service
        independently from the products referred to in points (a) and (b), that AI system shall
        be considered high-risk where both of the following conditions are fulfilled:
        (a) the AI system is intended to be used as a safety component of a product, or is
        itself a product, covered by the Union harmonisation legislation listed in Annex
        II;
        (b) the product whose safety component is the AI system, or the AI system itself as
        a product, is required to undergo a third-party conformity assessment with a
        view to the placing on the market or putting into service of that product
        pursuant to the Union harmonisation legislation listed in Annex II.
        2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems
        referred to in Annex III shall also be considered high-risk.
        When assessing for the purposes of paragraph 1 whether an AI system poses a risk of
        harm to the health and safety or a risk of adverse impact on fundamental rights that is
        equivalent to or greater than the risk of harm posed by the high-risk AI systems already
        referred to in Annex III, the Commission shall take into account the
        following criteria:
        (a) the intended purpose of the AI system;
        (b) the extent to which an AI system has been used or is likely to be used;
        (c) the extent to which the use of an AI system has already caused harm to the
        health and safety or adverse impact on the fundamental rights or has given rise
        to significant concerns in relation to the materialisation of such harm or
        adverse impact, as demonstrated by reports or documented allegations
        submitted to national competent authorities;
        (d) the potential extent of such harm or such adverse impact, in particular in terms
        of its intensity and its ability to affect a plurality of persons;
        (e) the extent to which potentially harmed or adversely impacted persons are
        dependent on the outcome produced with an AI system, in particular because
        for practical or legal reasons it is not reasonably possible to opt-out from that
        outcome;
        (f) the extent to which potentially harmed or adversely impacted persons are in a
        vulnerable position in relation to the user of an AI system, in particular due to
        an imbalance of power, knowledge, economic or social circumstances, or age;
        (g) the extent to which the outcome produced with an AI system is easily
        reversible, whereby outcomes having an impact on the health or safety of
        persons shall not be considered as easily reversible;
        (h) the extent to which existing Union legislation provides for:
        (i) effective measures of redress in relation to the risks posed by an AI
        system, with the exclusion of claims for damages;
        (ii) effective measures to prevent or substantially minimise those risks.


        HIGH-RISK AI SYSTEMS REFERRED TO IN ARTICLE 6(2)
        High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following
        areas:
        1. Biometric identification and categorisation of natural persons:
        (a) AI systems intended to be used for the ‘real-time’ and ‘post’ remote biometric
        identification of natural persons;
        2. Management and operation of critical infrastructure:
        (a) AI systems intended to be used as safety components in the management and
        operation of road traffic and the supply of water, gas, heating and electricity.
        3. Education and vocational training:
        (a) AI systems intended to be used for the purpose of determining access or
        assigning natural persons to educational and vocational training institutions;
        (b) AI systems intended to be used for the purpose of assessing students in
        educational and vocational training institutions and for assessing participants in
        tests commonly required for admission to educational institutions.
        4. Employment, workers management and access to self-employment:
        (a) AI systems intended to be used for recruitment or selection of natural persons,
        notably for advertising vacancies, screening or filtering applications, evaluating
        candidates in the course of interviews or tests;
        (b) AI intended to be used for making decisions on promotion and termination of
        work-related contractual relationships, for task allocation and for monitoring
        and evaluating performance and behavior of persons in such relationships.
        5. Access to and enjoyment of essential private services and public services and
        benefits:
        (a) AI systems intended to be used by public authorities or on behalf of public
        authorities to evaluate the eligibility of natural persons for public assistance
        benefits and services, as well as to grant, reduce, revoke, or reclaim such
        benefits and services;
        (b) AI systems intended to be used to evaluate the creditworthiness of natural
        persons or establish their credit score, with the exception of AI systems put into
        service by small scale providers for their own use;
        (c) AI systems intended to be used to dispatch, or to establish priority in the
        dispatching of emergency first response services, including by firefighters and
        medical aid.
        6. Law enforcement:
        (a) AI systems intended to be used by law enforcement authorities for making
        individual risk assessments of natural persons in order to assess the risk of a
        natural person for offending or reoffending or the risk for potential victims of
        criminal offences;
        (b) AI systems intended to be used by law enforcement authorities as polygraphs
        and similar tools or to detect the emotional state of a natural person;
        EN 5 EN
        (c) AI systems intended to be used by law enforcement authorities to detect deep
        fakes as referred to in article 52(3);
        (d) AI systems intended to be used by law enforcement authorities for evaluation
        of the reliability of evidence in the course of investigation or prosecution of
        criminal offences;
        (e) AI systems intended to be used by law enforcement authorities for predicting
        the occurrence or reoccurrence of an actual or potential criminal offence
        based on profiling of natural persons as referred to in Article 3(4) of Directive
        (EU) 2016/680 or assessing personality traits and characteristics or past
        criminal behaviour of natural persons or groups;
        (f) AI systems intended to be used by law enforcement authorities for profiling of
        natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 in the
        course of detection, investigation or prosecution of criminal offences;
        (g) AI systems intended to be used for crime analytics regarding natural persons,
        allowing law enforcement authorities to search complex related and unrelated
        large data sets available in different data sources or in different data formats in
        order to identify unknown patterns or discover hidden relationships in the data.
        7. Migration, asylum and border control management:
        (a) AI systems intended to be used by competent public authorities as polygraphs
        and similar tools or to detect the emotional state of a natural person;
        (b) AI systems intended to be used by competent public authorities to assess a risk,
        including a security risk, a risk of irregular immigration, or a health risk, posed
        by a natural person who intends to enter or has entered into the territory of a
        Member State;
        (c) AI systems intended to be used by competent public authorities for the
        verification of the authenticity of travel documents and supporting
        documentation of natural persons and detect non-authentic documents by
        checking their security features;
        (d) AI systems intended to assist competent public authorities for the examination
        of applications for asylum, visa and residence permits and associated
        complaints with regard to the eligibility of the natural persons applying for a
        status.
        8. Administration of justice and democratic processes:
        (a) AI systems intended to assist a judicial authority in researching and
        interpreting facts and the law and in applying the law to a concrete set of facts.

        Here are some important amendments to the EU AI Act: It is very important to consider them for the risk classification. Please read them carefully:
        Amendment 709
        Proposal for a regulation
        Annex III – paragraph 1 – introductory part
        High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas:
          The AI systems specifically refered to in under points 1 to 8a stand for critical use cases and are each considered to be high-risk AI systems pursuant to Article 6(2), provided that they fulfil the criteria set out in that Article:
        Amendment 710
        Proposal for a regulation
        Annex III – paragraph 1 – point 1 – introductory part
        1.  Biometric identification and categorisation of natural persons:
          1.  Biometric and biometrics-based systems
        Amendment 711
        Proposal for a regulation
        Annex III – paragraph 1 – point 1 – point a
        (a)  AI systems intended to be used for the ‘real-time’ and ‘post’ remote biometric identification of natural persons;
          (a)  AI systems intended to be used for biometric identification of natural persons, with the exception of those mentioned in Article 5;
        Amendment 712
        Proposal for a regulation
        Annex III – paragraph 1 – point 1 – point a a (new)
          (a a)  AI systems intended to be used to make inferences about personal characteristics of natural persons on the basis of biometric or biometrics-based data, including emotion recognition systems, with the exception of those mentioned in Article 5;
          Point 1 shall not include AI systems intended to be used for biometric verification whose sole purpose is to confirm that a specific natural person is the person he or she claims to be.
        Amendment 713
        Proposal for a regulation
        Annex III – paragraph 1 – point 2 – point a
        (a)  AI systems intended to be used as safety components in the management and operation of road traffic and the supply of water, gas, heating and electricity.
          (a)  AI systems intended to be used as safety components in the management and operation of road, rail and air traffic unless they are regulated in harmonisation or sectoral law.
        Amendment 714
        Proposal for a regulation
        Annex III – paragraph 1 – point 2 – point a a (new)
          (a a)  AI systems intended to be used as safety components in the management and operation of the supply of water, gas, heating, electricity and critical digital infrastructure;
        Amendment 715
        Proposal for a regulation
        Annex III – paragraph 1 – point 3 – point a
        (a)  AI systems intended to be used for the purpose of determining access or assigning natural persons to educational and vocational training institutions;
          (a)  AI systems intended to be used for the purpose of determining access or materially influence decisions on admission or assigning natural persons to educational and vocational training institutions;
        Amendment 716
        Proposal for a regulation
        Annex III – paragraph 1 – point 3 – point b
        (b)  AI systems intended to be used for the purpose of assessing students in educational and vocational training institutions and for assessing participants in tests commonly required for admission to educational institutions.
          (b)  AI systems intended to be used for the purpose of assessing students in educational and vocational training institutions and for assessing participants in tests commonly required for admission to those institutions;
        Amendment 717
        Proposal for a regulation
        Annex III – paragraph 1 – point 3 – point b a (new)
          (b a)  AI systems intended to be used for the purpose of assessing the appropriate level of education for an individual and materially influencing the level of education and vocational training that individual will receive or will be able to access;
        Amendment 718
        Proposal for a regulation
        Annex III – paragraph 1 – point 3 – point b b (new)
          (b b)  AI systems intended to be used for monitoring and detecting prohibited behaviour of students during tests in the context of/within education and vocational training institutions;
        Amendment 719
        Proposal for a regulation
        Annex III – paragraph 1 – point 4 – point a
        (a)  AI systems intended to be used for recruitment or selection of natural persons, notably for advertising vacancies, screening or filtering applications, evaluating candidates in the course of interviews or tests;
          (a)  AI systems intended to be used for recruitment or selection of natural persons, notably for placing targeted job advertisements screening or filtering applications, evaluating candidates in the course of interviews or tests;
        Amendment 720
        Proposal for a regulation
        Annex III – paragraph 1 – point 4 – point b
        (b)  AI intended to be used for making decisions on promotion and termination of work-related contractual relationships, for task allocation and for monitoring and evaluating performance and behavior of persons in such relationships.
          (b)  AI systems intended to be used to make or materially influence decisions affecting the initiation, promotion and termination of work-related contractual relationships, task allocation based on individual behaviour or personal traits or characteristics, or for monitoring and evaluating performance and behavior of persons in such relationships;
        Amendment 721
        Proposal for a regulation
        Annex III – paragraph 1 – point 5 – point a
        (a)  AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for public assistance benefits and services, as well as to grant, reduce, revoke, or reclaim such benefits and services;
          (a)  AI systems intended to be used by or on behalf of public authorities to evaluate the eligibility of natural persons for public assistance benefits and services, including healthcare services and essential services, including but not limited to housing, electricity, heating/cooling and internet, as well as to grant, reduce, revoke, increase or reclaim such benefits and services;
        Amendment 722
        Proposal for a regulation
        Annex III – paragraph 1 – point 5 – point b
        (b)  AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems put into service by small scale providers for their own use;
          (b)  AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score , with the exception of AI systems used for the purpose of detecting financial fraud;
        Amendment 723
        Proposal for a regulation
        Annex III – paragraph 1 – point 5 – point b a (new)
          (b a)  AI systems intended to be used for making decisions or materially influencing decisions on the eligibility of natural persons for health and life insurance;
        Amendment 724
        Proposal for a regulation
        Annex III – paragraph 1 – point 5 – point c
        (c)  AI systems intended to be used to dispatch, or to establish priority in the dispatching of emergency first response services, including by firefighters and medical aid.
          (c)  AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of emergency first response services, including by police and law enforcement, firefighters and medical aid, as well as of emergency healthcare patient triage systems;
        Amendment 725
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point a
        (a)  AI systems intended to be used by law enforcement authorities for making individual risk assessments of natural persons in order to assess the risk of a natural person for offending or reoffending or the risk for potential victims of criminal offences;
          deleted
        Amendment 726
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point b
        (b)  AI systems intended to be used by law enforcement authorities as polygraphs and similar tools or to detect the emotional state of a natural person;
          (b)  AI systems intended to be used by or on behalf of law enforcement authorities, or by Union agencies, offices or bodies in support of law enforcement authorities as polygraphs and similar tools, insofar as their use is permitted under relevant Union and national law;
        Amendment 727
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point c
        (c)  AI systems intended to be used by law enforcement authorities to detect deep fakes as referred to in article 52(3);
          deleted
        Amendment 728
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point d
        (d)  AI systems intended to be used by law enforcement authorities for evaluation of the reliability of evidence in the course of investigation or prosecution of criminal offences;
          (d)  AI systems intended to be used by or on behalf of law enforcement authorities, or by Union agencies, offices or bodies in support of law enforcement authorities to evaluate the reliability of evidence in the course of investigation or prosecution of criminal offences;
        Amendment 729
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point e
        (e)  AI systems intended to be used by law enforcement authorities for predicting the occurrence or reoccurrence of an actual or potential criminal offence based on profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 or assessing personality traits and characteristics or past criminal behaviour of natural persons or groups;
          deleted
        Amendment 730
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point f
        (f)  AI systems intended to be used by law enforcement authorities for profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 in the course of detection, investigation or prosecution of criminal offences;
          (f)  AI systems intended to be used by or on behalf of law enforcement authorities or by Union agencies, offices or bodies in support of law enforcement authorities for profiling of natural persons as referred to in Article 3(4) of Directive (EU) 2016/680 in the course of detection, investigation or prosecution of criminal offences or, in the case of Union agencies, offices or bodies, as referred to in Article 3(5) of Regulation (EU) 2018/1725;
        Amendment 731
        Proposal for a regulation
        Annex III – paragraph 1 – point 6 – point g
        (g)  AI systems intended to be used for crime analytics regarding natural persons, allowing law enforcement authorities to search complex related and unrelated large data sets available in different data sources or in different data formats in order to identify unknown patterns or discover hidden relationships in the data.
          (g)  AI systems intended to be used by or on behalf of law enforcement authorities or by Union agencies, offices or bodies in support of law enforcement authorities for crime analytics regarding natural persons, allowing law enforcement authorities to search complex related and unrelated large data sets available in different data sources or in different data formats in order to identify unknown patterns or discover hidden relationships in the data.
        Amendment 732
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point a
        (a)  AI systems intended to be used by competent public authorities as polygraphs and similar tools or to detect the emotional state of a natural person;
          (a)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies as polygraphs and similar tools insofar as their use is permitted under relevant Union or national law
        Amendment 733
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point b
        (b)  AI systems intended to be used by competent public authorities to assess a risk, including a security risk, a risk of irregular immigration, or a health risk, posed by a natural person who intends to enter or has entered into the territory of a Member State;
          (b)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies to assess a risk, including a security risk, a risk of irregular immigration, or a health risk, posed by a natural person who intends to enter or has entered into the territory of a Member State;
        Amendment 734
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point c
        (c)  AI systems intended to be used by competent public authorities for the verification of the authenticity of travel documents and supporting documentation of natural persons and detect non-authentic documents by checking their security features;
          (c)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies for the verification of the authenticity of travel documents and supporting documentation of natural persons and detect non-authentic documents by checking their security features;
        Amendment 735
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point d
        (d)  AI systems intended to assist competent public authorities for the examination of applications for asylum, visa and residence permits and associated complaints with regard to the eligibility of the natural persons applying for a status.
          (d)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies to assist competent public authorities for the examination and assessment of the veracity of evidence in relation to applications for asylum, visa and residence permits and associated complaints with regard to the eligibility of the natural persons applying for a status;
        Amendment 736
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point d a (new)
          (d a)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies in migration, asylum and border control management to monitor, surveil or process data in the context of border management activities, for the purpose of detecting, recognising or identifying natural persons;
        Amendment 737
        Proposal for a regulation
        Annex III – paragraph 1 – point 7 – point d b (new)
          (d b)  AI systems intended to be used by or on behalf of competent public authorities or by Union agencies, offices or bodies in migration, asylum and border control management for the forecasting or prediction of trends related to migration movement and border crossing;
        Amendment 738
        Proposal for a regulation
        Annex III – paragraph 1 – point 8 – point a
        (a)  AI systems intended to assist a judicial authority in researching and interpreting facts and the law and in applying the law to a concrete set of facts.
          (a)  AI systems intended to be used by a judicial authority ot administrative body or on their behalf to assist a judicial authority or administrative body in researching and interpreting facts and the law and in applying the law to a concrete set of facts or used in a similar way in alternative dispute resolution.
        Amendment 739
        Proposal for a regulation
        Annex III – paragraph 1 – point 8 – point a a (new)
          (a a)  AI systems intended to be used for influencing the outcome of an election or referendum or the voting behaviour of natural persons in the exercise of their vote in elections or referenda. This does not include AI systems whose output natural persons are not directly exposed to, such as tools used to organise, optimise and structure political campaigns from an administrative and logistic point of view.
        Amendment 740
        Proposal for a regulation
        Annex III – paragraph 1 – point 8 – point a b (new)
          (a b)  AI systems intended to be used by social media platforms that have been designated as very large online platforms within the meaning of Article 33 of Regulation EU 2022/2065, in their recommender systems to recommend to the recipient of the service user-generated content available on the platform.

        Here are the details of the AI system:

        Domain: "{}",
        Purpose: "{}",
        Capability: "{}",
        Sensing instrument and location: "{}",
        AI User: "{}",
        AI Subject: "{}"

         Please return the classification in the following format:
         {{
           "Description": "The AI system intended to be used ...",
           "Classification": ["Unacceptable Risk"/"High Risk"/"Not Classified as High Risk or Unacceptable Risk"],
           "Relevant Text from the EU AI Act": "[Quotation if applicable] - Include the amendment or EU AI Act section that mostly closely resembles the text.",
           "Reasoning": "[Explanation]"
         }}
            """
    }
]



def format_prompt(MESSAGES, domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject):
    S = "test {}"
    messages = deepcopy(MESSAGES)
    messages[1]['content'] = messages[1]['content'].format(domain,purpose,aiCapability,sensingInstrument,aiUser,aiSubject)
    return messages

"""# APPLY / RUN"""

FULL_RES = []
cost = 0

start_time = time.time()
i = 0
for useElements in prompt_result:
  useI = str(useElements['Use'])
  if int(useI) > 74:
    continue
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
  # response = get_completion_from_messages(messages, temperature=0)
  # print(response)

  response, token_count = get_completion_and_token_count(messages, temperature=0)
  res = token_count
  cost_chunk = (res['prompt_tokens'] * 0.03  + res['completion_tokens'] * 0.06)/1000.0
  cost += cost_chunk

  response = ast.literal_eval(response)

  print(replace_key(response, "Relevant Text from the EU AI Act", "AIActText"))
  # print(response)

  # save result
  # with open(f"{useI}_risk_report.json", "w") as json_file:
  #     json.dump(response, json_file, indent=4)  # 4 spaces of indentation
  # # Download the file to your local machine
  # files.download(f"{useI}_risk_report.json")


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



###############################
# save result

print(f"Execution time: {end_time - start_time:.5f} seconds")
print (f"TOTAL COST {cost}")

print(FULL_RES)

###############################
# save result
with open(f"FULL_RISK_REPORT.json", "w") as json_file:
    json.dump(FULL_RES, json_file, indent=4)  # 4 spaces of indentation
# Download the file to your local machine
files.download(f"FULL_RISK_REPORT.json")







"""# THE END"""

