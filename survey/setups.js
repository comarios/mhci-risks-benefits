/////////////////////////////////////////////////////
/* GLOBAL VARIABLES TO BE EDITED BY SURVEY ADOPTERS */

let _PATH_USE_SET_1 = "data/uses_set1.json";
let _PATH_USE_SET_2 = "data/uses_set2.json";
let _URL_REDIRECT_AFTER_SURVEY_FINISHED = "";
let _URL_SERVER = "submit.php";

/////////////////////////////////////////////////////
let _REDIRECT_MESSAGE = "We received your responses. Please wait to be redirected to the completion page in ";
let _REDIRECT_TIME = 3;
let _COHORT_NAME = "crowdworkers";
let _SURVEYS_START_STEP = 2; // Start of annotating the first table with uses
let _SURVEYS_END_STEP = 4; // End of annotating the second table with uses

/* VARIABLES TO STORE PARTICIPANTS' ANSWERS */
let _ANSWERS = [];
let _JSON_Set1 = [];
let _JSON_Set2 = [];

/* CLEAR SESSION STORAGE */
sessionStorage.clear();
sessionStorage.setItem('cohort', _COHORT_NAME);

/* FORM */
/* Form steps */
let _steps = Array.from(document.querySelectorAll("div[class*='formbold-form-step-']"));
const steps = Array.from(document.querySelectorAll("[class^='formbold-form-step-']"));
const stepMenus = Array.from(document.querySelectorAll("[class^='formbold-step-menu-']"));
let currentStepIndex = 0;

/* Form buttons */
const formSubmitBtn = document.querySelector('.formbold-btn')
const formSubmitBtnSpan = formSubmitBtn.querySelector('span');

/* Move between survey sections */
function activateStep(stepArray, stepIndex) {
    stepArray.forEach((step, index) => {
        step.classList.toggle('active', index === stepIndex);
    });
    stepMenus.forEach((menu, index) => {
        menu.classList.toggle('active', index === stepIndex);
    });
}

/* Update text in the "Next" button */
function updateButtonLabel() {
    if (currentStepIndex === steps.length - 1) {
        formSubmitBtnSpan.textContent = 'End survey';
    } else if (currentStepIndex === 0) {
        formSubmitBtnSpan.textContent = 'Next';
    } else {
        formSubmitBtnSpan.textContent = 'Next';
    }
}

function getTimestamp() {
    var now = new Date();
    var date = String(now.getFullYear()).padStart(4, '0') + "-" +
        String(now.getMonth() + 1).padStart(2, '0') + "-" +
        String(now.getDate()).padStart(2, '0');
    var time = String(now.getHours()).padStart(2, '0') + ":" +
        String(now.getMinutes()).padStart(2, '0') + ":" +
        String(now.getSeconds()).padStart(2, '0');
    return date + " " + time;
}

function createDummyNode() {
    var dummy = document.createElement("input"); // Create a dummy input
    dummy.type = "radio";
    dummy.checked = false; // Ensure it's unchecked
    dummy.value = "null"; // No value
    return dummy;
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Smooth scrolling animation
    });
}

/* Helper function to count words in a string */
function countWordsInRange(text, minWords, maxWords) {
    var words = text.trim().split(/\s+/);
    var wordCount = words.length;
    return wordCount >= minWords && wordCount <= maxWords;
}

// SURVEY ANSWER VALUES
const riskCategories = ["Unacceptable use", "High risk use", "Low risk use"];
const realismCategories = ["Existing", "Upcoming", "Unrealistic"];
const agreementCategories = ["Yes", "No"];

const sdgOptions = [
    "SDG1: No Poverty",
    "SDG2: Zero Hunger",
    "SDG3: Good Health and Well-being",
    "SDG4: Quality Education",
    "SDG5: Gender Equality",
    "SDG6: Clean Water and Sanitation",
    "SDG7: Affordable and Clean Energy",
    "SDG8: Decent Work and Economic Growth",
    "SDG9: Industry, Innovation, and Infrastructure",
    "SDG10: Reduced Inequality",
    "SDG11: Sustainable Cities and Communities",
    "SDG12: Responsible Consumption and Production",
    "SDG13: Climate Action",
    "SDG14: Life Below Water",
    "SDG15: Life on Land",
    "SDG16: Peace, Justice, and Strong Institutions",
    "SDG17: Partnerships for the Goals",
    "NNN00: None of the above"
];

