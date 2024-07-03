# MobileHCI 2024: Good Intentions, Risky Inventions: A Method for Assessing the Risks and Benefits of AI in Mobile and Wearable Uses
Assessing the Risks and Benefits of AI in Mobile and Wearable Uses

## Install requirements
pip install -r requirements.txt

## Prompts 
*1.* prompt1.py: generate mobilehci uses
*2.* prompt2.py: classify use risks according to the EU AI Act
*3.* prompt3.py: determine whether the use is beneficial according to the UN's Sustainability Development Goals

## Survey for evaluating LLM-based classification
This is the code for a custom survey we developed and used to evaluate LLM-based classification of uses in a crowdsourcing study. It tasks crowd workers with two tasks.

##### First Task : 
It asks them to read the definitions of 'risky' and 'beneficial' uses.

##### Second Task:
It presents assessment cards for uses, containing the LLM-based use risk classification and its justification. For each use, it asks crowd workers to read the assessment card and answer five mandatory questions:
*Q1*: How probable do you find the use?
*Q2*: Do you agree with the use risk classification? If not, please correct the classification.
*Q3*: Do you agree with the use risk justification?
*Q4*: Please explain your reasoning about the use risk classification and justification.
*Q5*: Please select all SDGs that this use supports.

## Adapting the survey
To adapt the survey to your mobile HCI uses, you need to:
*Step 1*: Prepare two datasets of your uses, formatted as JSON files:
```json
    [{
        "Use": 1,
        "Description": "Enhancing security through facial recognition using high-performance cameras in smartphones",
        "Classification": "High Risk",
        "Reasoning": "The AI system is used for biometric identification, which is listed as a high-risk AI system under Article 6(2) and Annex III of the EU AI Act."
    },
    {
        "Use": 7,
        "Description": "Sharing calendars and reminders on mobile phones",
        "Classification": "Low risk",
        "Reasoning": "The AI system described does not involve any prohibited practices such as manipulation, exploitation, social scoring, or real-time remote biometric identification. Therefore, it is low risk."
    }]
```

*Step 2*: Edit the `setup.js` file by adding the paths to your two datasets, and the URL you want to redirect your crowd workers to after completion (e.g., Prolific completion page).
*Step 3*: Edit the `submit.php` file by adding the path to your server.

## How to cite our paper
```
@article{constantinides2024mhcirisksandbenefits,
  title={Good Intentions, Risky Inventions: A Method for Assessing the Risks and Benefits of AI in Mobile and Wearable Uses},
  author={Constantinides, Marios and Bogucka, Edyta and Scepanovic, Sanja and Quercia, Daniele},
  journal={Proceedings of the ACM on Human-Computer Interaction},
  volume={7},
  number={MHCI},
  pages={1--25},
  year={2024},
  publisher={ACM}
} 
```
