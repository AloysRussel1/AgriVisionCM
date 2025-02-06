const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Fonction de validation pour le formulaire d'inscription
// function validateRegistration() {
//     const username = document.getElementById('username');
//     const email = document.getElementById('email');
//     const password = document.getElementById('password');
//     const usernameError = document.getElementById('usernameError');
//     const emailError = document.getElementById('emailError');
//     const passwordError = document.getElementById('passwordError');

//     let isValid = true;

//     // Validation du nom d'utilisateur
//     if (username.value.trim() === '') {
//         usernameError.textContent = 'Le nom d\'utilisateur est obligatoire.';
//         isValid = false;
//     } else {
//         usernameError.textContent = '';
//     }

//     // Validation de l'email (simple)
//     if (email.value.trim() === '') {
//         emailError.textContent = 'L\'email est obligatoire.';
//         isValid = false;
//     } else if (!/\S+@\S+\.\S+/.test(email.value)) {
//         emailError.textContent = 'Veuillez entrer un email valide.';
//         isValid = false;
//     } else {
//         emailError.textContent = ''; // Efface le message d'erreur précédent avant de vérifier l'unicité

//         // Vérification asynchrone de l'email
//         fetch('/auth/check-email', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ email: email.value }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.exists) {
//                 emailError.textContent = 'Cet email est déjà utilisé.';
//                 isValid = false;
//             }
//         })
//         .catch(error => {
//             console.error('Erreur lors de la vérification de l\'email:', error);
//             emailError.textContent = 'Erreur lors de la vérification de l\'email.';
//             isValid = false;
//         });
//     }

//     // Validation du mot de passe (simple)
//     if (password.value.trim() === '') {
//         passwordError.textContent = 'Le mot de passe est obligatoire.';
//         isValid = false;
//     } else if (password.value.length < 6) {
//         passwordError.textContent = 'Le mot de passe doit contenir au moins 6 caractères.';
//         isValid = false;
//     } else {
//         passwordError.textContent = '';
//     }

//     return isValid;
// }
// // Fonction de validation pour le formulaire de connexion
// function validateLogin() {
//     const email = document.getElementById('loginEmail');
//     const password = document.getElementById('loginPassword');
//     const emailError = document.getElementById('loginEmailError');
//     const passwordError = document.getElementById('loginPasswordError');

//     let isValid = true;

//     // Validation de l'email (simple)
//     if (email.value.trim() === '') {
//         emailError.textContent = 'L\'email est obligatoire.';
//         isValid = false;
//     } else if (!/\S+@\S+\.\S+/.test(email.value)) {
//         emailError.textContent = 'Veuillez entrer un email valide.';
//         isValid = false;
//     } else {
//         emailError.textContent = '';
//     }

//     // Validation du mot de passe (simple)
//     if (password.value.trim() === '') {
//         passwordError.textContent = 'Le mot de passe est obligatoire.';
//         isValid = false;
//     } else {
//         passwordError.textContent = '';
//     }

//     return isValid;
// }

// // Écouter les événements de saisie pour la validation en temps réel
// document.getElementById('registerForm').addEventListener('input', function(e) {
//     if (e.target.id !== 'register') {
//         validateRegistration();
//     }
// });

// document.getElementById('loginForm').addEventListener('input', function(e) {
//     if (e.target.id !== 'login') {
//         validateLogin();
//     }
// });

// // Écouter les événements de soumission de formulaire
// document.getElementById('registerForm').addEventListener('submit', function(e) {
//     if (!validateRegistration()) {
//         e.preventDefault();
//     }
// });

// document.getElementById('loginForm').addEventListener('submit', function(e) {
//     if (!validateLogin()) {
//         e.preventDefault();
//     }
// });