// QUESTION EXPLANATION WIDGETS
const explanationSdgs = `<span class="tooltip">&#9432; <span class="tooltiptext">
<b>SDG1 - No Poverty:</b> End poverty in all its forms everywhere.<br>
<b>SDG2 - Zero Hunger:</b> End hunger, achieve food security and improved nutrition, and support sustainable agriculture.<br>
<b>SDG3 - Good Health and Well-being:</b> Ensure healthy lives and support well-being for all at all ages.<br>
<b>SDG4 - Quality Education:</b> Ensure inclusive and equitable quality education and support lifelong learning opportunities for all.<br>
<b>SDG5 - Gender Equality:</b> Achieve gender equality and empower all women and girls.<br>
<b>SDG6 - Clean Water and Sanitation:</b> Ensure availability and sustainable management of water and sanitation for all.<br>
<b>SDG7 - Affordable and Clean Energy:</b> Ensure access to affordable, reliable, sustainable, and modern energy for all.<br>
<b>SDG8 - Decent Work and Economic Growth:</b> Support sustained, inclusive, and sustainable economic growth, full and productive employment, and decent work for all.<br>
<b>SDG9 - Industry, Innovation, and Infrastructure:</b> Build resilient infrastructure, support inclusive and sustainable industrialization, and foster innovation.<br>
<b>SDG10 - Reduced Inequality:</b> Reduce inequality within and among countries.<br>
<b>SDG11 - Sustainable Cities and Communities:</b> Make cities and human settlements inclusive, safe, resilient, and sustainable.<br>
<b>SDG12 - Responsible Consumption and Production:</b> Ensure sustainable consumption and production patterns.<br>
<b>SDG13 - Climate Action:</b> Take urgent action to combat climate change and its impacts.<br>
<b>SDG14 - Life Below Water:</b> Conserve and sustainably use the oceans, seas, and marine resources for sustainable development.<br>
<b>SDG15 - Life on Land:</b> Protect, restore, and support sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss.<br>
<b>SDG16 - Peace, Justice, and Strong Institutions:</b> Support peaceful and inclusive societies for sustainable development, provide access to justice for all, and build effective, accountable, and inclusive institutions at all levels.<br>
<b>SDG17 - Partnerships for the Goals:</b> Strengthen the means of implementation and revitalize the global partnership for sustainability.
</span></span>`;

const explanationRisks = `<span class="tooltip">&#9432;
<span class="tooltiptext">
    <b>Unacceptable uses</b> are deemed incompatible with EU values or are
    inherently unethical.
    These uses are prohibited outright due to their potential to cause
    significant harm or violate
    fundamental rights and freedoms.
    </br>
    </br>
    <b>High risk uses</b> pose significant potential risks to the safety,
    fundamental rights, or
    freedoms of individuals. These risks might include threats to health,
    safety, or fundamental
    rights such as privacy. Examples of high risk uses might include AI in
    critical infrastructure,
    law enforcement, healthcare, or transportation.
    <br>
    </br>
    <b>Low risk uses</b> have a lower potential to cause harm to individuals
    or society. They are
    considered to pose minimal risks to safety, fundamental rights, or
    freedoms. Examples of low-risk
    uses might include AI in entertainment, customer service, or basic
    administrative tasks.
</span></span>`;

