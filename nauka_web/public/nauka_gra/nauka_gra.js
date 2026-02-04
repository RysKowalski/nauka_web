// Klasa do zarządzania licznikiem
class Timer {
  constructor() {
    this.time = 0; // Czas w dziesiątych częściach sekundy
    this.interval = null; // ID interwału
  }
  // Rozpocznij licznik
  start() {
    console.log('started timer in');
    if (this.interval) return; // Jeśli już działa, nie uruchamiaj ponownie
    this.interval = setInterval(() => {
      this.time += 1; // Dodaj 0.1 sekundy
      this.update(); // Aktualizuj widok
    }, 100);
  }

  // Zatrzymaj licznik
  pause() {
    clearInterval(this.interval);
    this.interval = null;
  }

  // Ustaw licznik na określoną wartość
  set(timeInSeconds) {
    this.time = Math.round(timeInSeconds * 10); // Konwertuj sekundy na dziesiąte części sekundy
    this.update();
  }

  // Zwróć czas w formacie sekundowym z dokładnością do 0.1 sekundy
  getTime() {
    return (this.time / 10).toFixed(1);
  }

  // Aktualizuj widok
  update() {
    const element = document.getElementById('timer');
    element.textContent = this.getTime() + 's';
  }
}

function change_answer(show) {
  const element = document.getElementById('answer');
  if (show) {
    element.textContent = answer_content;
    element.classList.add('visible');
    element.classList.remove('hidden');
  } else {
    element.classList.add('hidden');
    element.classList.remove('visible');
  }
}

function show_question(text) {
  const element = document.getElementById('question');
  element.textContent = text;
}

function show_points(number) {
  const element = document.getElementById('points');
  element.textContent = 'punkty: ' + number;
}

function show_max_points(number) {
  const element = document.getElementById('max_points');
  element.textContent = 'Najwięcej punktów: ' + number;
}

function show_done_button(show) {
  const element = document.getElementById('done_button');
  if (show) {
    element.classList.add('visible');
    element.classList.remove('hidden');
  } else {
    element.classList.add('hidden');
    element.classList.remove('visible');
  }
}

function user_choice_buttons(show) {
  const element = document.getElementById('button_wrong');
  const element2 = document.getElementById('button_correct');
  if (show) {
    element.classList.add('visible');
    element.classList.remove('hidden');

    element2.classList.add('visible');
    element2.classList.remove('hidden');
  } else {
    element.classList.add('hidden');
    element.classList.remove('visible');

    element2.classList.add('hidden');
    element2.classList.remove('visible');
  }
}

function show_chances(show) {
  const element = document.getElementById('chances')
  if (show) {
    element.classList.add('visible');
    element.classList.remove('hidden');
  } else {
    element.classList.add('hidden');
    element.classList.remove('visible');
  }
}

function update_chances(data) {
  const chancesElement = document.getElementById('chances');
  chancesElement.innerHTML = '';
  const list = document.createElement('ul');
  for (const [key, value] of Object.entries(data)) {
    const listItem = document.createElement('li');
    listItem.textContent = `${key}: ${value}`;
    list.appendChild(listItem);
  }
  chancesElement.appendChild(list);
}

async function sendRequest(data, method, url) {
  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };
    if (method === 'POST') options.body = JSON.stringify(data);
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const jsonResponse = await response.json();
    console.log('Odpowiedź z serwera:', jsonResponse);
    return jsonResponse;
  } catch (error) {
    console.error('Błąd podczas wysyłania żądania:', error);
    throw error;
  }
}

function get_url_arguments() {
  // Pobierz aktualny URL
  const url = new URL(window.location.href);

  // Odczytaj parametry zapytania
  const params = new URLSearchParams(url.search);

  // Zwróć listę kluczy, które mają wartość 'true'
  const trueArguments = [];
  params.forEach((value, key) => {
    if (value === 'true') {
      trueArguments.push(key);
    }
  });

  // Zwróć obiekt z wynikami
  return {
    modules: trueArguments,
  };
}

function on_done_button() {
  timer.pause()
  show_done_button(false)
  user_choice_buttons(true)
  change_answer(true)
}

function on_user_correct() {
  move(true)
}

function on_user_wrong() {
  move(false)
}

function move(user_answer) {
  const user_time = timer.getTime();

  sendRequest({ 'time': user_time, 'answer': user_answer }, 'POST', '/api/nauka/move')
    .then((new_data) => {
      // Po zakończeniu operacji, przetwarzamy dane
      if (new_data && new_data.element_list) {
        show_points(new_data.points);
        show_max_points(new_data.max_points);
        show_question(new_data.question);
        answer_content = new_data.answer;
        update_chances(new_data.element_list);
      } else {
        console.error('Niepoprawne dane zwrócone przez serwer:', new_data);
      }

      change_answer(false);
      user_choice_buttons(false);
      show_done_button(true);
      timer.set(0);
      timer.start();
    })
    .catch((error) => {
      console.error('Błąd podczas przetwarzania danych:', error);
    });
}

async function init() {
  try {
    show_points(0);
    show_max_points(0);
    show_question('Brak pytania')
    change_answer(false)
    show_chances(false)
    update_chances({ 'brak': 0 })
    show_done_button(true)
    user_choice_buttons(false)
    const data = await sendRequest(get_url_arguments(), 'POST', '/api/nauka/init');
    if (data) {
      show_max_points(data.max_points);
      show_question(data.question)
      update_chances(data.element_list)
      answer_content = data.answer
    }

    const done_button_listener = document.getElementById('done_button')
    done_button_listener.addEventListener('click', on_done_button)

    const user_correct = document.getElementById('button_correct')
    user_correct.addEventListener('click', on_user_correct)

    const user_wrong = document.getElementById('button_wrong')
    user_wrong.addEventListener('click', on_user_wrong)
  } catch (error) {
    console.error('Błąd inicjalizacji:', error);
  }
}
const timer = new Timer();
timer.start();

let answer_content = ''

document.addEventListener('DOMContentLoaded', init);
