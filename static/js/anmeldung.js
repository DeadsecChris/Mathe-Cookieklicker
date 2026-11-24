// Anmeldeseite: Anmelden oder neu registrieren, danach weiter ins Hauptmenü.

const formAnmelden = document.getElementById("form-anmelden");
const formRegistrieren = document.getElementById("form-registrieren");

anfrage("/api/konto/passwortregel").then((daten) => {
  document.getElementById("passwortregel").textContent = "Passwort: " + daten.regel + ".";
});

formAnmelden.addEventListener("submit", async (ereignis) => {
  ereignis.preventDefault();
  const meldung = document.getElementById("anmelden-meldung");
  meldung.textContent = "";
  try {
    const antwort = await anfrage("/api/konto/anmelden", {
      benutzername: document.getElementById("anmelden-name").value,
      passwort: document.getElementById("anmelden-passwort").value,
    });
    window.location.href = antwort.weiter;
  } catch (fehler) {
    meldung.textContent = fehler.message;
  }
});

formRegistrieren.addEventListener("submit", async (ereignis) => {
  ereignis.preventDefault();
  const meldung = document.getElementById("reg-meldung");
  meldung.textContent = "";
  try {
    const antwort = await anfrage("/api/konto/registrieren", {
      benutzername: document.getElementById("reg-name").value,
      passwort: document.getElementById("reg-passwort").value,
      passwort_bestaetigen: document.getElementById("reg-bestaetigen").value,
    });
    window.location.href = antwort.weiter;
  } catch (fehler) {
    meldung.textContent = fehler.message;
  }
});