// FUNCTION TO POPULATE TABLE OF USES WITH DATA JSON
function populateTable(tableId, jsonUrl) {
    var table = d3.select(tableId + " tbody");

    d3.json(jsonUrl, function (data) {
        var rows = table.selectAll("tr")
            .data(data)
            .enter()
            .append("tr");

        // Column 1: Use decription, label and justification
        let description = rows.append("td")

        description
            .append("div")
            .attr("class", "use-counter")
            .append("text")
            .text("Use #")
            .append("span")
            .text(function (d) { return d.Use; });

        description.append("p")
            .attr("class", "use-title")
            .text(function (d) {
                return d.Description
            });

        description
            .append("p")
            .attr("class", "risk-label")
            .append("span")
            .attr("class", "risk-tag")
            .text(function (d) {
                return d.Classification + " use"
            });

        description.append("p")
            .attr("class", "risk-explanation")
            .text(function (d) {
                return "Justification: " + d.Reasoning
            });

        // Q1 How probable is this use? [Mandatory]
        var Q1 = rows.append("td")
        Q1.append("div").attr("class", "primary-question").append("p").text("Q1 How probable do you find this use?")
        Q1.each(function (d) { // Notice d is passed for use within each card
            var td = d3.select(this);
            realismCategories.forEach(function (level) {
                var td_wrapper = td.append("div").attr("class", "td-wrapper")
                td_wrapper.append("input")
                    .attr("type", "radio")
                    .attr("name", function (d) { return "probability_" + d.Use; })
                    .attr("value", level);
                td_wrapper.append("label")
                    .text(level);
            });
        });

        // Q2 Do you agree with the risk classification? [Mandatory]
        var Q2 = rows.append("td")

        Q2.each(function (d) { // 'd' refers to the current datum for the row
            var td = d3.select(this);
            var group = td.append("div").attr("class", "radio-group");
            group.append("div").attr("class", "primary-question").append("p").html("Q2 Do you agree with the risk classification?" + explanationRisks);
            agreementCategories.forEach(function (level) {
                var td_wrapper = group.append("div").attr("class", "td-wrapper");
                var radioInput = td_wrapper.append("input")
                    .attr("type", "radio")
                    .attr("name", "agreement_level_" + d.Use)
                    .attr("value", level)
                    .on("change", function () { toggleQ3Visibility(this, d.Use); }); // Attach event listener
                td_wrapper.append("label").text(level);
            });
        });

        // Q3 Please correct the classification. [Optional]
        var Q3 = Q2
            .each(function (d) {
                var td = d3.select(this);
                var group2 = td.append("div").attr("class", "radio-group").style("display", "none"); // Initially hidden
                group2.append("div").attr("class", "secondary-question").append("p").text("Please correct the classification:");
                riskCategories.forEach(function (option) {
                    var option_wrapper = group2.append("div").attr("class", "td-wrapper");
                    option_wrapper.append("input")
                        .attr("type", "radio")
                        .attr("name", "risk_level_" + d.Use)
                        .attr("value", option);
                    option_wrapper.append("label").text(option);
                });
            });

        // Toggle Q3's visivility based on Q2's answer
        function toggleQ3Visibility(element, useID) {
            var value = element.value;  // Get the value of the clicked radio button in Q2
            var td = d3.select(element).node().closest('td');  // Get the parent td of the clicked radio button
            // Select the second radio group within the same <td>, which pertains to Q3
            var Q3 = d3.select(td).selectAll('.secondary-question').node().parentNode;
            if (value === "No") {
                // Show Q3 if the selected value is "No"
                d3.select(Q3).style('display', null); // remove 'display: none' to make it visible
            } else {
                // Hide Q3 if the selected value is not "No"
                d3.select(Q3).style('display', 'none'); // set 'display: none' to hide it
            }
        }

        // Q4 Do you agree with the risk justification? [Mandatory]
        var Q4 = Q3
            .each(function (d) { // 'd' refers to the current datum for the row
                var td = d3.select(this);
                group3 = td.append("div").attr("class", "radio-group");
                group3.append("div").attr("class", "secondary-question").append("p").text("Q3 Do you agree with the risk justification?");
                agreementCategories.forEach(function (level) {
                    var td_wrapper = group3.append("div").attr("class", "td-wrapper");
                    td_wrapper.append("input")
                        .attr("type", "radio")
                        .attr("name", "agreement_justification_" + d.Use)  // Use 'd.Use' to make the name unique
                        .attr("value", level);
                    td_wrapper.append("label").text(level);
                });
            });

        // Q5 Please explain your reasoning about the use risk classification and justification. [Mandatory]
        var Q5 = rows.append("td")
            .each(function (d) {
                var td = d3.select(this);
                td.append("div").attr("class", "primary-question").append("p").text("Q4 Please explain your reasoning about the use risk classification and justification.");
                td.append("textarea")
                    .attr("name", "label_explanation_" + d.Use) // Unique name based on data
                    .attr("rows", "10") // Sets the number of lines
                    .on('paste', function () {
                        d3.event.preventDefault();
                        alert('Pasting text is not allowed in this field.');
                    })
            });

        // Q6 Please select all Sustainable Development Goals that this use supports. [Mandatory]
        var Q6 = rows.append("td")
        Q6.append("div").attr("class", "primary-question").append("p").html("Q5 Please select all Sustainable Development Goals that this use supports" + explanationSdgs)
        Q6.each(function (d) {
            var td = d3.select(this);
            var parent = td.append("div");
            // Loop through each SDG and include the index and d.Use in the name
            sdgOptions.forEach(function (sdg, index) {
                var td_wrapper = parent.append("div").attr("class", "sdg-wrapper");

                // Generate a unique ID for each checkbox
                var checkboxId = `sdg_${index + 1}_${d.Use}`;

                // Append checkbox and set ID
                td_wrapper.append("input")
                    .attr('type', 'checkbox')
                    .attr('id', checkboxId)  // Set unique ID for associating label
                    .attr('name', `sdg_${index + 1}_${d.Use}`)
                    .attr("value", sdg);

                // Append label and use 'for' attribute to link it with the checkbox
                td_wrapper.append("label")
                    .attr('for', checkboxId)  // Ensure the 'for' attribute matches the checkbox's ID
                    .text(sdg.split(":")[1]);
            });
        });

    });
}

