console.log("main.js loaded");

const addToCart = (productId) => {
  var csrfToken = localStorage.getItem("csrf_token");
  console.log(csrfToken);
  // var csrfToken = "{{ csrf_token }}";
  var formData = new FormData();
  formData.append("product", productId);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/orders/add_item/", true);
  xhr.setRequestHeader("X-CSRFToken", csrfToken);

  xhr.onload = function () {
    if (xhr.status === 200) {
      // Sucesso - fazer algo se necessário
      console.log("Produto adicionado ao carrinho com sucesso!");
    } else {
      // Tratar erros, se houver
      console.error("Erro ao adicionar produto ao carrinho:", xhr.statusText);
    }
  };

  xhr.onerror = function () {
    // Tratar erros de rede
    console.error("Erro de rede ao adicionar produto ao carrinho.");
  };

  xhr.send(formData);

  // let cart = JSON.parse(localStorage.getItem("cart")) || { items: {} };

  // if (!cart.items[productId]) {
  //   cart.items[productId] = { quantity: 1 };
  // } else {
  //   cart.items[productId].quantity++;
  // }
  // localStorage.setItem("cart", JSON.stringify(cart));
  // console.log("4:", cart);
};

const emailInput = document.getElementById("id_email");
const usernameInput = document.getElementById("id_username");

if (emailInput && usernameInput) {
  emailInput.addEventListener("input", function () {
    usernameInput.value = emailInput.value;
  });
}
const redirect = (url) => {
  window.location.assign(url);
};

const inputCep = document.getElementById("id_cep");
const inputStreet = document.getElementById("id_street");
const inputUf = document.getElementById("id_uf");
const inputCity = document.getElementById("id_city");
const errorLocalization = document.getElementById("error_message_localization");
const errorCepInvalid = document.getElementById("error_message_invalid_cep");

if (inputCep) {
  inputCep.addEventListener("input", () => fetchAddViaCep(inputCep.value));
}

function fetchAddViaCep(cep) {
  // Limpa o CEP removendo caracteres não numéricos
  console.log("FOI");
  cep = cep.replace(/\D/g, "");
  if (cep.length === 0) {
    errorLocalization.style.visibility = "hidden";
  }

  if (cep.length == 8) {
    // Verifica se o CEP possui o tamanho correto
    if (cep.length !== 8) {
      console.error("CEP inválido");
      return;
    }

    // URL da API do ViaCEP para buscar o endereço pelo CEP
    const url = `https://viacep.com.br/ws/${cep}/json/`;

    // Faz a requisição GET para a API do ViaCEP
    fetch(url)
      .then((response) => {
        // Verifica se a resposta da requisição foi bem-sucedida (status 200)
        if (!response.ok) {
          throw new Error("Erro ao buscar endereço");
        }
        return response.json();
      })
      .then((data) => {
        // Exibe os dados do endereço no console

        if (data.erro) {
          errorCepInvalid.style.visibility = "visible";
        }
        if (data.uf === "MG") {
          errorLocalization.style.visibility = "hidden";
          inputStreet.value = data.logradouro;
          inputUf.value = data.uf;
          inputCity.value = data.localidade;
        } else {
          errorLocalization.style.visibility = "visible";
        }
        // Aqui você pode fazer o que quiser com os dados do endereço, como preencher campos de um formulário, por exemplo
      })
      .catch((error) => {
        console.error("Erro:", error);
      });
  }
}

// Exemplo de uso da função
// buscarEnderecoPorCEP("01001000"); // Você deve passar um CEP válido como argumento
function copyQrCodeToClipBoard() {
  const text = document.getElementById("qr-code-clip-board");
  text.select();
  document.execCommand("copy");
}

function checkPaymentStatus(payment_id, orde) {
  // Make a POST request to check the payment status
  fetch("check_payment/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ payment_id: payment_id }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.payment_status === false) {
        // Payment is not yet completed, continue checking
        setTimeout(checkPaymentStatus, 5000); // Check every 5 seconds (for example)
      } else {
        // Payment has been successfully completed, perform your desired action here
        console.log("Payment has been completed!");
        // For example, redirect to a confirmation page
        window.location.href = "/confirmation";
      }
    })
    .catch((error) => {
      // Handle errors here
      console.error("Error checking payment status:", error);
    });
}

function calculateTimeRemaining(expirationDate) {
  console.log("EXPRIRE: ", expirationDate);

  // Convert expiration date to JavaScript Date object
  var expirationDate = new Date(expirationDate);

  // Get current date and time
  var currentDate = new Date();

  // Calculate the difference in milliseconds between expiration date and current date
  var timeDifferenceInMilliseconds = expirationDate - currentDate;

  // Calculate remaining time in seconds
  var remainingSeconds = Math.floor(timeDifferenceInMilliseconds / 1000);

  // Calculate remaining minutes
  var remainingMinutes = Math.floor(remainingSeconds / 60);

  // Calculate remaining seconds after removing complete minutes
  var formattedRemainingSeconds = remainingSeconds % 60;

  // Format remaining time to 'mm:ss' format
  var formattedTimeRemaining =
    (remainingMinutes < 10 ? "0" : "") +
    remainingMinutes +
    ":" +
    (formattedRemainingSeconds < 10 ? "0" : "") +
    formattedRemainingSeconds;

  return formattedTimeRemaining;
}

// Example usage:
// var expirationDate = '2024-04-02T12:00:00'; // Replace this with your expiration date
// var timeRemainingFormatted = calculateTimeRemaining(expirationDate);
// console.log('Formatted time remaining:', timeRemainingFormatted);
