function showSignup() {
  document.getElementById("login-section").style.display = "none";
  document.getElementById("signup-section").style.display = "block";
  document.getElementById("forgot-section").style.display = "none";
}

function showLogin() {
  document.getElementById("signup-section").style.display = "none";
  document.getElementById("forgot-section").style.display = "none";
  document.getElementById("login-section").style.display = "block";
}

function showForgot() {
  document.getElementById("login-section").style.display = "none";
  document.getElementById("signup-section").style.display = "none";
  document.getElementById("forgot-section").style.display = "block";
  document.getElementById("emailForm").style.display = "block";
  document.getElementById("resetForm").style.display = "none";
  document.getElementById("emailError").textContent = '';
}

async function verifyEmail(event) {
  event.preventDefault();
  const email = document.getElementById("email_reset").value;

  const response = await fetch('/verify_email', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email })
  });

  const result = await response.json();

  if (result.exists) {
    document.getElementById("emailForm").style.display = "none";
    document.getElementById("resetForm").style.display = "block";
    document.getElementById("verified_email").value = email;
  } else {
    document.getElementById("emailError").textContent = "\u274C Email not found.";
  }
}

function togglePassword(fieldId, icon) {
  const input = document.getElementById(fieldId);
  if (input.type === "password") {
    input.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

function showSection(idToShow) {
  const sections = ['login-section', 'signup-section', 'forgot-section'];
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (id === idToShow) {
      el.classList.remove("hide");
      el.style.display = "block";
    } else {
      el.classList.add("hide");
      setTimeout(() => {
        el.style.display = "none";
      }, 500); // match CSS transition duration
    }
  });
}

function showSignup() {
  showSection("signup-section");
}

function showLogin() {
  showSection("login-section");
}

function showForgot() {
  showSection("forgot-section");
}

function togglePassword(fieldId, icon) {
  const field = document.getElementById(fieldId);
  if (field.type === "password") {
    field.type = "text";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  } else {
    field.type = "password";
    icon.classList.add("fa-eye-slash");
    icon.classList.remove("fa-eye");
  }
}