// FUNCTION TO RETRIEVE DATA FROM PARTICIPANTS' INTERACTIONS ON THE WEBSITE
function getSurveyResponses(className) {
    // Get the current page of the survey
    const elements = document.querySelectorAll('.' + className);
    let allRequiredFilled = true;
    const responses = {};

    // Set flags for alert messages
    let inputFilled = true;
    let radioGroupFilled = true;

    // Get all elements in the survey page
    elements.forEach((element, index) => {

        // VALIDATE ONE_LINER RESPONSES
        const openQuestionWrappers = element.querySelectorAll('.open-question-wrapper');
        openQuestionWrappers.forEach(openQuestionWrapper => {
            const inputs = openQuestionWrapper.querySelectorAll('input');
            let label = openQuestionWrapper.querySelector('label');

            // Validation for the one-liner input
            inputs.forEach(input => {
                // Get the input value length
                let inputLength = input.value.length;
                let inputLimit = parseInt(input.getAttribute('minlength'));

                // Check if the input length is less than max characters
                if (inputLength < inputLimit) {
                    allRequiredFilled = false;
                    inputFilled = false;
                    // Add asterisk if input length in not correct
                    if (label && !label.innerHTML.includes("*")) {
                        label.innerHTML += ' <span style="color: red;">*</span>';
                    }
                } else {
                    // Remove asterisk if the input length is correct
                    if (label) {
                        label.innerHTML = label.innerHTML.replace(' <span style="color: red;">*</span>', '');
                    }
                }
            });
        });

        // VALIDATE RADIO BUTTONS
        const questionWrappers = element.querySelectorAll('.radio-question-wrapper');
        questionWrappers.forEach(questionWrapper => {
            const radioButtons = questionWrapper.querySelectorAll('input[type="radio"]');
            const isRadioSelected = Array.from(radioButtons).some(radio => radio.checked);
            const label = questionWrapper.querySelector('label');

            // Validate radio buttons
            if (!isRadioSelected) {
                allRequiredFilled = false;
                radioGroupFilled = false;
                radioFilled = false;
                // Add asterisk if a radio button is not selected
                if (label && !label.innerHTML.includes("*")) {
                    label.innerHTML += ' <span style="color: red;">*</span>';
                }
            } else {
                // Remove asterisk if a radio button is selected
                if (label) {
                    label.innerHTML = label.innerHTML.replace(' <span style="color: red;">*</span>', '');
                }
            }
        });

        const allInputs = element.querySelectorAll('input, textarea, select');

        allInputs.forEach(input => {
            // Handle survey responses based on different input types
            switch (input.type) {
                case 'radio':
                    if (input.checked) {
                        responses[input.name] = input.value;
                    }
                    break;
                case 'checkbox':
                    if (!responses[input.name]) {
                        responses[input.name] = [];
                    }
                    if (input.checked) {
                        responses[input.name].push(input.value);
                    }
                    break;
                case 'text':
                    responses[input.name] = input.value;
                    break;
                default:
                    console.log(`Unhandled input type: ${input.type}`);
            }
        });
    });

    if (!inputFilled) {
        alert("Your answer is too short. Please extend it to meet the minimum character requirement.");
    } else if (!radioGroupFilled) {
        alert("Your answer is incomplete. Please address the missing statements using radio buttons.");
    }
    return { allRequiredFilled, responses };
}

