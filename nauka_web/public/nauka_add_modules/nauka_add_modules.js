function updateModuleName() {
    const moduleNameInput = document.getElementById("module-name");
    module.name = moduleNameInput.value;
}

function addElement() {
    const element = createNewElement();
    module.elements.push(element);
    updateElementsDisplay();
}

function createNewElement() {
    return {question: "", answer: "" };
}

function createElementDiv(element, index) {
    const elementDiv = document.createElement("div");
    elementDiv.classList.add("element");
    
    const numberLabel = document.createElement("span");
    numberLabel.textContent = (index + 1) + ". ";

    const questionInput = createInput("Pytanie", element.question, (value) => element.question = value);
    const answerInput = createInput("Odpowiedź", element.answer, (value) => element.answer = value);
    const removeButton = createRemoveButton(index);
    
    elementDiv.append(numberLabel, questionInput, answerInput, removeButton);
    return elementDiv;
}

function createInput(placeholder, value, onInputChange) {
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = placeholder;
    input.value = value;
    input.addEventListener("input", () => onInputChange(input.value));
    return input;
}

function createRemoveButton(index) {
    const button = document.createElement("button");
    button.textContent = "Usuń";
    button.addEventListener("click", function () {
        removeElement(index);
    });
    return button;
}

function removeElement(index) {
    module.elements.splice(index, 1);
    updateElementsDisplay();
}

function updateElementsDisplay() {
    const elementsContainer = document.getElementById("elements-container");
    elementsContainer.innerHTML = "";
    module.elements.forEach((element, index) => {
        elementsContainer.appendChild(createElementDiv(element, index));
    });
}

function send_data() {
    const urlSubmit = '/api/nauka/submit';
    const data = JSON.stringify(module);

    fetch(urlSubmit, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: data
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert("Błąd: " + result.error_message);
        } else {
            alert('Sukces: ' + result.error_message);
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
    });
}

let module = { name: "", elements: [] };

document.getElementById("module-name").addEventListener("input", updateModuleName);
document.getElementById("add-element").addEventListener("click", addElement);
document.getElementById("submit-data").addEventListener("click", send_data);