// VALIDATE SURVEY RESPONSES AND PUSH THEM TO GLOBAL VARIABLE, IF CORRECT
formSubmitBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent submitting the form
    scrollToTop();

    // Validate Pages 1-3: Prolific ID + Familiarity with definitions
    if (currentStepIndex == 0 || currentStepIndex == 1 || currentStepIndex == 2) {
        const { allRequiredFilled, responses } = getSurveyResponses('formbold-form-step-' + (currentStepIndex + 1));
        if (!allRequiredFilled) {
            return; // Do not proceed if not all required fields are filled
        }
        // Save individual responses to sessionStorage
        for (const [key, value] of Object.entries(responses)) {
            sessionStorage.setItem(key, value);
        }
    }

    // Validate Page 3: First table
    if (currentStepIndex == 3) {
        var isValid = true;
        d3.selectAll("#annotation-table-one tr").each(function (d, i) {
            // Get fields for the JSON based on the table's structure
            var row = d3.select(this);
            var useID = row.select("td:nth-child(1) span").text();
            var description = row.select("td:nth-child(1) p").text();
            var probabilityElement = row.select("td:nth-child(2) input[type='radio']:checked").node();  // This returns a DOM element - Existing, Upcoming, Unlikely
            var labelAgreement = row.select("td:nth-child(3) .radio-group:nth-child(1) input[type='radio']:checked").node();
            var correctedLabel = row.select("td:nth-child(3) .radio-group:nth-child(2) input[type='radio']:checked").node();
            // Check if correctedLabel is null and assign a dummy node if true
            if (!correctedLabel) {
                correctedLabel = createDummyNode();
            }
            var justificationAgreement = row.select("td:nth-child(3) .radio-group:nth-child(3) input[type='radio']:checked").node();
            var correctedJustification = row.select("td:nth-child(4) textarea").node();
            var sdgs = row.selectAll("td:nth-child(5) input[type='checkbox']:checked").nodes();

            // Clear previous errors and validation messages
            row.selectAll(".validation-error").remove(); 
            row.selectAll(".primary-question").style("background-color", "white");
            row.selectAll(".secondary-question").style("background-color", "white");

            if (!probabilityElement || !labelAgreement || (labelAgreement && labelAgreement.value === "No" && correctedLabel.value === "null") || !justificationAgreement || (correctedJustification.value.length === 0) || (sdgs.length === 0)) {
                isValid = false;
                if (!probabilityElement) {
                    row.select("td:nth-child(2) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }
                if (!labelAgreement) {
                    row.select("td:nth-child(3) .radio-group:nth-child(1) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (labelAgreement && labelAgreement.value === "No" && correctedLabel.value === "null") {
                    row.select("td:nth-child(3) .radio-group:nth-child(2) .secondary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (!justificationAgreement) {
                    row.select("td:nth-child(3) .radio-group:nth-child(3) .secondary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }
                if (correctedJustification.value.length === 0) {
                    row.select("td:nth-child(4) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (sdgs.length === 0) {
                    row.select("td:nth-child(5) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }
            }
            if (probabilityElement && labelAgreement && justificationAgreement) {
                _JSON_Set1.push({
                    "Use": useID,
                    "Description": description,
                    "Probability": probabilityElement.value,  // Existing, Upcoming, Unlikely
                    "ClassificationAgreement": labelAgreement.value,  // Yes/No
                    "CorrectedClassification": correctedLabel.value,
                    "JustificationAgreement": justificationAgreement.value, //Yes/No
                    "CorrectedJustification": correctedJustification.value,
                    "SDGs": sdgs.map(function (d) {
                        return d.value.split(":")[0]; // Split SDG option based on ":" and store it as the impacted SDG, e.g., "SDG13: Climate Action" -> will store "SDG13"
                    })
                });
            }
        });

        if (isValid) {
            // Object to hold the last occurrence of each "Use"
            let uniqueByUse = {};
            // Populate the object with entries, where duplicates are overwritten
            _JSON_Set1.forEach(item => {
                uniqueByUse[item.Use] = item;  // The key is `item.Use`, ensuring duplicates are overwritten
            });
            // Convert the unique object back to an array and overwrite jsonData
            _JSON_Set1 = Object.values(uniqueByUse);
        } else {
            alert("Some entries are incomplete. Please fill out all fields.");
            return;
        }
    }

    // Validate Page 4: Second table
    if (currentStepIndex == 4) {
        var isValid = true;
        d3.selectAll("#annotation-table-two tr").each(function (d, i) {
            // Get fields for the JSON based on the table's structure
            var row = d3.select(this);
            var useID = row.select("td:nth-child(1) span").text();
            var description = row.select("td:nth-child(1) p").text();
            var probabilityElement = row.select("td:nth-child(2) input[type='radio']:checked").node();  // This returns a DOM element - Existing, Upcoming, Unlikely
            var labelAgreement = row.select("td:nth-child(3) .radio-group:nth-child(1) input[type='radio']:checked").node();
            var correctedLabel = row.select("td:nth-child(3) .radio-group:nth-child(2) input[type='radio']:checked").node();

            // Check if correctedLabel is null and assign a dummy node if true
            if (!correctedLabel) {
                correctedLabel = createDummyNode();
            }
            var justificationAgreement = row.select("td:nth-child(3) .radio-group:nth-child(3) input[type='radio']:checked").node();
            var correctedJustification = row.select("td:nth-child(4) textarea").node();
            var sdgs = row.selectAll("td:nth-child(5) input[type='checkbox']:checked").nodes();

            // Clear previous errors and validation messages
            row.selectAll(".validation-error").remove();
            row.selectAll(".primary-question").style("background-color", "white");
            row.selectAll(".secondary-question").style("background-color", "white");

            if (!probabilityElement || !labelAgreement || (labelAgreement && labelAgreement.value === "No" && correctedLabel.value === "null") || !justificationAgreement || (correctedJustification.value.length === 0) || (sdgs.length === 0)) {
                isValid = false;
                if (!probabilityElement) {
                    row.select("td:nth-child(2) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (!labelAgreement) {
                    row.select("td:nth-child(3) .radio-group:nth-child(1) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (labelAgreement && labelAgreement.value === "No" && correctedLabel.value === "null") {
                    row.select("td:nth-child(3) .radio-group:nth-child(2) .secondary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (!justificationAgreement) {
                    row.select("td:nth-child(3) .radio-group:nth-child(3) .secondary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (correctedJustification.value.length === 0) {
                    row.select("td:nth-child(4) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }

                if (sdgs.length === 0) {
                    row.select("td:nth-child(5) .primary-question")
                        .style("background-color", "#ff005e38")
                        .append("span")
                        .attr("class", "validation-error")
                        .text(" *");
                }
            }
            if (probabilityElement && labelAgreement && justificationAgreement) {
                _JSON_Set2.push({
                    "Use": useID,
                    "Description": description,
                    "Probability": probabilityElement.value,  // Existing, Upcoming, Unlikely
                    "ClassificationAgreement": labelAgreement.value,  // Yes/No
                    "CorrectedClassification": correctedLabel.value,
                    "JustificationAgreement": justificationAgreement.value, //Yes/No
                    "CorrectedJustification": correctedJustification.value,
                    "SDGs": sdgs.map(function (d) {
                        return d.value.split(":")[0];
                    })
                });
            }
        });

        if (isValid) {
            let uniqueByUse = {};
            // Populate the object with entries, where duplicates are overwritten
            _JSON_Set2.forEach(item => {
                uniqueByUse[item.Use] = item;  // The key is `item.Use`, ensuring duplicates are overwritten
            });
            // Convert the unique object back to an array and overwrite jsonData
            _JSON_Set2 = Object.values(uniqueByUse);
        } else {
            alert("Some entries are incomplete. Please fill out all fields.");
            return;
        }

        // Validate and get responses for the current step
        const { allRequiredFilled, responses } = getSurveyResponses('formbold-form-step-' + (currentStepIndex + 1));

        if (!allRequiredFilled) {
            return; // Do not proceed if not all required fields are filled
        }

        if (allRequiredFilled) {
            sessionStorage.setItem('attention-check-two', responses.attention_check_two);
        }
    }

    // Save timestamps at specific steps
    switch (currentStepIndex) {
        case _SURVEYS_START_STEP: //
            sessionStorage.setItem('survey-start-timestamp', getTimestamp());
        case _SURVEYS_END_STEP:
            sessionStorage.setItem('survey-end-timestamp', getTimestamp());
            break;
    }

    // Check if not the last step
    if (currentStepIndex < steps.length - 1) {
        // Proceed to the next step
        currentStepIndex++;
        activateStep(_steps, currentStepIndex);
        updateButtonLabel();
    } else {
        // If the last step, handle final form submission
        sendData();
        document.getElementById('final-click').remove();
        document.getElementById('final-message').innerText = _REDIRECT_MESSAGE;
        document.querySelector('.formbold-btn').style.visibility = 'hidden';
        document.getElementById('countdown').style.visibility = 'visible';
        document.getElementById('countdown-wrapper').style.flexDirection = "row";
        document.getElementById('countdown-wrapper').style.alignItems = "center";
        document.querySelector('.hide-message').style.visibility = 'visible';
        updateCountdown();
    }
});

// FUNCTION TO SENT DATA TO THE SERVER
/* Save data as a separate json */
function sendData() {
    // Object to hold session storage data
    let dataToSend = {};

    // Iterate over all keys in sessionStorage
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (key !== "") {  // Check if the key is not empty
            const value = sessionStorage.getItem(key);
            dataToSend[key] = value;
        }
    }

    // Pushing each object in newData to the _ANSWERS array
    _JSON_Set1.forEach(item => _ANSWERS.push(item));
    _JSON_Set2.forEach(item => _ANSWERS.push(item));

    // Sorting the array by use 'id' in ascending order
    _ANSWERS.sort((a, b) => a.Use - b.Use);
    dataToSend['answers'] = _ANSWERS;

    // AJAX call to send the data to the server
    $.ajax({
        type: "POST",
        url: _URL_SERVER, // Replace with your server URL
        data: dataToSend,
        dataType: "text",
        success: function (response) {
            console.log("Data sent successfully:", response);
            formSubmitBtn.disabled = true;
        },
        error: function (xhr, status, error) {
            console.error("Error sending data:", xhr);
        }
    });
}

// FUNCTION TO UPDATE COUNTDOWN AND REDIRECT AFTER COUNTDOWN ENDS
function updateCountdown() {
    // Update countdown value in the HTML
    document.getElementById('countdown').textContent = _REDIRECT_TIME;

    // If countdown is finished, redirect to the confirmation page, e.g., on Prolific
    if (_REDIRECT_TIME <= 0) {
        window.location.href = _URL_REDIRECT_AFTER_SURVEY_FINISHED; 
    } else {
        // Decrement countdown value
        _REDIRECT_TIME--;

        // Call updateCountdown function again after each 1 second
        setTimeout(updateCountdown, 1000);
    }
}

/* DYNAMICALLY COUNT CHARACTERS OR WORDS */
document.addEventListener('DOMContentLoaded', () => {
    const textAreas = document.querySelectorAll('textarea.formbold-form-input');
    const textInputs = document.querySelectorAll('input.formbold-form-input');

    textAreas.forEach(textArea => {
        textArea.addEventListener('keyup', function () {
            // Get the boundary values for minimum and maximum number of words
            let words = 0;
            const wordLimit = parseInt(this.getAttribute('data-word-limit'));
            const wordMin = parseInt(this.getAttribute('data-word-min'));

            // Get the number of words
            if (this.value.match(/\S+/g) != null) {
                words = this.value.match(/\S+/g).length;
            }

            // Trim excess words
            if (words > wordLimit) {
                const trimmed = this.value.split(/\s+/, wordLimit).join(" ");
                this.value = trimmed + " ";
            }

            // Update word counter
            const label = this.previousElementSibling;
            const displayCount = label.querySelector('.display-count');
            displayCount.textContent = words;

            // Update counter color
            if (words >= wordMin) {
                displayCount.style.color = '#6A64F1';
            } else {
                displayCount.style.color = ''; // Revert to default color
            }
        });

    });

    textInputs.forEach(textInput => {
        textInput.addEventListener('keyup', function () {
            // Count number of characters
            let characters = this.value.length;
            const characterLimit = parseInt(this.getAttribute('minlength'));

            // Update counter
            const label = this.previousElementSibling;
            const displayCount = label.querySelector('.display-count');
            displayCount.textContent = characters;

            // Update counter color
            if (characters >= characterLimit) {
                displayCount.style.color = '#6A64F1';
            } else {
                displayCount.style.color = ''; // Revert to default color
            }
        })
    });
});

/* INITIALIZE FORM */
updateButtonLabel();
populateTable("#annotation-table-one", _PATH_USE_SET_1);
populateTable("#annotation-table-two", _PATH_USE_SET_2);